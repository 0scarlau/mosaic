import os
import yaml
from yaml.error import YAMLError
from yaml.loader import SafeLoader
from pathlib import Path


class MosaicConfig:

    def __init__(self):
        self.config = None
        self.tile_path = None
        self.tile_folder = None
        self.target_path = None
        self.width = None
        self.height = None
        self.grid_size = None
        self.load_config(self.get_config_path())

    def load_config(self, config):

        if isinstance(config, str):
            with open(config, 'r') as stream:
                try:
                    self.config = yaml.load(stream, Loader=SafeLoader)
                except YAMLError as ex:
                    print(ex)
        else:
            self.config = config

        for key, values in self.config.items():
            for value in values:
                if 'image' in key:
                    setattr(self, value, self.config[key][value])

        self.grid_size = self.width, self.height

    def get_config_path(self):
        return os.path.join(Path(os.getcwd()), "config/config.yaml")