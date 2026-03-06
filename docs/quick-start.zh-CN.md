# PM Agent OS 最小白快速开始

这份文档只讲“怎么用”，不讲原理。

如果你完全不想思考，照着下面做就行。

## 你只需要记住两件事

1. 开始工作前，运行一条命令，复制恢复提示词
2. 结束工作前，运行一条命令，复制收尾提示词

然后把它粘贴到对应的 AI 里。

## 第一次使用

第一次只做这两件事：

1. 打开并填写你的个人记忆文件  
文件位置：
`/Users/wamg/.codex/memories/memory.md`

不会写时，直接参考这个中文模板：
[个人记忆中文模板](../templates/personal-memory.zh-CN.template.md)

2. 打开并填写你当前 team 的信息  
文件位置：
`/Users/wamg/Documents/monthly/context/team-context.md`

不会写时，直接参考这个中文模板：
[team 上下文中文模板](../templates/team-context.zh-CN.template.md)

不用写很复杂，先随便写个最小版本也可以。

补充：

如果你希望“新对话也知道我们历史上聊过什么”，后面请持续维护这个文件：
`/Users/wamg/Documents/monthly/context/history-highlights.md`

不会写时，直接参考这个中文模板：
[历史精华中文模板](../templates/history-highlights.zh-CN.template.md)

## 每天开始工作

### 如果你在 Codex 里继续

在终端执行：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode resume --copy
```

然后：

1. 打开 Codex
2. 粘贴
3. 回车

### 如果你切到 Kimi

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform kimi --mode resume --copy
```

然后打开 Kimi，直接粘贴。

### 如果你切到 Claude

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform claude --mode resume --copy
```

然后打开 Claude，直接粘贴。

### 如果你切到千问

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform qwen --mode resume --copy
```

然后打开千问，直接粘贴。

### 如果你切到 GPT

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform gpt --mode resume --copy
```

然后打开 GPT，直接粘贴。

## 每天结束工作

### 最推荐的方式

在 Codex 里收尾，因为它更适合更新本地文件。

在终端执行：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode close --copy
```

然后：

1. 打开 Codex
2. 粘贴
3. 回车

它会帮你整理这次工作做到哪了、下一步是什么、有哪些风险。
如果本次形成了长期有价值的结论，也应该同步更新历史精华。

## 如果你换了 team

你只需要做一件事：

更新这个文件：

`/Users/wamg/Documents/monthly/context/team-context.md`

然后再执行你要使用的平台恢复命令。

也就是说：

- 换 team，不需要重建整个系统
- 只需要换 team 信息
- 然后重新恢复一次

## 如果你换了模型

你不用手工找文件，也不用手工导出。
也不需要先安装 Git skill。

只需要换一条命令：

- Codex：`./scripts/pm_prompt.py --platform codex --mode resume --copy`
- Kimi：`./scripts/pm_prompt.py --platform kimi --mode resume --copy`
- Claude：`./scripts/pm_prompt.py --platform claude --mode resume --copy`
- 千问：`./scripts/pm_prompt.py --platform qwen --mode resume --copy`
- GPT：`./scripts/pm_prompt.py --platform gpt --mode resume --copy`

脚本会自动帮你生成适合那个模型的提示词，并复制到剪贴板。

## 平台读取方式速记

这是最容易搞混的一点，只记这 3 句就够了：

- `Codex`
  - 通常能直接读取本地文件
  - 适合走“文件读取版”恢复
  - 也最适合做 `close` 收尾和本地回写

- `Claude / Kimi / 千问 / GPT 客户端或网页端`
  - 当前默认不能直接读取你电脑上的本地文件
  - 只能走“嵌入式上下文包”恢复
  - 它们能续接，是因为你贴入了压缩后的状态，不是因为它们自己会去读盘

- 如果你以后希望这些客户端也能直接读文件
  - 需要再接一层 wrapper、本地连接器或类似 MCP 的方案
  - 当前这版 baseline 还没做这一层

## 你最常用的两条命令

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

如果你只打算记两条，就记这两条。

## 最容易理解的一句话

这个系统不是让 AI 记住你所有聊天。

而是让 AI 每次都先看你的“工作档案”，然后再继续。

## 如果你懒得记

以后就按这个固定动作走：

1. 早上执行一条 `resume` 命令
2. 晚上执行一条 `close` 命令

就够了。

## 如果出问题

先检查这三件事：

1. `memory.md` 有没有内容
2. `team-context.md` 有没有内容
3. 你是不是执行了正确的平台命令

大多数问题都出在这里。
