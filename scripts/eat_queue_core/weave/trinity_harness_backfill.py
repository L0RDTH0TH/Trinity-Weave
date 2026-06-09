"""Backward extrapolation: weave/harness implementation → Trinity draft legs.

Reads Python modules and harness.py wiring so proposals carry enforcement narrative,
not only primary_paths + TODO Conceptual placeholders.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_HARNESS_CMD_DEF_RE = re.compile(
    r"def\s+cmd_(\w+)\([^)]*\)\s*->\s*[^:]+:\s*\n\s*\"\"\"(.*?)\"\"\"",
    re.DOTALL,
)
_HARNESS_CMD_CALL_RE = re.compile(
    r"def\s+cmd_(\w+)\([^)]*\)[^:]*:\s*.*?\"\"\"(.*?)\"\"\".*?"
    r"(?:from\s+\.(\w+)\s+import|(\w+)\()",
    re.DOTALL,
)
_PATH_LIT_RE = re.compile(
    r'["\']((?:\.technical|3-Resources|Ingest|scripts/eat_queue_core)[^"\']+)["\']'
)
_SUBPROC_HARNESS_RE = re.compile(
    r'subprocess\.(?:run|call|Popen)\s*\([^)]*["\']scripts\.eat_queue_core\.harness["\'][^)]*["\'](\w+)["\']',
    re.DOTALL,
)
_ACTION_KEY_RE = re.compile(r'["\']action["\']\s*:\s*["\'](\w+)["\']')
_FORBIDDEN_COMMENT_RE = re.compile(
    r"(?:must not|never|do not|forbidden|hard stop|abort)\s+([^\n\.]{8,80})",
    re.IGNORECASE,
)


@dataclass
class HarnessBackfill:
    module_path: str
    module_doc: str = ""
    harness_commands: list[str] = field(default_factory=list)
    harness_help: str = ""
    inbound_paths: list[str] = field(default_factory=list)
    outbound_paths: list[str] = field(default_factory=list)
    artifacts_touched: list[str] = field(default_factory=list)
    harness_side_effects: list[str] = field(default_factory=list)
    config_keys: list[str] = field(default_factory=list)
    enforcement_bullets: list[str] = field(default_factory=list)
    forbidden_hints: list[str] = field(default_factory=list)
    precedence_hints: list[str] = field(default_factory=list)
    primary_flow: str = ""
    misread_hints: list[str] = field(default_factory=list)

    def to_meta_dict(self) -> dict[str, Any]:
        return {
            "method": "harness_backward_extrapolation",
            "module_path": self.module_path,
            "harness_commands": self.harness_commands,
            "enforcement_bullets": self.enforcement_bullets,
            "artifacts_touched": self.artifacts_touched,
            "harness_side_effects": self.harness_side_effects,
            "config_keys": self.config_keys,
        }


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _module_docstring(text: str) -> str:
    try:
        tree = ast.parse(text)
        doc = ast.get_docstring(tree) or ""
        return doc.strip().replace("\n", " ")
    except SyntaxError:
        m = re.match(r'^\s*["\'][\'"]{3}(.*?)["\'][\'"]{3}', text, re.DOTALL)
        return (m.group(1).strip().replace("\n", " ") if m else "")[:500]


def _import_paths(text: str, vault_root: Path) -> list[str]:
    out: list[str] = []
    for m in re.finditer(r"from\s+\.([\w.]+)\s+import", text):
        mod = m.group(1).replace(".", "/")
        candidate = f"scripts/eat_queue_core/{mod}.py"
        if (vault_root / candidate).is_file():
            out.append(candidate)
    for m in re.finditer(r"from\s+\.weave\.(\w+)\s+import", text):
        candidate = f"scripts/eat_queue_core/weave/{m.group(1)}.py"
        if (vault_root / candidate).is_file():
            out.append(candidate)
    return sorted(set(out))


def _artifact_paths(text: str) -> list[str]:
    found: set[str] = set()
    for m in _PATH_LIT_RE.finditer(text):
        p = m.group(1).strip()
        if not p.endswith(".py") and "*" not in p:
            found.add(p)
    for m in re.finditer(r'/\s*["\']([^"\']+\.(?:json|jsonl|yaml|md))["\']', text):
        found.add(m.group(1))
    return sorted(found)


def _subprocess_harness_cmds(text: str) -> list[str]:
    return sorted(set(_SUBPROC_HARNESS_RE.findall(text)))


def _action_names(text: str) -> list[str]:
    return sorted(set(_ACTION_KEY_RE.findall(text)))


def _config_keys(text: str) -> list[str]:
    keys: set[str] = set()
    for block in ("DEFAULT_KNOBS", "DEFAULT_CLOCK", "DEFAULT_"):
        m = re.search(rf"{block}[^=]*=\s*\{{([^}}]+)\}}", text, re.DOTALL)
        if m:
            for km in re.finditer(r'"(\w+)":', m.group(1)):
                keys.add(km.group(1))
    return sorted(keys)[:20]


def _entry_function_flow(text: str) -> str:
    """First public function docstring (tick, run_*, main entry)."""
    try:
        tree = ast.parse(text)
        for prefer in ("tick", "run", "handle", "process", "write", "reconcile", "main"):
            for node in tree.body:
                if not isinstance(node, ast.FunctionDef):
                    continue
                if prefer == "main" or prefer in node.name:
                    doc = ast.get_docstring(node) or ""
                    if doc:
                        return f"{node.name}: {doc.strip().replace(chr(10), ' ')[:400]}"
    except SyntaxError:
        pass
    for name in ("tick", "run_", "handle_", "process_"):
        pat = rf"def\s+(\w*{name}\w*)\s*\([^)]*\)\s*(?:->[^:]+)?:\s*\n\s*\"\"\"(.*?)\"\"\""
        m = re.search(pat, text, re.DOTALL)
        if m:
            body = m.group(2).strip().replace("\n", " ")
            return f"{m.group(1)}: {body[:400]}"
    return ""


def build_harness_command_index(vault_root: Path) -> dict[str, list[dict[str, str]]]:
    """Map module stem → harness commands that call into it."""
    harness = vault_root / "scripts/eat_queue_core/harness.py"
    text = _read_text(harness)
    index: dict[str, list[dict[str, str]]] = {}
    for m in re.finditer(
        r'def\s+(cmd_\w+)\([^)]*\)\s*->\s*[^:]+:\s*\n\s*"""(.*?)"""',
        text,
        re.DOTALL,
    ):
        cmd_name = m.group(1).replace("cmd_", "", 1)
        help_text = m.group(2).strip().split("\n")[0]
        fn_start = m.end()
        fn_chunk = text[fn_start : fn_start + 2500]
        for stem in re.findall(r"from\s+\.(\w+)\s+import\s+(\w+)", fn_chunk):
            mod_stem = stem[0]
            index.setdefault(mod_stem, []).append(
                {"command": cmd_name, "help": help_text, "import": stem[1]}
            )
        for call in re.findall(r"\b(\w+)\(\s*vault_root", fn_chunk):
            if call not in ("print", "json", "Path", "load"):
                index.setdefault(call.replace("_", ""), []).append(
                    {"command": cmd_name, "help": help_text, "import": call}
                )
    return index


def analyze_module(vault_root: Path, rel_path: str) -> HarnessBackfill | None:
    if not rel_path or not rel_path.endswith(".py"):
        return None
    full = vault_root / rel_path
    if not full.is_file():
        return None
    text = _read_text(full)
    if not text.strip():
        return None

    stem = Path(rel_path).stem
    cmd_index = build_harness_command_index(vault_root)
    harness_cmds: list[dict[str, str]] = []
    for key in (stem, stem.replace("_", "")):
        harness_cmds.extend(cmd_index.get(key, []))
    # pseudo_clock → pseudo_clock_tick import tick
    if stem == "pseudo_clock":
        harness_cmds.extend(cmd_index.get("pseudo", []))
        harness_cmds.extend(
            [{"command": "pseudo_clock_tick", "help": "Weave/harness background heartbeat — threshold-driven housekeeping.", "import": "tick"}]
            if not any(c.get("command") == "pseudo_clock_tick" for c in harness_cmds)
            else []
        )

    commands = sorted({c["command"] for c in harness_cmds if c.get("command")})
    helps = [c["help"] for c in harness_cmds if c.get("help")]

    doc = _module_docstring(text)
    artifacts = _artifact_paths(text)
    inbound = _import_paths(text, vault_root)
    subprocess_cmds = _subprocess_harness_cmds(text)
    actions = _action_names(text)
    config_keys = _config_keys(text)
    flow = _entry_function_flow(text)

    forbidden: list[str] = []
    for m in _FORBIDDEN_COMMENT_RE.finditer(text):
        phrase = m.group(1).strip()
        if phrase and len(phrase) > 8:
            forbidden.append(phrase[:80])

    enforcement: list[str] = []
    if doc:
        enforcement.append(f"Module intent (docstring): {doc}")
    if commands:
        enforcement.append(f"Harness entrypoints: {', '.join(commands)}")
    if helps:
        enforcement.append(f"Harness role: {helps[0]}")
    if flow:
        enforcement.append(f"Primary flow: {flow}")
    if artifacts:
        enforcement.append(f"Artifacts read/written: {', '.join(artifacts[:8])}")
    if actions:
        enforcement.append(f"Recorded actions: {', '.join(actions[:12])}")
    if subprocess_cmds:
        enforcement.append(f"Invokes harness subcommands: {', '.join(subprocess_cmds)}")
    if config_keys:
        enforcement.append(f"Knob/config surface: {', '.join(config_keys[:10])}")

    precedence: list[str] = []
    if "parse_curator_pseudo_clock_enabled" in text or "enabled" in text:
        precedence.append("respect config master switch before side effects")
    if "merge_pending" in text:
        precedence.append("merge pending PQ before threshold evaluation")
    if subprocess_cmds:
        precedence.append("subprocess harness calls only after threshold checks")

    misread: list[str] = []
    if subprocess_cmds:
        misread.append(f"Treat as manual operator action — subprocess runs harness {subprocess_cmds}")
    if "skipped" in text:
        misread.append("Assume tick always mutates — may return skipped when disabled in config")
    if "institute" in text and "curator" in text:
        misread.append("Confuse institute bundle with deprecated curator path naming")

    outbound = list(artifacts)
    for p in inbound:
        if p not in outbound:
            outbound.append(p)

    return HarnessBackfill(
        module_path=rel_path,
        module_doc=doc,
        harness_commands=commands,
        harness_help=helps[0] if helps else "",
        inbound_paths=inbound,
        outbound_paths=outbound[:25],
        artifacts_touched=artifacts[:25],
        harness_side_effects=subprocess_cmds,
        config_keys=config_keys,
        enforcement_bullets=enforcement,
        forbidden_hints=forbidden[:8],
        precedence_hints=precedence,
        primary_flow=flow,
        misread_hints=misread,
    )


def _harness_import_map(harness_text: str) -> dict[str, str]:
    """Callable name in harness → module stem (e.g. pseudo_clock_tick → pseudo_clock)."""
    mapping: dict[str, str] = {}
    for m in re.finditer(
        r"from\s+\.([\w.]+)\s+import\s+([\w]+)(?:\s+as\s+(\w+))?",
        harness_text[:8000],
    ):
        mod_path = m.group(1).replace(".", "/")
        stem = mod_path.split("/")[-1]
        alias = m.group(3) or m.group(2)
        mapping[alias] = stem
        mapping[m.group(2)] = stem
    return mapping


def _extract_cmd_function_body(harness_text: str, cmd: str) -> str:
    m = re.search(
        rf"def\s+cmd_{re.escape(cmd)}\([^)]*\)[^:]*:.*?(?=\ndef\s+cmd_|\ndef\s+main\b|\Z)",
        harness_text,
        re.DOTALL,
    )
    return m.group(0) if m else ""


# Harness subcommand → implementation module (when cmd body delegates here).
_CMD_PRIMARY_MODULE: dict[str, str] = {
    "rewrite_consumed": "scripts/eat_queue_core/full_cycle.py",
    "append_entries": "scripts/eat_queue_core/a5b_dedupe.py",
    "plan": "scripts/eat_queue_core/plan.py",
    "snapshot": "scripts/eat_queue_core/harness.py",
    "verify": "scripts/eat_queue_core/harness.py",
    "post_queue_gitforge": "scripts/eat_queue_core/post_queue_gitforge.py",
    "post_queue_memory_pass": "scripts/eat_queue_core/continuity_handoff.py",
    "headless_eat": "scripts/eat_queue_core/headless_orchestrator.py",
    "headless_architect": "scripts/eat_queue_core/headless_architect.py",
    "headless_fanout": "scripts/eat_queue_core/headless_orchestrator.py",
    "pseudo_clock_tick": "scripts/eat_queue_core/pseudo_clock.py",
}


def analyze_harness_command(vault_root: Path, cmd: str) -> HarnessBackfill | None:
    """Extrapolate from cmd_* body + help, not the whole harness.py module docstring."""
    harness_path = vault_root / "scripts/eat_queue_core/harness.py"
    harness = _read_text(harness_path)
    body = _extract_cmd_function_body(harness, cmd)
    if not body:
        return None
    help_m = re.search(
        rf'def\s+cmd_{re.escape(cmd)}\([^)]*\)[^:]*:\s*\n\s*"""(.*?)"""',
        harness,
        re.DOTALL,
    )
    harness_help = (help_m.group(1).strip().split("\n")[0] if help_m else "") or cmd

    primary_rel = _CMD_PRIMARY_MODULE.get(cmd)
    if not primary_rel:
        primary_rel = resolve_primary_path_for_trinity_id(
            vault_root, f"harness_{cmd}", f"scripts/eat_queue_core/harness.py#cmd:{cmd}"
        )
    if primary_rel.endswith("harness.py"):
        primary_rel = "scripts/eat_queue_core/harness.py"

    mod_backfill = analyze_module(vault_root, primary_rel) if primary_rel else None
    enforcement: list[str] = [f"Harness subcommand `{cmd}`: {harness_help}"]
    if mod_backfill and mod_backfill.module_doc:
        enforcement.append(f"Implementation ({primary_rel}): {mod_backfill.module_doc[:200]}")
    if "apply_queue_cleanup_dual_track" in body:
        enforcement.append(
            "Dual-track fanout: remove consumed ids from track PQ and central pool when enabled"
        )
    elif "apply_queue_cleanup" in body:
        enforcement.append("Read–filter–write PQ lines whose id is in removal set")
    if "queue_rewrite_ids" in body or "consumed_ids" in body:
        enforcement.append("Accept ids from --plan (queue_rewrite_ids / consumed_ids) or --ids")
    if mod_backfill:
        enforcement.extend(mod_backfill.enforcement_bullets[2:6])

    flow = ""
    if help_m:
        flow = f"cmd_{cmd}: {harness_help}"
    elif mod_backfill:
        flow = mod_backfill.primary_flow

    forbidden: list[str] = []
    if cmd == "rewrite_consumed":
        forbidden = [
            "Layer 0 or Layer 1 ad-hoc PQ line deletion outside harness rewrite_consumed",
            "rewrite before Pass 3 inline repair drain completes when repair ids belong in plan",
            "drop central pool lines but leave track PQ (or vice versa) under dual-track fanout",
        ]
        precedence = [
            "Layer 1 builds processed_success_ids and re-reads PQ before calling harness",
            "pass --plan eat_queue_run_plan.json so queue_rewrite_ids includes Pass 3 entries",
            "dual-track: apply_queue_cleanup_dual_track unless --single-pool",
        ]
        misread = [
            "Treating rewrite as optional cleanup — A.7 is mandatory for consumed success ids",
            "Editing PQ with shell append instead of append_entries for new lines",
            "Removing ids not in processed_success_ids — drops in-flight or failed entries incorrectly",
        ]
    else:
        precedence = mod_backfill.precedence_hints if mod_backfill else []
        misread = mod_backfill.misread_hints if mod_backfill else []
        forbidden = mod_backfill.forbidden_hints if mod_backfill else []

    artifacts = ["scripts/eat_queue_core/harness.py", ".technical/prompt-queue.jsonl"]
    if mod_backfill:
        artifacts.extend(mod_backfill.artifacts_touched)
    artifacts = sorted(set(artifacts))[:25]

    return HarnessBackfill(
        module_path=primary_rel or "scripts/eat_queue_core/harness.py",
        module_doc=harness_help,
        harness_commands=[cmd],
        harness_help=harness_help,
        inbound_paths=(mod_backfill.inbound_paths if mod_backfill else [])
        + ["scripts/eat_queue_core/harness.py"],
        outbound_paths=artifacts,
        artifacts_touched=artifacts,
        harness_side_effects=mod_backfill.harness_side_effects if mod_backfill else [],
        config_keys=mod_backfill.config_keys if mod_backfill else [],
        enforcement_bullets=enforcement,
        forbidden_hints=forbidden,
        precedence_hints=precedence,
        primary_flow=flow,
        misread_hints=misread,
    )


def resolve_primary_path_for_trinity_id(
    vault_root: Path, trinity_id: str, primary_path: str
) -> str:
    if primary_path and not primary_path.endswith("harness.py") and "#cmd:" not in primary_path:
        if (vault_root / primary_path).is_file():
            return primary_path
    if trinity_id.startswith("harness_"):
        cmd = trinity_id.removeprefix("harness_")
        mapped = _CMD_PRIMARY_MODULE.get(cmd)
        if mapped and (vault_root / mapped).is_file():
            return mapped
        harness_path = vault_root / "scripts/eat_queue_core/harness.py"
        harness = _read_text(harness_path)
        body = _extract_cmd_function_body(harness, cmd)
        import_map = _harness_import_map(harness)
        mod_stem: str | None = None
        for call in re.findall(r"\b(\w+)\(\s*vault_root", body):
            if call in import_map:
                mod_stem = import_map[call]
                break
        if not mod_stem:
            fm = re.search(r"from\s+\.([\w.]+)\s+import", body)
            if fm:
                mod_stem = fm.group(1).split(".")[-1]
        if mod_stem:
            for candidate in (
                f"scripts/eat_queue_core/{mod_stem}.py",
                f"scripts/eat_queue_core/weave/{mod_stem}.py",
            ):
                if (vault_root / candidate).is_file():
                    return candidate
    if primary_path and (vault_root / primary_path.split("#")[0]).is_file():
        return primary_path.split("#")[0]
    return primary_path


def apply_backfill_to_card(card: dict[str, Any], backfill: HarnessBackfill) -> dict[str, Any]:
    """Merge extrapolated legs into card; keep operator_question in meta.source."""
    component = card.get("id", "component")
    doc = backfill.module_doc

    outcome = doc if doc else f"Enforces weave behavior for {component} (see meta.backfill)."
    if backfill.harness_commands:
        outcome = (
            f"{outcome} Harness: {', '.join(backfill.harness_commands)}."
            if doc
            else f"Weave enforcement via harness {', '.join(backfill.harness_commands)} — {doc or component}."
        )

    summary_parts = [
        "Backward extrapolation from implementation (harness + module). "
        "Validate Conceptual against code; correct intent if disconnected."
    ]
    if backfill.enforcement_bullets:
        summary_parts.append(backfill.enforcement_bullets[0])
    summary = " ".join(summary_parts)[:900]

    if backfill.primary_flow:
        primary_case = backfill.primary_flow
    elif backfill.enforcement_bullets:
        primary_case = " ".join(backfill.enforcement_bullets[1:4])[:800]
    else:
        primary_case = (
            f"See meta.backfill and `{backfill.module_path}`; "
            "validate enforcement bullets against harness."
        )

    edge_cases: list[str] = []
    if backfill.config_keys:
        edge_cases.append(f"Config/knobs: {', '.join(backfill.config_keys[:8])}")
    if backfill.harness_side_effects:
        edge_cases.append(f"May subprocess-call harness: {', '.join(backfill.harness_side_effects)}")
    edge_cases.append("Returns skipped when config master switch disables this weave path")

    misread = list(backfill.misread_hints)
    if not misread:
        misread = ["Treating TODO placeholders as final — read meta.backfill and source file"]

    conceptual = dict(card.get("conceptual") or {})
    conceptual.update(
        {
            "outcome": outcome[:500],
            "summary": summary,
            "primary_case": primary_case[:800],
            "edge_cases": edge_cases or conceptual.get("edge_cases") or [],
            "misread_risks": misread[:6],
        }
    )
    card["conceptual"] = conceptual

    touch = dict(card.get("touch") or {})
    paths = list(touch.get("primary_paths") or [])
    if backfill.module_path and backfill.module_path not in paths:
        paths.insert(0, backfill.module_path)
    touch["primary_paths"] = paths
    inbound = list(touch.get("inbound") or [])
    for p in backfill.inbound_paths:
        if p not in inbound:
            inbound.append(p)
    touch["inbound"] = inbound[:30]
    outbound = list(touch.get("outbound") or [])
    for p in backfill.outbound_paths:
        if p not in outbound:
            outbound.append(p)
    touch["outbound"] = outbound[:30]
    if backfill.harness_commands:
        touch["harness_commands"] = backfill.harness_commands
    card["touch"] = touch

    rules = dict(card.get("rules") or {})
    forbidden = list(rules.get("forbidden") or [])
    for h in backfill.forbidden_hints:
        if h not in forbidden:
            forbidden.append(h[:100])
    if not forbidden:
        forbidden = [
            "bypass harness-only write contract",
            "mutate without reading config master switch",
            "treat subprocess side effects as operator-approved without review",
        ]
    rules["forbidden"] = forbidden[:10]
    precedence = list(rules.get("precedence") or [])
    for h in backfill.precedence_hints:
        if h not in precedence:
            precedence.append(h)
    if not precedence:
        precedence = ["config gate before side effects", "read artifacts before write"]
    rules["precedence"] = precedence[:10]
    card["rules"] = rules

    meta = dict(card.get("meta") or {})
    source = dict(meta.get("source") or {})
    source["backfill"] = backfill.to_meta_dict()
    meta["source"] = source
    card["meta"] = meta
    return card
