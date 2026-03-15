from zenith.scripts.utils import load_assets
from zenith.scripts import process, model


class InferencePipeline:
    def __init__(self):
        model_dir = "artifacts/models/model.skops"
        preprocessor_dir = "artifacts/preprocessor/preprocessor.skops"
        self.model = load_assets(model_dir, "model")
        self.preprocessor = load_assets(preprocessor_dir, "model")

    def execute(self, PredictionInput: dict):
        print("Inference Pipeline Started >")
        processed_PredictionInput, full_prediction_sample = process.prediction_input(
            PredictionInput
        )
        predictions = model.predict_with_loaded_model(
            processed_PredictionInput, self.preprocessor, self.model
        )
        return predictions
