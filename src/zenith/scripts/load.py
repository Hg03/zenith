from zenith.scripts.utils import save_assets
from supabase import create_client
from omegaconf import DictConfig
from dotenv import load_dotenv
from tqdm import tqdm
import polars as pl
import os


def format_dataframe(df: pl.DataFrame, target_col: str):
    col_map = {col.lower(): col for col in df.columns}
    df = df.rename(col_map)
    df = df.filter(pl.col(target_col).is_not_null())
    return df


def from_supabase(config: DictConfig) -> pl.DataFrame:
    load_dotenv()
    raw_data_path = config.path.raw_data
    conn = create_client(
        supabase_url=os.getenv("SUPABASE_URL"), supabase_key=os.getenv("SUPABASE_KEY")
    )
    json_data = []
    batch_size, offset = config.process.batch_size, config.process.offset
    total_rows = (
        conn.table(config.process.raw_data_table_name)
        .select("count", count="exact")
        .execute()
        .count
    )
    # Create progress bar
    progress_bar = tqdm(
        total=total_rows, desc="Loading data from Supabase", unit=" rows"
    )
    while True:
        response = (
            conn.table(config.process.raw_data_table_name)
            .select("*")
            .limit(batch_size)
            .offset(offset)
            .execute()
        )
        batch = response.data
        if not batch:
            break
        json_data.extend(batch)
        offset += batch_size
        progress_bar.update(len(batch))
    progress_bar.close()
    raw_data = pl.DataFrame(json_data)
    df = format_dataframe(df=raw_data, target_col=config.attrs.target)
    save_assets(to_save=df, path=raw_data_path, mode="parquet")
    print("Loading Completed")
    return df


def to_supabase(config: DictConfig):
    print("Pushing Data from Supabase")
