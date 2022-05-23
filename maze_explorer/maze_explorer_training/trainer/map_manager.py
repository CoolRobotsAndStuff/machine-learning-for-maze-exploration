import pickle
import os

from google.cloud import storage

class MapManager:
    def __init__(self, bucket_path, client=None):
        self.bucket_name = bucket_path.split("/")[-1]
        print(self.bucket_name)
        self.bucket_path = bucket_path
        self.client = client

        self.bucket = self.client.bucket(self.bucket_name)

        assert self.bucket.get_blob("map_0.map") is not None, "No maps found in bucket"

        self.current_map_index = 0

    def unpickle_map(file_path):
        with open(file_path, "rb") as map_file:
            unpickled_map = pickle.load(map_file)
            return unpickled_map
    
    def get_map(self, map_name):
        map_blob = self.bucket.get_blob(map_name)
        if map_blob is None:
            return None
        pickled_map = map_blob.download_as_bytes()
        return pickle.loads(pickled_map)

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
        map_name = "map_" + str(self.current_map_index) + ".map"
        map = self.get_map(map_name)
        if map is None:
            self.current_map_index = 0
            map_name = "map_" + str(self.current_map_index) + ".map"
            map = self.get_map(map_name)
        self.current_map_index += 1
        return map

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_dir + '/composed-arch-348513-69f529adb730.json'
    client = storage.Client()
    my_manager = MapManager("gs://map_dataset", client=client)
    for _ in range(10):
        map, map_data = my_manager.get_next_map()
        my_manager.print_grid(map)
        print(map_data)


    