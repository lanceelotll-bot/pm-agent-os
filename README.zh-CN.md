# PM Agent OS

[English](README.md) | [简体中文](README.zh-CN.md) | [最小白快速开始](docs/quick-start.zh-CN.md) | [非技术背景使用说明](docs/user-guide.zh-CN.md)

这是一个面向产品经理的可复用工作系统，目标是在频繁切换 team、切换会话、切换模型平台时，仍然保持对话、记忆和执行的连续性。

## 这个仓库解决什么问题

- 把稳定的个人记忆从单次聊天中抽离出来
- 把 team 专属上下文和个人长期记忆分开维护
- 让每个任务都能被交接和续接
- 用一组面向产品经理的 agent 角色来路由工作

## 推荐的记忆分层

1. 全局记忆
   将长期稳定的个人上下文放在 `~/.codex/memories/memory.md`。
2. Team 上下文
   将 team 专属信息放在仓库内，基于 `templates/team-context.template.md` 生成。
3. 历史精华
   将长期有价值的历史对话结论和共识压缩到 `context/history-highlights.md`。
4. 任务简报
   对于非 trivial 的任务，创建一个简短的 task packet。
5. 交接状态
   每次工作结束时更新当前 handoff 文件。
6. Manifest
   如果你希望跨模型、跨平台都使用同一套加载规则，使用 `templates/context-manifest.template.yaml`。

## 推荐的团队仓库结构

```text
context/
  team-context.md
  team-context.example.md
  history-highlights.md
  history-highlights.example.md
handoffs/
  current.md
  current.example.md
tasks/
  active/
    current.md
    current.example.md
docs/
  pm-agent-cluster.md
```

## 建议的工作流程

1. 先填写 `templates/personal-memory.template.md`，然后将结果保存到 `~/.codex/memories/memory.md`。
2. 每加入一个新 team，就基于 `templates/team-context.template.md` 创建 `context/team-context.md`。
3. 当形成长期仍有价值的历史结论时，更新 `context/history-highlights.md`。
4. 每遇到一个较大的任务，就基于 `templates/task-brief.template.md` 创建任务简报。
5. 每次工作结束时，用 `templates/handoff.template.md` 更新 `handoffs/current.md`，必要时同步更新 `context/history-highlights.md`。
6. 下次开始工作时，使用 `templates/session-bootstrap-prompt.template.md` 中的启动提示。
7. 在 Codex 兼容环境中，可以用 `AGENTS.md` 作为同平台自动加载策略。
8. 如果要上传到 Git，请只提交 `.example` 文件、模板、文档和脚本，运行态文件保留在本地。

## 实践原则

不要把聊天记录当成唯一真相源。把聊天当成执行空间，把文件当成记忆空间。

## 平台读取方式

- `Codex / 可读本地文件的工作区`
  - 通常可以直接读取本地状态文件
  - 可以走“文件读取版”恢复
  - 更适合做 `close` 收尾和本地回写

- `Claude / Kimi / 千问 / GPT 客户端或网页端`
  - 当前 baseline 默认不能直接读取你电脑上的本地文件
  - 只能走“嵌入式上下文包”恢复
  - 它们能续接，是因为你贴入了压缩后的状态，不是因为它们自己会去读盘

- 如果你以后希望外部客户端也能直接读文件
  - 需要再加一层 wrapper、本地连接器或类似 MCP 的方案
  - 这不在当前 baseline 范围内

## Git 使用约定

- 提交模板、文档、脚本、skill 和 `.example` 上下文文件。
- 把 `context/team-context.md`、`context/history-highlights.md`、`handoffs/current.md` 和 `tasks/active/current.md` 留在本地。
- 克隆仓库后，基于 `.example` 文件或模板创建自己的 live 文件。

## 仓库中的关键文件

- `docs/pm-agent-cluster.md`：产品经理 agent 集群设计
- `docs/platform-adapters.md`：不同平台的接入方式
- `docs/quick-start.zh-CN.md`：最小白快速开始
- `docs/user-guide.zh-CN.md`：给非技术背景用户的使用说明
- `scripts/pm_prompt.py`：一键生成并复制恢复/收尾提示词
- `templates/personal-memory.template.md`：个人长期记忆模板
- `templates/personal-memory.zh-CN.template.md`：个人长期记忆中文填写模板
- `templates/team-context.template.md`：team 上下文模板
- `templates/team-context.zh-CN.template.md`：team 上下文中文填写模板
- `templates/history-highlights.zh-CN.template.md`：历史精华中文填写模板
- `templates/task-brief.template.md`：标准任务简报模板
- `templates/handoff.template.md`：交接模板
- `templates/session-bootstrap-prompt.template.md`：会话续接提示模板
- `templates/platform-prompts/`：Codex、Claude、Kimi 的平台适配提示
- `templates/context-manifest.template.yaml`：统一上下文加载契约
- `docs/cross-platform-memory-protocol.md`：跨平台记忆协议
- `AGENTS.md`：工作区级别自动加载策略
- `skills/pm-agent-os/`：可复用的 Codex skill 包
- `scripts/build_context_pack.py`：把当前状态导出为一个可跨平台使用的上下文包
