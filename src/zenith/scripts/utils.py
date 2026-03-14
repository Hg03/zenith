from skops.io import dump, load, get_untrusted_types
from omegaconf import DictConfig
import polars as pl


def save_assets(to_save, path: str, mode: str) -> None:
    if mode == "parquet":
        to_save.write_parquet(path)
    if mode == "model":
        dump(to_save, path)


def load_assets(config: DictConfig, path: str, mode: str):
    if mode == "parquet":
        return pl.read_parquet(path)
    if mode == "model":
        unknown_types = get_untrusted_types(file=path)
        return load(path, unknown_types)
