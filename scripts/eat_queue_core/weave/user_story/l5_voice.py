"""L5 scope voice guard — experiential complete vision, not factory compliance prose."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_COMPLIANCE_PATTERNS = (
    re.compile(r"REQ[-_][A-Z0-9-]+", re.I),
    re.compile(r"\|\s*REQ[-_]", re.I),
    re.compile(r"KH-\d", re.I),
    re.compile(r"OQ[-_]factory[-_]001", re.I),
    re.compile(r"horizon[_\s-]?demo", re.I),
    re.compile(r"AttestationSeparationPolicy", re.I),
    re.compile(r"factory_staged_dispatch", re.I),
    re.compile(r"gate\s+checklist", re.I),
    re.compile(r"evidence\s+pack", re.I),
)

_REQUIRED_SECTIONS = (
    re.compile(r"^##\s+Complete vision\s*$", re.MULTILINE | re.I),
    re.compile(r"^##\s+Core loop\s*$", re.MULTILINE | re.I),
)


@dataclass(frozen=True)
class L5VoiceResult:
    ok: bool
    violations: tuple[str, ...] = field(default_factory=tuple)
    compliance_hits: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "violations": list(self.violations),
            "compliance_hits": self.compliance_hits,
        }


def _strip_frontmatter(text: str) -> str:
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    return text[m.end() :] if m else text


def validate_l5_voice(text: str, *, max_compliance_hits: int = 4) -> L5VoiceResult:
    """
    Reject L5 bodies dominated by REQ/gate/horizon_demo compliance boilerplate.

    Requires Complete vision + Core loop sections (template shape).
    """
    body = _strip_frontmatter(text.strip())
    if len(body) < 200:
        return L5VoiceResult(False, ("l5_too_short",))

    violations: list[str] = []
    for pat in _REQUIRED_SECTIONS:
        if not pat.search(body):
            violations.append(f"missing_section:{pat.pattern}")

    compliance_hits = 0
    for pat in _COMPLIANCE_PATTERNS:
        compliance_hits += len(pat.findall(body))

    gate_rows = len(re.findall(r"^\|", body, re.MULTILINE))
    if gate_rows > 12 and compliance_hits >= 2:
        violations.append("compliance_table_density")

    if compliance_hits > max_compliance_hits:
        violations.append(f"compliance_prose_density:{compliance_hits}")

    experiential = len(
        re.findall(
            r"(?i)\b(player|when complete|core loop|ship tier|experien|mutate until parity)\b",
            body,
        )
    )
    if experiential < 2 and compliance_hits >= 3:
        violations.append("experiential_voice_missing")

    return L5VoiceResult(
        ok=not violations,
        violations=tuple(violations),
        compliance_hits=compliance_hits,
    )
