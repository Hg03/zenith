from omegaconf import DictConfig


def train(config: DictConfig):
    print("Training Model")
    experiment(config, assets={})


def experiment(config: DictConfig, assets):
    print("Logging Experiment")
