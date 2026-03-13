# Zenith ML System

## How I did setup

- `uv init --package zenith`
- Added required folder and initial code.
- Added required tools to format, lint and pre-commit. For tooling, I did the next point
- `uv add prek ruff rust-just ty --dev`
- `prek install` : Install git hook
- Then used `hydra-core` and `omegaconf` for configuration management. `uv add hydra-core omegaconf`.
