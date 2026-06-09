"""Optional post-queue tail — publish Trinity-Weave after clean maintenance runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .weave_public_publish import get_weave_publish_config, run_weave_public_sync
from .live_config import load_live_config


@dataclass
class PostQueueWeavePublishResult:
    status: str
    exit_code: int
    payload: dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(self.payload, indent=2)


def run_post_queue_weave_publish(
    vault_root: Path,
    handoff: dict[str, Any],
    config_path: Path,
) -> PostQueueWeavePublishResult:
    vault_root = vault_root.resolve()
    merged = load_live_config(vault_root, config_path=config_path)
    wp = get_weave_publish_config(merged)

    def finish(status: str, code: int, payload: dict[str, Any]) -> PostQueueWeavePublishResult:
        payload["status"] = status
        payload["exit_code"] = code
        return PostQueueWeavePublishResult(status=status, exit_code=code, payload=payload)

    if wp.get("harness_enabled", True) is False:
        return finish("skipped", 0, {"reason": "harness_disabled"})

    if not wp.get("enabled", True):
        return finish("skipped", 0, {"reason": "weave_publish_disabled"})

    if wp.get("invoke_only_on_clean_success", True) and not handoff.get("queue_success", False):
        return finish("skipped", 0, {"reason": "queue_not_clean_success"})

    mode = str(handoff.get("mode") or "balance").lower()
    if mode == "fast":
        return finish("skipped", 0, {"reason": "fast_mode_skip"})

    summary = (handoff.get("changes_summary") or handoff.get("eat_queue_run_id") or "")[:120]
    push = bool(wp.get("push_on_sync", True))
    result = run_weave_public_sync(
        vault_root,
        config_path,
        push=push,
        summary=summary,
        use_lock=True,
    )
    return finish(result.status, result.exit_code, result.payload)
