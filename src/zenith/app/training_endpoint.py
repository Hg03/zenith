from zenith.pipelines import feature_pipeline, training_pipeline


def main():
    feature_pipeline.FeaturePipeline().execute()
    training_pipeline.TrainingPipeline().execute()


if __name__ == "__main__":
    main()
