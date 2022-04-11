import random
from grid_maker import make_grid
import utils
import numpy as np
import copy



def get_random_vortex_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "vortex":
            return (x, y)

def get_random_tile_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "tile":
            return (x, y)

def get_random_wall_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "wall":
            return (x, y)
def zero_in_array(grid):
    for row in grid:
        for node in row:
            if node == 0:
                return True
    return False

def get_random_areas(n_areas, grid):
    area_grid_width = (len(grid[0]) - 1) // 4
    area_grid_height = (len(grid) - 1) // 4

    area_grid = np.zeros((area_grid_height, area_grid_width), dtype=int)
    new_area_grid = np.zeros((area_grid_height, area_grid_width), dtype=int)
    probs = {}
    
    for i in range(n_areas):
        prob = random.randint(0, 99) / 100
        starting_vortex = get_random_vortex_position(grid, include_edges=False)
        starting_vortex = (starting_vortex[1] // 4, starting_vortex[0] // 4)
        while area_grid[starting_vortex] != 0:
            starting_vortex = get_random_vortex_position(grid, include_edges=False)
            starting_vortex = (starting_vortex[1] // 4, starting_vortex[0] // 4)
        area_grid[starting_vortex] = i + 1
        new_area_grid[starting_vortex] = i + 1
        probs[i+1] = prob

    while zero_in_array(area_grid):
        for y, row in enumerate(area_grid):
            for x, node in enumerate(row):
                if node == 0:
                    neighbours = utils.get_adjacents((x, y), include_straight=True, include_diagonals=False)
                    for neighbour in neighbours:
                        neighbour = list(neighbour)
                        neighbour.reverse()
                        neighbour = tuple(neighbour)
                        if not(0 <= neighbour[0] < area_grid.shape[0] and 0 <= neighbour[1] < area_grid.shape[1]):
                            continue
                        if area_grid[neighbour] == 0:
                            continue
                        prob1 = random.randint(0, 100) / 100
                        if prob1 > probs[area_grid[neighbour]]:
                            continue
                        new_area_grid[(y, x)] = area_grid[neighbour]
                        break
        

        area_grid = copy.deepcopy(new_area_grid)
    print(area_grid)
    return area_grid

def check_areas(areas):
    counts = list()
    for i in range(3):
        counts.append(np.count_nonzero(areas == i+1))
    print(counts)
    for count in counts:
        if 0 < count < 4:
            return False 

    return True
    

def generate_areas(area_grid, grid):
    
    final_area_grid = np.zeros((len(grid), len(grid[0])), dtype=int)

    for y, row in enumerate(area_grid):
        for x, node in enumerate(row):
            x1 = x * 4 + 2
            y1 = y * 4 + 2
            final_area_grid[y1][x1] = node
            adjacents = utils.get_adjacents((x1, y1), include_straight=True, include_diagonals=True)
            for adjacent in adjacents:
                adjacent = list(adjacent)
                adjacent.reverse()
                adjacent = tuple(adjacent)
                if not(0 <= adjacent[0] < final_area_grid.shape[0] and 0 <= adjacent[1] < final_area_grid.shape[1]):
                    continue
                final_area_grid[adjacent] = node

    print(final_area_grid)
    return final_area_grid

def print_area_grid(grid):
    node_to_pixel = {
        1: "\033[1;35;47m██"+ "\033[0m",
        2: "\033[1;31;47m██"+ "\033[0m",
        3: "\033[1;33;47m██"+ "\033[0m",
        0: "  ",
    }
    for row in grid:
        for node in row:
            print(node_to_pixel[node], end="")
        print()

def fill_grid_borders(shape):
    for x in range(0, shape[1]):
        grid[0][x].status = "occupied"
        grid[-1][x].status = "occupied"
    for y in range(0, shape[0]):
        grid[y][0].status = "occupied"
        grid[y][-1].status = "occupied"

def fill_area_limits(grid, area_grid):
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if area_grid[y][x] != 0:
                continue
            adjacents = utils.get_adjacents((y, x), include_straight=True, include_diagonals=True)
            adj_values = []
            for adjacent in adjacents:
                if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                    continue
                adj_values.append(area_grid[adjacent])
            numbers = {1, 2, 3}
            
            for value in adj_values:
                if value in numbers:
                    numbers.remove(value)
                    for value in adj_values:
                        if value in numbers:
                            node.status = "occupied"

def print_grid(grid):
    for row in grid:
        for val in row:
            print(val.get_string(), end="")
        
        print("\n", end="")

def get_random_connections():
    n_connections = random.choice((2, 3))

    possible_connections = [{1, 2}, {1, 3}, {2, 3}]
    connections = copy.deepcopy(possible_connections)
    if n_connections == 2:
        del connections[random.randint(0, len(connections) - 1)]


size_x = random.randint(12, 32)
size_y = random.randint(12, 32)

while (size_x // 4) * (size_y // 4) < 6:
    size_x = random.randint(12, 32)
    size_y = random.randint(12, 32)

shape_x =  size_x // 4 * 4 + 1
shape_y = size_y // 4 * 4 + 1


grid = make_grid((shape_x, shape_y))

if (size_x // 4) * (size_y // 4) < 9:
    n_of_areas = 2
else:
    n_of_areas = random.randint(2, 3)

areas = get_random_areas(n_of_areas, grid)
while not check_areas(areas):
    areas = get_random_areas(n_of_areas, grid)

area_grid = generate_areas(areas, grid)

print_area_grid(area_grid)

fill_grid_borders((shape_x, shape_y))

fill_area_limits(grid, area_grid)

print_grid(grid)

"""

vertices_tiles_positions = {}

for i in vertices_tiles_positions:
    adjs = utils.get_adjacents(i, include_diagonals=True, include_straight=False)
    for adj in adjs:
        grid[adj[1]][adj[0]].tile_type = vertices_tiles_positions[i]
"""









