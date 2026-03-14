from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from omegaconf import DictConfig
from skrub import Cleaner, TableVectorizer
import polars as pl


def features_(config: DictConfig, raw_data: pl.DataFrame) -> pl.DataFrame:
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
    processed_data = {
        "X_train": processed_X_train,
        "X_test": processed_X_test,
        "y_train": y_train,
        "y_test": y_test,
    }
    print(f"Content of processed: {processed_data.keys()}")
