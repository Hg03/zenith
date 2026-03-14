from omegaconf import DictConfig
import polars as pl


def save_assets(to_save, path: str, mode: str) -> None:
    if mode == "parquet":
        to_save.write_parquet(path)


def load_assets(config: DictConfig, path: str, mode: str):
    if mode == "parquet":
        return pl.read_parquet(path)
