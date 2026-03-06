# 团队接入指南

这份文档回答一个最实际的问题：

**别人怎么继承 PM Agent OS 这套设计？**

结论先说：

- 继承这套设计，核心靠的是 `仓库 + 模板 + 脚本 + 状态文件协议`
- `skill` 只是给 Codex 用户的增强层，不是所有人的必需品

## 先区分三层

### 第一层：继承方法论

这一层任何人都能继承，不需要安装 skill。

包括：

- 记忆分层
- 恢复/收尾流程
- 上下文包协议
- agent 集群设计
- 跨平台续接规则

只要拿到仓库，就拿到了这一层。

### 第二层：继承工作流

这一层是大多数人真正需要的。

包括：

- 填自己的 `memory.md`
- 填自己的 `team-context.md`
- 用 `pm_prompt.py` 生成恢复和收尾提示词
- 用 `history-highlights.md` 维护长期精华

这一层也不依赖 skill。

### 第三层：继承 Codex 增强能力

这一层才和 skill 有关。

如果对方也用 Codex，安装 `pm-agent-os` skill 后，Codex 会更自然地：

- 按固定顺序读上下文
- 按 PM 角色路由任务
- 输出固定结构
- 在收尾时提醒或执行回写

## 路径 A：对方也是 Codex 用户

推荐路径如下：

1. 克隆这个仓库
2. 填自己的状态文件
3. 可选：安装 `pm-agent-os` skill
4. 重启 Codex
5. 开始使用 `resume / close`

### 必填文件

- `~/.codex/memories/memory.md`
- `context/team-context.md`
- `context/history-highlights.md`

### 日常最常用命令

开始工作：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode resume --copy
```

结束工作：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode close --copy
```

### skill 是不是必须

不是必须。

不装 skill：

- 一样能用这套方法
- 主要靠仓库、脚本和上下文文件

装了 skill：

- Codex 会更接近“原生按这套规则工作”

## 路径 B：对方不是 Codex 用户

如果对方主要用 Claude、Kimi、千问、GPT：

1. 克隆这个仓库
2. 填自己的状态文件
3. 不需要安装 skill
4. 直接用 `pm_prompt.py`
5. 切平台时把恢复提示词贴进去

### 关键区别

- 这些平台当前 baseline 默认不能直接读取本机文件
- 它们靠的是“嵌入式上下文包”
- 所以它们继承的是你贴进去的压缩状态，不是自动读盘

## 所有人都要遵守的规则

### 本地保留

这些 live 文件应该保留在本地，不直接提交：

- `~/.codex/memories/memory.md`
- `context/team-context.md`
- `context/history-highlights.md`
- `handoffs/current.md`
- `tasks/active/current.md`

### 可以提交到 Git

- 文档
- 模板
- 脚本
- `.example` 文件
- skill 定义

## 最简单的继承方式

如果你要把这套东西交给另一个同事，最简单的做法不是先讲原理，而是直接让他做下面 3 步：

1. 看 [最小白快速开始](quick-start.zh-CN.md)
2. 填自己的 `memory.md` 和 `team-context.md`
3. 按平台运行 `resume` 命令

## 一句话总结

- `仓库` 继承方法论和工作流
- `脚本` 继承恢复/收尾动作
- `skill` 只增强 Codex，不是所有人的前提
