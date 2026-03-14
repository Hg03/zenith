from sklearn.ensemble import HistGradientBoostingClassifier
from zenith.scripts.utils import load_assets, save_assets
from sklearn.metrics import classification_report
from omegaconf import DictConfig


def train(config: DictConfig):
    print("Training Model")
    X_train, X_test, y_train, y_test = (
        load_assets(config=config, path=config.path.processed_X_train, mode="parquet"),
        load_assets(config=config, path=config.path.processed_X_test, mode="parquet"),
        load_assets(config=config, path=config.path.processed_y_train, mode="parquet"),
        load_assets(config=config, path=config.path.processed_y_test, mode="parquet"),
    )
    model = HistGradientBoostingClassifier()
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    save_assets(model, config.path.model, mode="model")
    experiment(
        config,
        assets={
            "model": model,
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "train_preds": train_predictions,
            "test_preds": test_predictions,
        },
    )


def experiment(config: DictConfig, assets):
    print("Logging Experiment")
    print(
        classification_report(
            assets["y_train"],
            assets["train_preds"],
            target_names=list(config.process.strategies.encoding_map.keys()),
        )
    )
