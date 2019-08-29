import numpy as np
import random

def get_average_rgb(image):
    im = np.array(image)
    width, height, dimension = im.shape
    return tuple(np.average(im.reshape(width * height, dimension), axis=0))

def euclidean_distance(x1: list, x2: list):
    distance = 0
    if len(x1) != len(x2):
        raise Exception('Two arrays do not have identical lengths')
    else:
        for i in range(len(x1)):
            distance = distance + (x1[i] - x2[i]) ** 2
        return distance

def best_match_tile_images(target_tile_rgb_average:list, tile_rgb_averages:list) -> int:
    min_dist = float("inf")
    best_fit_index = 0

    for index, average in enumerate(tile_rgb_averages):
        dist = euclidean_distance(target_tile_rgb_average, average)
        if dist < min_dist:
            if bool(random.getrandbits(1)):
                min_dist = dist
                best_fit_index = index
    return best_fit_index

def progress_bar(progress: int, len_of_array: int) -> None:
    if round(float(progress / len_of_array) * 100) == 0.0:
        print(f'[Start >                                                           Finish]')
    if round(float(progress / len_of_array) * 100) == 10.0:
        print(f'[Start ========>                                                   Finish]')
    if round(float(progress / len_of_array) * 100) == 20.0:
        print(f'[Start ==============>                                             Finish]')
    if round(float(progress / len_of_array) * 100) == 30.0:
        print(f'[Start ===================>                                        Finish]')
    if round(float(progress / len_of_array) * 100) == 40.0:
        print(f'[Start =========================>                                  Finish]')
    if round(float(progress / len_of_array) * 100) == 50.0:
        print(f'[Start ================================>                           Finish]')
    if round(float(progress / len_of_array) * 100) == 60.0:
        print(f'[Start =======================================>                    Finish]')
    if round(float(progress / len_of_array) * 100) == 70.0:
        print(f'[Start ==============================================>             Finish]')
    if round(float(progress / len_of_array) * 100) == 80.0:
        print(f'[Start =====================================================>      Finish]')
    if round(float(progress / len_of_array) * 100) == 90.0:
        print(f'[Start ===========================================================>Finish]')




