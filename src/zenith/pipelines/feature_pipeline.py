from zenith.scripts import load, process
from omegaconf import DictConfig


class FeaturePipeline:
    def __init__(self, config: DictConfig = None):
        self.config = config

    def execute(self):
        print("Feature Pipeline Started >")
        process.features_(self.config, load.from_supabase(self.config))
