#!/usr/bin/env python3
"""Restore PM Agent OS live state from a snapshot directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from shutil import copy2

from state_files import DEFAULT_SNAPSHOT_ROOT, STATE_FILES, WORKSPACE, resolve_target


def load_metadata(snapshot_dir: Path) -> dict[str, object] | None:
    metadata_path = snapshot_dir / "snapshot.json"
    if not metadata_path.exists():
        return None
    try:
        return json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--snapshot",
        default=str(DEFAULT_SNAPSHOT_ROOT / "latest"),
        help="snapshot directory to restore from",
    )
    parser.add_argument(
        "--workspace",
        help="restore workspace-scoped files into this workspace instead of the current repo",
    )
    parser.add_argument(
        "--skip-global-memory",
        action="store_true",
        help="do not restore ~/.codex/memories/memory.md",
    )
    parser.add_argument(
        "--skip-workspace-files",
        action="store_true",
        help="do not restore repo-local continuity files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be restored without writing files",
    )
    args = parser.parse_args()

    snapshot_dir = Path(args.snapshot).expanduser()
    if not snapshot_dir.exists():
        raise SystemExit(f"Snapshot not found: {snapshot_dir}")

    metadata = load_metadata(snapshot_dir.resolve())
    workspace_root = Path(args.workspace).expanduser().resolve() if args.workspace else WORKSPACE

    restored: list[str] = []
    skipped: list[str] = []
    missing: list[str] = []

    for item in STATE_FILES:
        if item.scope == "global" and args.skip_global_memory:
            skipped.append(f"{item.title}: skipped by flag")
            continue
        if item.scope == "workspace" and args.skip_workspace_files:
            skipped.append(f"{item.title}: skipped by flag")
            continue

        source_path = snapshot_dir / item.snapshot_rel
        if not source_path.exists():
            missing.append(f"{item.title}: {source_path}")
            continue

        target_path = resolve_target(item, workspace_root)
        if args.dry_run:
            restored.append(f"{item.title}: {source_path} -> {target_path}")
            continue

        target_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(source_path, target_path)
        restored.append(f"{item.title}: {target_path}")

    print(f"Snapshot: {snapshot_dir.resolve()}")
    print(f"Workspace target: {workspace_root}")
    if metadata and metadata.get("workspace"):
        print(f"Original workspace: {metadata['workspace']}")
    if args.dry_run:
        print("Dry run only. No files were written.")
    if restored:
        print("Restore actions:")
        for line in restored:
            print(f"- {line}")
    if skipped:
        print("Skipped:")
        for line in skipped:
            print(f"- {line}")
    if missing:
        print("Missing in snapshot:")
        for line in missing:
            print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
