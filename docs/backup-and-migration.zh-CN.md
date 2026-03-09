# 备份与迁移

这页只讲一件事：如果你突然被移出 workspace、母号出问题、换设备，怎么把 PM Agent OS 的状态带走并恢复。

## 当前实现状态

- 手动快照：已实现
- 本地恢复：已实现
- 换设备迁移：已实现，但你需要把快照目录同步到私有位置
- 自动定时备份：未默认开启
- 自动收尾回写：仍建议先跑一次 `close`

一句话说：现在已经有“备份”和“恢复”，但“每天自动备份”还需要你再接一层 automation 或系统定时任务。

## 先记住最短流程

离开当前 workspace、换设备或担心账号风险前，执行这两步：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode close --copy
./scripts/snapshot_state.py
```

上面两步分别解决：

1. 先把最新状态写进 `handoff / history-highlights / team-context / memory`
2. 再把这些 live state 文件打成一个快照

## 它会备份哪些文件

默认会打包这 5 个 live state 文件：

- `~/.codex/memories/memory.md`
- `context/team-context.md`
- `context/history-highlights.md`
- `handoffs/current.md`
- `tasks/active/current.md`

快照默认放在本地：

`/Users/wamg/Documents/monthly/state-backups/`

并自动更新一个：

`/Users/wamg/Documents/monthly/state-backups/latest`

## 如何创建快照

最简单就是这一条：

```bash
cd /Users/wamg/Documents/monthly
./scripts/snapshot_state.py
```

如果你想给这次备份加标签：

```bash
./scripts/snapshot_state.py --label before-device-switch
```

如果你想直接备份到私有同步目录：

```bash
./scripts/snapshot_state.py --output-root ~/Documents/private-pm-backups
```

## 如何恢复

### 恢复到当前仓库

```bash
cd /Users/wamg/Documents/monthly
./scripts/restore_state.py --snapshot state-backups/latest
```

### 先看一眼会恢复什么

```bash
./scripts/restore_state.py --snapshot state-backups/latest --dry-run
```

### 恢复到另一个 workspace

```bash
./scripts/restore_state.py \
  --snapshot /path/to/state-backups/latest \
  --workspace /path/to/new/workspace
```

这个命令适合：

- 换电脑后恢复到新的仓库目录
- 需要把原项目状态迁移到新的本地 workspace

## 换设备时怎么做

最稳的流程是：

1. 在旧设备跑一次 `close`
2. 跑一次 `snapshot_state.py`
3. 把 `state-backups/` 同步到私有位置
4. 在新设备拉下仓库
5. 把快照目录拿到新设备
6. 跑 `restore_state.py`
7. 再跑一次 `resume`

## 换 team 空间时怎么做

如果你只是换了平台里的 team 空间，但还是同一台机器：

- 原项目 live state 还在本机
- 最稳做法仍然是先生成 `resume` 提示词，再贴到新空间的新线程

也就是说：

- `snapshot / restore` 解决的是防丢状态、换设备、跨目录迁移
- `resume prompt` 解决的是换线程、换模型、换平台继续执行

## 目前还没默认自动化的部分

现在默认还没有：

- 每天自动跑 `close`
- 每天自动跑 `snapshot`
- 自动把快照推到私有 Git 仓库或云盘

这些都可以再接一层 automation，但当前 baseline 没有后台自动任务。

## 建议你现在就采用的最低成本动作

如果你只想先把风险降下来，记住这两条就够了：

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode close --copy
./scripts/snapshot_state.py
```

这样至少可以把“被踢出 workspace / 换设备 / 本地误删”的风险压低很多。
