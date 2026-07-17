"""Proof tiers for kinesthetic / Surface seat — structural lint cannot ship."""

from __future__ import annotations

# Sources that may set kinesthetic pass:true (ship tier).
KINESTHETIC_SHIP_SOURCES: frozenset[str] = frozenset(
    {"operator", "simulated_input", "playtest_trace"}
)

# Sources that inform only — never certify human operate.
STRUCTURAL_LINT_SOURCES: frozenset[str] = frozenset(
    {"structural_lint", "static", "smoke", "factory", "probe"}
)

LEGACY_SOURCE_ALIASES: dict[str, str] = {
    "static": "structural_lint",
    "smoke": "structural_lint",
    "factory": "structural_lint",
    "probe": "structural_lint",
}


def normalize_source(source: str | None) -> str:
    raw = (source or "").strip().lower()
    return LEGACY_SOURCE_ALIASES.get(raw, raw or "unknown")


def source_may_ship_kinesthetic(source: str | None, *, operator_confirmed: bool = False) -> bool:
    norm = normalize_source(source)
    if norm == "playtest_trace":
        return operator_confirmed
    return norm in KINESTHETIC_SHIP_SOURCES - {"playtest_trace"}


def is_proxy_pass_as_kinesthetic(
    *,
    kinesthetic: bool,
    pass_val: bool | None,
    source: str | None,
    operator_confirmed: bool = False,
) -> bool:
    if not kinesthetic or pass_val is not True:
        return False
    norm = normalize_source(source)
    if norm in STRUCTURAL_LINT_SOURCES:
        return True
    if norm == "playtest_trace" and not operator_confirmed:
        return True
    return False
