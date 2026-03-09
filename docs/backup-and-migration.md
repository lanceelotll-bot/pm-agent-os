# Backup and migration

This page covers one thing: how to keep PM Agent OS portable if you lose workspace access, switch devices, or need to restore the latest live state.

## Current status

- Manual snapshots: implemented
- Local restore: implemented
- Device migration: implemented, as long as you sync the snapshot directory somewhere private
- Scheduled backups: not enabled by default
- Automatic close/writeback: still best handled by running `close` first

In short: backup and restore now exist, but daily unattended backup is still a separate automation layer.

## Minimum safe flow

Before leaving a workspace, switching devices, or when account risk matters, run:

```bash
cd /Users/wamg/Documents/monthly
./scripts/pm_prompt.py --platform codex --mode close --copy
./scripts/snapshot_state.py
```

The first command writes the latest durable state back to your local files.
The second command snapshots those live state files.

## What gets backed up

The snapshot includes these live files:

- `~/.codex/memories/memory.md`
- `context/team-context.md`
- `context/history-highlights.md`
- `handoffs/current.md`
- `tasks/active/current.md`

By default, snapshots live under:

`/Users/wamg/Documents/monthly/state-backups/`

The script also refreshes:

`/Users/wamg/Documents/monthly/state-backups/latest`

## Create a snapshot

```bash
cd /Users/wamg/Documents/monthly
./scripts/snapshot_state.py
```

Optional label:

```bash
./scripts/snapshot_state.py --label before-device-switch
```

Optional private backup root:

```bash
./scripts/snapshot_state.py --output-root ~/Documents/private-pm-backups
```

## Restore a snapshot

Restore into the current repo:

```bash
cd /Users/wamg/Documents/monthly
./scripts/restore_state.py --snapshot state-backups/latest
```

Preview without writing:

```bash
./scripts/restore_state.py --snapshot state-backups/latest --dry-run
```

Restore into another workspace:

```bash
./scripts/restore_state.py \
  --snapshot /path/to/state-backups/latest \
  --workspace /path/to/new/workspace
```

## Device-switch flow

The safest sequence is:

1. Run `close` on the old device.
2. Run `snapshot_state.py`.
3. Sync `state-backups/` to a private location.
4. Clone the repo on the new device.
5. Bring the snapshot directory over.
6. Run `restore_state.py`.
7. Run `resume`.

## Workspace switch vs restore

Use the right tool for the right problem:

- `snapshot / restore` is for state protection, device switches, and cross-directory migration.
- `resume prompt` is for switching threads, platforms, or team spaces and continuing work.

## Not automated yet

The current baseline still does not do these automatically:

- daily `close`
- daily `snapshot`
- automatic push to a private Git repo or cloud drive

Those are natural next steps, but they are not enabled by default yet.
