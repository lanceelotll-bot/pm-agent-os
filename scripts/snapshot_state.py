#!/usr/bin/env python3
"""Create a portable snapshot of the current PM Agent OS live state."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from shutil import copy2

from state_files import DEFAULT_SNAPSHOT_ROOT, STATE_FILES, WORKSPACE


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return slug or "snapshot"


def build_snapshot_dir(output_root: Path, label: str | None) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if label:
        return output_root / f"{timestamp}-{slugify(label)}"
    return output_root / timestamp


def update_latest_link(output_root: Path, snapshot_dir: Path) -> None:
    latest_link = output_root / "latest"
    if latest_link.is_symlink() or latest_link.exists():
        latest_link.unlink()
    latest_link.symlink_to(snapshot_dir.name, target_is_directory=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_SNAPSHOT_ROOT),
        help="directory used to store snapshots",
    )
    parser.add_argument(
        "--label",
        help="optional label appended to the timestamped snapshot directory",
    )
    parser.add_argument(
        "--no-latest-link",
        action="store_true",
        help="do not update the latest symlink",
    )
    args = parser.parse_args()

    output_root = Path(args.output_root).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    snapshot_dir = build_snapshot_dir(output_root, args.label)
    snapshot_dir.mkdir(parents=True, exist_ok=False)

    records: list[dict[str, str]] = []
    copied: list[str] = []
    missing: list[str] = []

    for item in STATE_FILES:
        snapshot_path = snapshot_dir / item.snapshot_rel
        record = {
            "title": item.title,
            "scope": item.scope,
            "source": str(item.source),
            "snapshot_path": str(snapshot_path.relative_to(snapshot_dir)),
        }

        if item.source.exists():
            snapshot_path.parent.mkdir(parents=True, exist_ok=True)
            copy2(item.source, snapshot_path)
            record["status"] = "copied"
            copied.append(f"{item.title}: {snapshot_path.relative_to(snapshot_dir)}")
        else:
            record["status"] = "missing"
            missing.append(f"{item.title}: {item.source}")

        records.append(record)

    metadata = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace": str(WORKSPACE),
        "snapshot_dir": str(snapshot_dir),
        "items": records,
    }
    metadata_path = snapshot_dir / "snapshot.json"
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    if not args.no_latest_link:
        update_latest_link(output_root, snapshot_dir)

    print(f"Created snapshot: {snapshot_dir}")
    print(f"Metadata: {metadata_path}")
    if copied:
        print("Copied files:")
        for line in copied:
            print(f"- {line}")
    if missing:
        print("Missing files:")
        for line in missing:
            print(f"- {line}")
    if not args.no_latest_link:
        print(f"Latest link: {output_root / 'latest'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
