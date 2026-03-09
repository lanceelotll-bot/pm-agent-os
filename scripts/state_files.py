#!/usr/bin/env python3
"""Shared PM Agent OS live state file definitions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent.parent
GLOBAL_MEMORY = Path("~/.codex/memories/memory.md").expanduser()
TEAM_CONTEXT = WORKSPACE / "context" / "team-context.md"
HISTORY_HIGHLIGHTS = WORKSPACE / "context" / "history-highlights.md"
HANDOFF = WORKSPACE / "handoffs" / "current.md"
ACTIVE_TASK = WORKSPACE / "tasks" / "active" / "current.md"
DEFAULT_SNAPSHOT_ROOT = WORKSPACE / "state-backups"


@dataclass(frozen=True)
class StateFile:
    title: str
    source: Path
    scope: str
    restore_rel: Path
    snapshot_rel: Path


STATE_FILES = (
    StateFile(
        title="Global Memory",
        source=GLOBAL_MEMORY,
        scope="global",
        restore_rel=Path("memory.md"),
        snapshot_rel=Path("global-memory/memory.md"),
    ),
    StateFile(
        title="Team Context",
        source=TEAM_CONTEXT,
        scope="workspace",
        restore_rel=Path("context/team-context.md"),
        snapshot_rel=Path("workspace/context/team-context.md"),
    ),
    StateFile(
        title="History Highlights",
        source=HISTORY_HIGHLIGHTS,
        scope="workspace",
        restore_rel=Path("context/history-highlights.md"),
        snapshot_rel=Path("workspace/context/history-highlights.md"),
    ),
    StateFile(
        title="Current Handoff",
        source=HANDOFF,
        scope="workspace",
        restore_rel=Path("handoffs/current.md"),
        snapshot_rel=Path("workspace/handoffs/current.md"),
    ),
    StateFile(
        title="Active Task",
        source=ACTIVE_TASK,
        scope="workspace",
        restore_rel=Path("tasks/active/current.md"),
        snapshot_rel=Path("workspace/tasks/active/current.md"),
    ),
)

SECTION_SPECS = tuple((item.title, item.source) for item in STATE_FILES)


def resolve_target(item: StateFile, workspace: Path | None = None) -> Path:
    if item.scope == "global":
        return GLOBAL_MEMORY
    root = workspace or WORKSPACE
    return root / item.restore_rel
