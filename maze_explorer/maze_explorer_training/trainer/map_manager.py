import pickle
import os
import gzip

from google.cloud import storage

class MapManager:
    def __init__(self, bucket_name, bucket_path, client=None):
        self.bucket_name = bucket_name
        self.bucket_path = bucket_path
        self.client = client

        self.bucket = self.client.get_bucket(self.bucket_name)

        self.n_maps = len(self.bucket.list_blobs(prefix="map_"))

        self.current_map_index = 0

        print("Found maps:", self.n_maps)

    def unpickle_map(file_path):
        with open(file_path, "rb") as map_file:
            map = pickle.load(map_file)
            return map
    
    def get_map(self, map_name):
        map_blob = self.bucket.blob(self.bucket_path + map_name)
        map_blob.download_to_filename(map_name)
        gzip.decompress()
        map = MapManager.unpickle_map(map_name)
        os.remove(map_name)
        return map
    # Prints the grid
    def print_grid(self, grid):
        for row in grid:
            for val in row:
                print(val.get_string(), end="")
            
            print("\n", end="")

    def print_map(self, file):
        with open(file, "rb") as map_file:
            map, map_data = pickle.load(map_file)
            self.print_grid(map)
            print(map_data)
    
    def get_next_map(self):
        if self.current_map_index == self.n_maps:
            self.current_map_index = 0
        map_name = "map_" + str(self.current_map_index) + ".map"
        map = self.get_map(map_name)
        self.current_map_index += 1
        return map

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_dir + '/composed-arch-348513-69f529adb730.json'
    client = storage.Client()
    my_manager = MapManager("map_dataset", "gs://map_dataset", client)
    map = my_manager.get_next_map()


    