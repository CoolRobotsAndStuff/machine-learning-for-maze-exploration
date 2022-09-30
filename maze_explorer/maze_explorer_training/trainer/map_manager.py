import pickle
import os
import sys

from google.cloud import storage

try:
    import trainer.random_map_generator as random_map_generator
except:
    import random_map_generator


sys.path.append(os.path.join(os.path.dirname(__file__)))

current_dir = os.path.dirname(__file__)

class MapManager:
    def __init__(self, bucket_path, client=None):
        self.bucket_name = bucket_path.split("/")[-1]
        print(self.bucket_name)
        self.bucket_path = bucket_path
        self.client = client

        self.bucket = self.client.bucket(self.bucket_name)

        assert self.bucket.get_blob("map_0.map") is not None, "No maps found in bucket"

        self.current_map_index = 0

    def generate_maps(self, num_maps):
        """
        Generates a set of maps for the maze explorer.
        :param num_maps: The number of maps to generate.
        """
        for i in range(num_maps):
            map = random_map_generator.generate_map(visualize=False)
            with open(current_dir + '/small_maps/map_' + str(i) + ".map", 'wb') as map_file:
                pickle.dump(map, map_file)
            print("Generated " + str(i) + " / " + str(num_maps - 1) + "  -  " + str(round(i/(num_maps - 1)*100)) + "%")

    def unpickle_map(self, file_path):
        with open(file_path, "rb") as map_file:
            unpickled_map = pickle.load(map_file)
            return unpickled_map
    
    def get_map(self, map_name):
        """
        map_blob = self.bucket.get_blob(map_name)
        if map_blob is None:
            return None
        pickled_map = map_blob.download_as_bytes()
        """
        try:
            with open("trainer/small_maps/"+ map_name, "rb") as pickled_map:
                unpickled_map = pickle.load(pickled_map) 
        except:
            unpickled_map = None
        return unpickled_map

    # Prints the grid
    def print_grid(self, grid):
        for row in grid:
            for val in row:
                print(val.get_string(), end="")
            
            print("\n", end="")

    def print_map(self, map):
        map, map_data = pickle.loads(map)
        self.print_grid(map)
        print(map_data)
    
    def get_next_map(self):
        #map_name = "map_" + str(self.current_map_index) + ".map"
        map_name = "map_7.map"
        map = self.get_map(map_name)
        if map is None:
            self.current_map_index = 0
            map_name = "map_" + str(self.current_map_index) + ".map"
            map = self.get_map(map_name)
        self.current_map_index += 1
        return map

if __name__ == "__main__":
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_dir + '/composed-arch-348513-69f529adb730.json'
    client = storage.Client()
    my_manager = MapManager("gs://map_dataset", client=client)
    map, map_data = my_manager.get_map("map_56787.map")
    my_manager.print_grid(map)
    print(map_data)
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_dir + '/composed-arch-348513-69f529adb730.json'
    client = storage.Client()
    my_manager = MapManager("gs://map_dataset", client=client)
    for i in range(10):
        mm = my_manager.get_map("map_" + str(i) + ".map")
        my_manager.print_grid(mm[0])
