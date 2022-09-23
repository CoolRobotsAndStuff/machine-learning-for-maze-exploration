import pickle
from random_map_generator import generate_map, print_grid
import math
import os
current_dir = os.getcwd()


def generate_maps(num_maps):
    """
    Generates a set of maps for the maze explorer.
    :param num_maps: The number of maps to generate.
    """
    for i in range(num_maps):
        map = generate_map(visualize=False)
        with open(current_dir + '/maze_explorer/small_maps/map_' + str(i) + ".map", 'wb') as map_file:
            pickle.dump(map, map_file)
        print("Generated " + str(i) + " / " + str(num_maps - 1) + "  -  " + str(round(i/(num_maps - 1)*100)) + "%")

def print_map(file):
        with open(file, "rb") as map_file:
            map, map_data = pickle.load(map_file)
            print_grid(map)

def load_map(file_path):
    with open(file_path, "rb") as map_file:
        map = pickle.load(map_file)
        return map

if __name__ == "__main__":

    #generate_maps(1000)

    print_map(current_dir + "/maze_explorer/small_maps/map_0.map")


    