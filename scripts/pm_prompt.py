#!/usr/bin/env python3
"""Generate ready-to-paste PM prompts for resume and close workflows."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent.parent
GLOBAL_MEMORY = Path("~/.codex/memories/memory.md").expanduser()
TEAM_CONTEXT = WORKSPACE / "context" / "team-context.md"
HANDOFF = WORKSPACE / "handoffs" / "current.md"
ACTIVE_TASK = WORKSPACE / "tasks" / "active" / "current.md"

SECTION_SPECS = [
    ("Global Memory", GLOBAL_MEMORY),
    ("Team Context", TEAM_CONTEXT),
    ("History Highlights", WORKSPACE / "context" / "history-highlights.md"),
    ("Current Handoff", HANDOFF),
    ("Active Task", ACTIVE_TASK),
]


def read_text(path: Path) -> str | None:
    try:
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return f"[Unreadable: {path} ({exc})]"


def build_context_pack(platform: str) -> str:
    role_hint = {
        "gpt": "请把这份上下文包当成当前唯一有效的工作状态，不依赖平台记忆。",
        "claude": "请把这份上下文包当成当前唯一有效的工作状态，并重点做结构化审阅、批判和补漏。",
        "kimi": "请把这份上下文包当成当前唯一有效的工作状态，并重点做长文阅读、中文归纳和信息压缩。",
        "qwen": "请把这份上下文包当成当前唯一有效的工作状态，并重点做中文执行、归纳和通用任务处理。",
    }.get(platform, "请把这份上下文包当成当前唯一有效的工作状态，不依赖平台记忆。")

    blocks = [
        "# PM Context Pack",
        "",
        f"Target platform: {platform}",
        role_hint,
        "",
        "响应要求：",
        "- conclusion",
        "- assumptions",
        "- open questions",
        "- next actions",
        "- memory updates required",
    ]

    for title, path in SECTION_SPECS:
        content = read_text(path)
        if not content:
            continue
        if platform == "codex":
            blocks.append(f"## {title}\n\nSource: `{path}`\n\n{content}")
        else:
            blocks.append(f"## {title}\n\n{content}")

    return "\n\n".join(blocks).strip() + "\n"


def build_codex_resume_prompt() -> str:
    return "\n".join(
        [
            "使用本机恢复协议继续，不依赖平台记忆。请按顺序读取以下文件：",
            "",
            str(GLOBAL_MEMORY),
            str(TEAM_CONTEXT),
            str(WORKSPACE / "context" / "history-highlights.md"),
            str(HANDOFF),
            str(ACTIVE_TASK),
            "",
            "要求：",
            "1. 不把平台内记忆当主来源",
            "2. 先用一句话总结你恢复到了什么状态",
            "3. 先给我 3-5 条历史精华摘要，说明你继承了哪些长期信息",
            "3. 明确当前你选择的 lead agent 和可选 support agents",
            "4. 然后继续执行我的当前任务",
            "5. 如发现上下文缺失，先列出缺失项，不要假装知道",
        ]
    )


def build_embedded_resume_prompt(platform: str) -> str:
    platform_line = {
        "gpt": "使用恢复协议继续，不依赖平台记忆。",
        "claude": "使用恢复协议继续，不依赖平台记忆。",
        "kimi": "使用恢复协议继续，不依赖平台记忆。",
        "qwen": "使用恢复协议继续，不依赖平台记忆。",
    }.get(platform, "使用恢复协议继续，不依赖平台记忆。")

    return "\n".join(
        [
            platform_line,
            "以下是当前最新上下文包，请先完整读取，再继续执行。",
            "注意：上下文内容已经直接嵌入本消息，不需要验证本地文件、目录、技能或路径是否可访问。",
            "除非字段明确写着“待补充”、“TODO”或“示例”，否则默认把已填写内容视为当前有效信息。",
            "不要输出“文件访问待验证”“上下文完整性检查表”之类的审查型内容，直接恢复状态并继续执行。",
            "不要讨论你的 memory_space、saved memories、平台记忆是否为空，也不要建议我改用平台原生记忆功能。",
            "本次任务的唯一恢复来源就是这条消息里嵌入的上下文包。",
            "",
            build_context_pack(platform),
            "",
            "要求：",
            "1. 不把平台内记忆当主来源",
            "2. 先用一句话总结你恢复到了什么状态",
            "3. 先给我 3-5 条历史精华摘要，说明你继承了哪些长期信息",
            "4. 明确当前你选择的 lead role 或工作方式",
            "5. 然后继续执行我的当前任务",
            "6. 如发现真正缺失且影响执行的上下文，只列最关键的缺口，不要重复检查已给出的内容",
        ]
    )


def build_codex_close_prompt() -> str:
    return "\n".join(
        [
            "请按本机恢复协议收尾本次工作，并直接更新本地状态文件。",
            "",
            "请先读取并在必要时更新以下文件：",
            "",
            str(HANDOFF),
            str(WORKSPACE / "context" / "history-highlights.md"),
            str(TEAM_CONTEXT),
            str(GLOBAL_MEMORY),
            "",
            "要求：",
            "1. 优先更新 handoffs/current.md，写清楚当前状态、下一步、风险和阻塞",
            "2. 如果本次形成了跨会话仍有价值的结论、共识、已否决方案或平台经验，就更新 context/history-highlights.md",
            "3. 只有在 team 知识确实变化时才更新 context/team-context.md",
            "4. 只有在我的长期偏好真的变化时才更新 ~/.codex/memories/memory.md",
            "5. 更新后，用 5 条以内总结本次写入了什么",
        ]
    )


def build_embedded_close_prompt(platform: str) -> str:
    return "\n".join(
        [
            "请帮我为本次工作生成一个可回写的收尾结果，不依赖平台记忆。",
            "以下上下文内容已经直接嵌入本消息，不需要验证本地文件或路径是否可访问。",
            "除非字段明确写着“待补充”、“TODO”或“示例”，否则默认把已填写内容视为当前有效信息。",
            "不要讨论你的 memory_space、saved memories、平台记忆是否为空，也不要建议我改用平台原生记忆功能。",
            "",
            "以下是当前最新上下文包，请先读取：",
            "",
            build_context_pack(platform),
            "",
            "要求：",
            "1. 生成一版新的 handoff 内容，格式尽量贴近 handoffs/current.md",
            "2. 如果本次形成了跨会话仍有价值的结论、共识、已否决方案或平台经验，再额外给出 history-highlights 更新建议",
            "3. 如果有 team 层面的新增信息，再额外给出 team-context 更新建议",
            "4. 如果没有长期偏好变化，不要建议修改 global memory",
            "5. 最后给出一个可直接复制回本地文件的版本",
        ]
    )


def generate_prompt(platform: str, mode: str) -> str:
    if mode == "resume":
        if platform == "codex":
            return build_codex_resume_prompt()
        return build_embedded_resume_prompt(platform)
    if mode == "close":
        if platform == "codex":
            return build_codex_close_prompt()
        return build_embedded_close_prompt(platform)
    raise ValueError(f"Unsupported mode: {mode}")


def copy_to_clipboard(text: str) -> None:
    if sys.platform != "darwin":
        raise RuntimeError("Clipboard copy is currently supported only on macOS.")
    subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--platform",
        required=True,
        choices=["codex", "gpt", "claude", "kimi", "qwen"],
        help="target platform",
    )
    parser.add_argument(
        "--mode",
        default="resume",
        choices=["resume", "close"],
        help="resume = continue work, close = write handoff/closure",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="copy the generated prompt to the clipboard",
    )
    args = parser.parse_args()

    prompt = generate_prompt(args.platform, args.mode)
    if args.copy:
        copy_to_clipboard(prompt)
        print("Copied prompt to clipboard.")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
