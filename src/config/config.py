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

        if 'image' in self.config:
            self.tile_path = self.config.get('image').get('tile')
            self.target_path = self.config.get('image').get('target')
            self.width = self.config.get('image').get('width')
            self.height = self.config.get('image').get('height')
            self.tile_folder = self.config.get('image').get('folder')

        self.grid_size = self.width, self.height

    def get_config_path(self):
        return os.path.join(Path(os.getcwd()), "config/config.yaml")
