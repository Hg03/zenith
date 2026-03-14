from zenith.scripts import model


class TrainingPipeline:
    def __init__(self, config=None):
        self.config = config

    def execute(self):
        print("Training Pipeline Started >")
        model.train(self.config)
