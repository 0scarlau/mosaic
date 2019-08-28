import os
import sys
sys.path.append(os.getcwd())
from src.utils.image import TileImages, TargetImage, MosaicImage
from src.config.config import MosaicConfig
import time
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collecting inputs to create Mosaic Images')
    parser.add_argument('--target-path', help='Specify target path for target image', required=False)
    parser.add_argument('--target-image', help='Specify target image filename', required=True)
    parser.add_argument('--grid-size', type=int, nargs='+', help='Specify grid size', required=False)
    parser.add_argument('--tile-path', help='Specify Tile image path', required=False)
    parser.add_argument('--tile-folder', help='Specify Tile folder name', required=False)
    parser.add_argument('--mosaic-image', help='Specify Mosaic image output filename', required=False)
    parser.add_argument('--resize', type=int, nargs='+', help='Specify Mosaic image output filename', required=False)

    args = parser.parse_args()
    target_path = args.target_path
    target_image = args.target_image
    grid_size = args.grid_size
    tile_path = args.tile_path
    tile_folder = args.tile_folder
    save = args.mosaic_image
    resize = args.resize
    start_time = time.time()
    config = MosaicConfig()

    target = TargetImage(grid_size=grid_size, target_path=target_path, config=config)
    tile_image = TileImages(tile_path=tile_path, config=config, resize=resize, folder=tile_folder)
    target_image = target.get_target_image(target_image)
    input_images = tile_image.tiles
    cropped_images = target.target_image_split()
    tile_fit = tile_image.get_tile_fit(cropped_images, reuse=True)
    mosaic = MosaicImage(tile_images=tile_fit, grid_size=target.grid_size)
    mosaic_image = mosaic.build_mosaic()
    mosaic.save(mosaic_image, save)

    finish_time = time.time()
    print(f'Time of processing: {round(finish_time - start_time)} seconds')
