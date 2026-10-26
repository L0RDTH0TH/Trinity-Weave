"""Runner observe class — person | record from code path, not catalog text.

person: runner starts a window and injects pointer/input.
record: runner compares stdout, reads a file, or runs an author-supplied command.

Catalog keys and Prefer prose cannot override. Renaming argv fields does nothing.
"""

from __future__ import annotations

from typing import Any

OBSERVE_PERSON = "person"
OBSERVE_RECORD = "record"
OBSERVE_VALUES = frozenset({OBSERVE_PERSON, OBSERVE_RECORD})

# Op that takes the person path in proof_runner (window + pointer inject).
WINDOW_POINTER_OP = "window_pointer_inject"


def classify_op_path(op: str, args: dict[str, Any] | None = None) -> str:
    """Return observe class for the runner branch that would run ``op``.

    Does not read catalog labels or Prefer summary. Args cannot reclassify a
    record op as person by renaming fields.
    """
    _ = args  # reserved; class comes from op branch, not costume keys
    op_n = str(op or "").strip()
    if op_n == WINDOW_POINTER_OP:
        return OBSERVE_PERSON
    return OBSERVE_RECORD


def proof_shape_for_observe(observe: str) -> str | None:
    """Map row observe → Prefer proof_shape."""
    o = str(observe or "").strip().lower()
    if o == OBSERVE_PERSON:
        return "moment"
    if o == OBSERVE_RECORD:
        return "contract"
    return None


def claim_class_for_observe(observe: str) -> str | None:
    """Map row observe → Prefer claim_class."""
    o = str(observe or "").strip().lower()
    if o == OBSERVE_PERSON:
        return "ask_success"
    if o == OBSERVE_RECORD:
        return "component"
    return None
