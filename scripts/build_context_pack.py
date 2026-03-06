#!/usr/bin/env python3
"""Build a portable PM context pack from the standard workspace files."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


SECTION_SPECS = [
    ("Global Memory", Path("~/.codex/memories/memory.md").expanduser()),
    ("Team Context", Path("context/team-context.md")),
    ("History Highlights", Path("context/history-highlights.md")),
    ("Current Handoff", Path("handoffs/current.md")),
    ("Active Task", Path("tasks/active/current.md")),
]


def read_text(path: Path) -> str | None:
    try:
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return f"[Unreadable: {path} ({exc})]"


def build_header(platform: str) -> str:
    platform_name = platform.lower()
    role_hint = {
        "generic": "Read this context pack before handling the task.",
        "gpt": "Read this context pack and use it as the current source of truth.",
        "codex": "Read this context pack and follow the workspace continuity contract.",
        "claude": "Read this context pack and focus on critique, structure, and edge-case review.",
        "kimi": "Read this context pack and focus on long-document digestion and Chinese synthesis.",
    }.get(platform_name, "Read this context pack before handling the task.")
    return "\n".join(
        [
            "# PM Context Pack",
            "",
            f"Target platform: {platform}",
            role_hint,
            "",
            "Response contract:",
            "- conclusion",
            "- assumptions",
            "- open questions",
            "- next actions",
            "- memory updates required",
        ]
    )


def iter_sections(section_specs: Iterable[tuple[str, Path]]) -> list[str]:
    blocks: list[str] = []
    for title, path in section_specs:
        content = read_text(path)
        if not content:
            continue
        blocks.append(f"## {title}\n\nSource: `{path}`\n\n{content}")
    return blocks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform",
        default="generic",
        choices=["generic", "gpt", "codex", "claude", "kimi"],
        help="tailor the header for the target platform",
    )
    parser.add_argument(
        "--output",
        help="optional output path; if omitted, print to stdout",
    )
    args = parser.parse_args()

    parts = [build_header(args.platform)]
    parts.extend(iter_sections(SECTION_SPECS))

    if len(parts) == 1:
        parts.append("No context files were found.")

    result = "\n\n".join(parts) + "\n"
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result, encoding="utf-8")
    else:
        print(result, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
