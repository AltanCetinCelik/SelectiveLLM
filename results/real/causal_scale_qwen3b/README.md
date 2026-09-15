# Qwen2.5-3B Scale-Replication Results

This directory contains real Qwen2.5-3B-Instruct measurements using logical
inference-time ablation of contiguous MLP blocks. No weights are unloaded and no
VRAM reduction is measured or claimed.

`latest/` is published only by a complete run from a clean committed worktree.

The GitHub-friendly `latest/` directory includes the reports, row-level evidence,
masks, rankings, and raw/normalized block scores. The manifest also hashes two
large channel-level tensor archives and three resumable progress files retained
in the local timestamped canonical run. Those five files are intentionally not
tracked; the largest exceeds GitHub's ordinary per-file limit. Their absence from
the compact publication subset does not change the completed result.
