# Zenith ML System

## How I did setup

- Firstly, if you don't want the barebone step. Just clone the repo, build the docker container and attach your visual studio code. If interested to build it from initial stages. Get to the next point.
- Keep `uv` installed as a prerequisite.
- `uv init --package zenith`
- Added required folder and initial code.
- Added required tools to format, lint and pre-commit. For tooling, I did the next point
- `uv add prek ruff rust-just ty --dev`
- `prek install` : Install git hook
- Review the [prek.toml](https://github.com/Hg03/zenith/blob/main/prek.toml) which is doing ruff check and format on every git commits.
- Then used `hydra-core` and `omegaconf` for configuration management. `uv add hydra-core omegaconf`.
