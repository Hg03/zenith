from zenith.pipelines import feature_pipeline, training_pipeline
from omegaconf import DictConfig
import hydra


@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg: DictConfig):
    if cfg.steps.pipeline == "feature":
        feature_pipeline.FeaturePipeline(config=cfg).execute()
    elif cfg.steps.pipeline == "training":
        training_pipeline.TrainingPipeline(config=cfg).execute()
    else:
        feature_pipeline.FeaturePipeline(config=cfg).execute()
        training_pipeline.TrainingPipeline(config=cfg).execute()


if __name__ == "__main__":
    main()
