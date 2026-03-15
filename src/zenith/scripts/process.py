from sklearn.model_selection import train_test_split
from zenith.scripts.utils import save_assets, load_assets
from skrub import Cleaner, TableVectorizer
from sklearn.pipeline import Pipeline
from omegaconf import DictConfig
from datetime import datetime
import polars as pl


def features_(config: DictConfig, raw_data: pl.DataFrame) -> pl.DataFrame:
    print("Preprocessing Data")
    X, y = raw_data.select(config.attrs.features), raw_data.select(config.attrs.target)
    y = y.with_columns(
        pl.col(config.attrs.target[0])
        .replace(config.process.strategies.encoding_map)
        .alias(config.attrs.target[0])
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.process.test_size, stratify=y
    )
    preprocessor = Pipeline(
        steps=[("Cleaner", Cleaner()), ("Vectorizer", TableVectorizer())]
    ).set_output(transform="polars")
    processed_X_train = preprocessor.fit_transform(X_train)
    processed_X_test = preprocessor.transform(X_test)
    save_assets(processed_X_train, config.path.processed_X_train, "parquet")
    save_assets(processed_X_test, config.path.processed_X_test, "parquet")
    save_assets(y_train, config.path.processed_y_train, "parquet")
    save_assets(y_test, config.path.processed_y_test, "parquet")
    save_assets(preprocessor, config.path.preprocessor, "model")


def prediction_input(input_: dict) -> pl.DataFrame:
    raw_data = load_assets("data/raw/raw_data.parquet", "parquet")
    top_id = raw_data.select(pl.col("id")).max()
    full_prediction_sample = {
        "id": top_id + 1,
        "date": datetime.now(),
        "created_at": datetime.now(),
    }
    full_prediction_sample = {**full_prediction_sample, **input_}
    processed_input_ = {k: v for k, v in input_.items() if k != "person_name"}
    return processed_input_, full_prediction_sample
