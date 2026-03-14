from omegaconf import DictConfig
import polars as pl


def from_supabase(config: DictConfig) -> pl.DataFrame:
    print("Loading Data from Supabase")


def to_supabase(config: DictConfig):
    print("Pushing Data from Supabase")
