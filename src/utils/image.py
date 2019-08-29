import os
from PIL import Image
from src.utils.processor import get_average_rgb, best_match_tile_images, progress_bar
from src.config.config import MosaicConfig
import random


"""
TargetImage Class 
Used to open up the target image by specifying the target path (default path is /images/target) and the image
filename in that path. Image file should be in .jpg or .jpeg format. 
Configuration will be loaded automatically, however variables can be overwritten 
"""


class TargetImage:
    def __init__(self, target_path=None, grid_size=None, config=MosaicConfig()):
        self.image = None
        if config:
            self.config = config
            self.target_path = os.path.join(os.getcwd(), self.config.target_path)
            self.grid_size = self.config.grid_size
        if grid_size:
            self.grid_size = grid_size
        if target_path:
            self.target_path = target_path

    def get_target_image(self, filename):
        print(f'Processing target image with filename: {filename}')
        try:
            file = os.path.join(self.target_path, filename)
            self.image = Image.open(file)
            return self.image
        except FileNotFoundError:
            print(f'{filename} does not exist in path {self.target_path}')

    def target_image_split(self):
        """
        Image will split into the grid size provided in the class. Default [50,50]
        Size of the split tile image will be calculated and used to crop the existing target image to form
        new tiles images. The cropped target images will be appended into an array and returned
        """

        print(f'Splitting target image into tiles')
        images = []
        target_image_width = self.image.size[0]
        target_image_height = self.image.size[1]
        larger_image = self.image.resize((target_image_width, target_image_height))
        number_of_columns, number_of_rows = self.grid_size
        column_size, row_size = int(target_image_width / number_of_columns), int(target_image_height / number_of_rows)

        # im.crop(box) left, upper, right, and lower
        for j in range(number_of_columns):
            for i in range(number_of_rows):
                images.append(larger_image.crop((i * column_size,
                                                 j * row_size,
                                                 (i + 1) * column_size,
                                                 (j + 1) * row_size))
                              )
        print(f'Total number of tiles from splitted target image: {len(images)}')
        return images

"""
TileImage class opens up all the input tile images placed in the tile path (default path is /images/tile) 
If using the default path, the class must take in the folder name where the tile images are located or
the direct tile path can be loaded.

The input tile images will vary in size, and the resize variable can increase or decrease the input tile images
before processing. The greater the size of the input tile images, the greater the size of the file will be
If resize parameter is not used, the default input tile image size will be used for processing
"""


class TileImages:
    def __init__(self, tile_path=None, config=MosaicConfig(), resize=None, folder=None):
        self.tiles = list()
        self.resize = resize

        if config:
            self.config = config
            if folder:
                self.tile_path = os.path.join(os.getcwd(), self.config.tile_folder, folder)
            else:
                self.tile_path = os.path.join(os.getcwd(), self.config.tile_path)
            self.tiles = self.prepare_tile_images(self.tile_path)
        if tile_path:
            self.tiles = self.prepare_tile_images(tile_path)

    def _process_tile(self, tile_path):
        try:
            image = Image.open(tile_path)
            if self.resize:
                image.thumbnail((self.resize[0], self.resize[1]))
            return image
        except Exception as ex:
            pass

    # def _build_white_tile(self):
    #     white_image = Image.new('RGB', (self.resize[0], self.resize[1]), (255, 255, 255))
    #     return white_image

    def prepare_tile_images(self, tile_path):
        print(f'Reading tile images from path: {tile_path}\n')
        # self.tiles.append(self._build_white_tile())
        try:
            tile_paths = os.listdir(tile_path)
            random.shuffle(tile_paths)
            for path in tile_paths:
                if '.jpg' in path or '.jpeg' in path:
                    file_path = os.path.abspath(os.path.join(tile_path, path))
                    self.tiles.append(self._process_tile(file_path))
        except FileNotFoundError:
            print(f'{tile_path} does not contain any image files\n')
        return self.tiles

    @staticmethod
    def tile_average_rgb(tile_images: list) -> list:
        averages = list()
        for image in tile_images:
            averages.append(get_average_rgb(image))
        return averages

    def get_tile_fit(self, split_images, reuse=True) -> list:

        """
        Averages of each split images and input tile images are calculated and the best fit for each split image
        will be calculated using euclidean distance formula. The distance formula will return the index of the input
        tile images that best fits the split images.

        Function returns the input tile images in an array in the order of fitting
        """
        indices = list()
        tile_fit = list()

        print(f'Total number of tile images to process: {len(split_images)}\n')
        split_image_average_rgb = self.tile_average_rgb(split_images)
        tile_image_average_rgb = self.tile_average_rgb(self.tiles)

        print(f'Finding Tiles of best fit\n')
        for progress, average in enumerate(split_image_average_rgb):
            i = best_match_tile_images(average, tile_image_average_rgb)
            indices.append(i)
            if not reuse:
                del tile_image_average_rgb[i]

            if len(tile_image_average_rgb) == 0:
                raise Exception('No tiles images left to process')

            progress_bar(progress, len(split_image_average_rgb))

        print(f'Preparing tile indices\n')
        for process, index in enumerate(indices):
            tile_fit.append(self.tiles[index])
            progress_bar(process, len(indices))

        return tile_fit

"""
MosaicImage class takes the tile images and populates it into a Mosaic image 
"""


class MosaicImage:
    def __init__(self, tile_images: list, grid_size):
        self.tiles = tile_images
        self.grid_size = grid_size

    def build_mosaic(self) -> Image:
        number_of_columns, number_of_rows = self.grid_size

        width = max([tile.size[0] for tile in self.tiles])
        height = max([tile.size[1] for tile in self.tiles])
        grid_image = Image.new('RGB', (width * number_of_columns, height * number_of_rows))

        print(f'Pasting tile of best fit images')
        for i in range(len(self.tiles)):
            row_number = int(i / number_of_rows)
            column_number = i - number_of_columns * row_number
            grid_image.paste(self.tiles[i], (column_number * width, row_number * height))
            progress_bar(i, len(self.tiles))

        return grid_image

    @staticmethod
    def save(image, filename=None):
        path = os.path.join(os.getcwd(), 'output')
        if not os.path.exists(path):
            os.mkdir(path)

        if filename is not None:
            saved_path = os.path.join(os.getcwd(), 'output/', filename + '.jpg')
        else:
            saved_path = os.path.join(os.getcwd(), 'output/mosaic.jpg')
        image.save(saved_path)
        print(f'File has been saved at {saved_path}')