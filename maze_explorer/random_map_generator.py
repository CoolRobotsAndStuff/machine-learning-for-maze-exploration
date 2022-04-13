import random
from grid_maker import make_grid
import utils
import numpy as np
import copy

# Returns a random psition of a vortex node in the grid
def get_random_vortex_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "vortex":
            return (x, y)

# Returns a random position of a tile node in the grid
def get_random_tile_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "tile":
            return (x, y)

# Returns a random position of a wall node in the grid
def get_random_wall_position(grid, include_edges=True):
    minimum = 0 if include_edges else 1
    max_x = len(grid[0]) - 1 if include_edges else len(grid[0]) - 2
    max_y = len(grid) - 1 if include_edges else len(grid) - 2
    while True:
        x = random.randint(minimum, max_x)
        y = random.randint(minimum, max_y)
        if grid[y][x].node_type == "wall":
            return (x, y)

# Checks of there is a zero in an array
def zero_in_array(grid):
    for row in grid:
        for node in row:
            if node == 0:
                return True
    return False

# Subdivides the grid into areas
def get_random_areas(n_areas, grid):
    area_grid_width = (len(grid[0]) - 1) // 4
    area_grid_height = (len(grid) - 1) // 4

    area_grid = np.zeros((area_grid_height, area_grid_width), dtype=int)
    new_area_grid = np.zeros((area_grid_height, area_grid_width), dtype=int)
    probs = {}
    
    n_set = set(range(2, MAX_N_AREAS + 1))
    for i in range(n_areas):
        if i == 0:
            n = 1
        else:
            n = random.choice(list(n_set))
            n_set.remove(n)
        prob = random.randint(0, 99) / 100
        starting_vortex = get_random_vortex_position(grid, include_edges=False)
        starting_vortex = (starting_vortex[1] // 4, starting_vortex[0] // 4)
        while area_grid[starting_vortex] != 0:
            starting_vortex = get_random_vortex_position(grid, include_edges=False)
            starting_vortex = (starting_vortex[1] // 4, starting_vortex[0] // 4)
        area_grid[starting_vortex] = n
        new_area_grid[starting_vortex] = n
        probs[n] = prob
        

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
    return area_grid

# Checks if the areas are valid
def check_areas(areas):
    # checks all areas have a minimum of 3 nodes
    counts = list()
    for i in range(3):
        counts.append(np.count_nonzero(areas == i+1))
    print(counts)
    for count in counts:
        if 0 < count < 4:
            return False 
    return True
    
# Generates a grid from the areas
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

    return final_area_grid

# Prints an area grid
def print_area_grid(grid):
    node_to_pixel = {
        1: "\033[1;33;47m██"+ "\033[0m",
        2: "\033[1;31;47m██"+ "\033[0m",
        3: "\033[1;35;47m██"+ "\033[0m",
        0: "  ",
    }
    for row in grid:
        for node in row:
            print(node_to_pixel[node], end="")
        print()

# Fills the perimeter of the grid
def fill_grid_borders(shape):
    for x in range(0, shape[1]):
        grid[0][x].status = "occupied"
        grid[-1][x].status = "occupied"
    for y in range(0, shape[0]):
        grid[y][0].status = "occupied"
        grid[y][-1].status = "occupied"

# Given the area grid, fills the grid
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

# Prints the grid
def print_grid(grid):
    for row in grid:
        for val in row:
            print(val.get_string(), end="")
        
        print("\n", end="")

# Given the area grid, generates connections between areas randomly
def get_random_connections(areas):
    connection_grid = np.zeros(areas.shape, dtype=int)
    limits = {(1, 2):[], (2, 3):[], (3, 1):[]}
    for y, row in enumerate(areas):
        for x, value in enumerate(row):
            if value == 0:
                continue
            adjacents = utils.get_adjacents((y, x), include_straight=True, include_diagonals=False)
            for adjacent in adjacents:
                for val in limits.values():
                    if adjacent in val:
                        continue
                if adjacent[0] < 0 or adjacent[0] >= len(areas) or adjacent[1] < 0 or adjacent[1] >= len(areas[0]):
                    continue
                if areas[adjacent] == 0:
                    continue
                if areas[adjacent] == value:
                    continue
                for key in limits.keys():
                    set_key = set(key)
                    if set_key == set((value, areas[adjacent])):
                        limits[key].append(((x,y), (adjacent[1], adjacent[0])))


    final_limits = {}
    for key, value in limits.items():
        if len(limits[key]) == 0:
            continue

        r_limit = random.choice(limits[key])
        x, y = r_limit[0]

        final_limits[key] = r_limit

        if key == (1, 2):
            val = 1
        elif key == (2, 3):
            val = 2
        elif key == (3, 1):
            val = 3

        connection_grid[y][x] = val
    print(connection_grid)

    final_area_grid = np.zeros((len(grid), len(grid[0])), dtype=int)

    for y, row in enumerate(connection_grid):
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
    
    for key, value in final_limits.items():
        x1, y1 = value[0][0] * 4 + 2, value[0][1] * 4 + 2
        x2, y2 = value[1][0] * 4 + 2, value[1][1] * 4 + 2

        #print(x1, y1, ":", x2, y2)

        if x1 == x2:
            final_x = x1
            final_y = min(y1, y2) + 2
        elif y1 == y2:
            final_y = y1
            final_x = min(x1, x2) + 2
        
        final_area_grid[(final_y, final_x)] = -1
                

    return final_area_grid

# Given the connections grid, adds the connections in to the grid
def fill_connections(grid, connection_grid):
    conn_to_string = {
        1: "connection1-2",
        2: "connection2-3",
        3: "connection1-3",
        5: "start",
    }
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if connection_grid[y][x] == 0:
                continue
            if connection_grid[y][x] == -1:
                if node.node_type == "vortex":
                    node.status = "not_occupied"
                    adjacents = utils.get_adjacents((y, x), include_straight=True, include_diagonals=False)
                    for adjacent in adjacents:
                        if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                            continue
                        if grid[adjacent[0]][adjacent[1]].node_type == "wall":
                            grid[adjacent[0]][adjacent[1]].status = "not_occupied"
            elif node.node_type == "tile":
                node.tile_type = conn_to_string[connection_grid[y][x]]

# given a vortex, is it connected to a wall?
def has_adjacent_occupied(vortex_pos, grid):
    adjacents = utils.get_adjacents(vortex_pos, include_straight=True, include_diagonals=False, multiplier=2)
    for adjacent in adjacents:
        if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
            continue
        if grid[adjacent[1]][adjacent[0]].status == "occupied":
            return True
    return False

# Creates a random start tile in the grid
def fill_start(areas, connection_grid, grid):
    possible_start_nodes = []
    for y, row in enumerate(areas):
        for x, node in enumerate(row):
            x1 = x * 4 + 2
            y1 = y * 4 + 2
            is_valid = False
            if node != 1:
               continue
            if x == 0 or y == 0 or x == len(areas[0]) - 1 or y == len(areas) - 1:
                is_valid = True
            adjacents = utils.get_adjacents((y, x), include_straight=True, include_diagonals=False)
            for adjacent in adjacents:
                if adjacent[0] < 0 or adjacent[0] >= len(areas) or adjacent[1] < 0 or adjacent[1] >= len(areas[0]):
                    continue
                if areas[adjacent] != node:
                    is_valid = True
            if not has_adjacent_occupied((x1, y1), grid):
                is_valid = False
            
            if is_valid:
                possible_start_nodes.append((x1, y1))
    
    if len(possible_start_nodes) == 0:
        return
    
    """
    for start_node in possible_start_nodes:
        print("node_type", grid[start_node[1]][start_node[0]].node_type)
        adj = utils.get_adjacents(start_node, include_straight=False, include_diagonals=True)
        for adjacent in adj:
            grid[adjacent[1]][adjacent[0]].tile_type = "start"
    """
    while True:
        start_node = random.choice(possible_start_nodes)
        if connection_grid[start_node[1]][start_node[0]] == 0:
            adj = utils.get_adjacents(start_node, include_straight=False, include_diagonals=True)
            for adjacent in adj:
                grid[adjacent[1]][adjacent[0]].tile_type = "start"
            break
    
# Fills the walls in the borders between areas
def fill_walls_around_limits(grid, connection_grid):
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node.node_type == "vortex":
                
                if connection_grid[y][x] == 0 or connection_grid[y][x] == -1:
                    continue
                adjacents = utils.get_adjacents((y, x), include_straight=True, include_diagonals=False, multiplier=2)
                occ_count = 0
                possible_walls = []
                for adjacent in adjacents:
                    if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                        continue
                    if grid[adjacent[0]][adjacent[1]].status == "occupied":
                        occ_count += 1
                    elif connection_grid[adjacent[0]][adjacent[1]] == 0:
                        possible_walls.append(adjacent)

                final_walls = []
                random.shuffle(possible_walls)
                if occ_count == 0:
                    final_walls = possible_walls[0:2]
                elif occ_count == 1:
                    final_walls = possible_walls[0:1]

                for wall in final_walls:
                    grid[wall[0]][wall[1]].status = "occupied"
            
MAX_SIZE = 32
MIN_SIZE = 12

MIN_AREA_SIZE = 3

MAX_N_AREAS = 3
MIN_N_AREAS = 2

assert (MIN_SIZE ** 2) >= MIN_AREA_SIZE * MIN_N_AREAS

cycles = 101
while cycles > 100:
    cycles = 0
    size_x = random.randint(MIN_SIZE, MAX_SIZE)
    size_y = random.randint(MIN_SIZE, MAX_SIZE)

    while (size_x // 4) * (size_y // 4) < MIN_N_AREAS * MIN_AREA_SIZE:
        size_x = random.randint(MIN_SIZE, MAX_SIZE)
        size_y = random.randint(MIN_SIZE, MAX_SIZE)

    shape_x =  size_x // 4 * 4 + 1
    shape_y = size_y // 4 * 4 + 1

    grid = make_grid((shape_x, shape_y))

    if (size_x // 4) * (size_y // 4) < 9:
        n_of_areas = MIN_AREA_SIZE
    else:
        n_of_areas = random.randint(MIN_N_AREAS, MAX_N_AREAS)

    areas = get_random_areas(n_of_areas, grid)
    while not check_areas(areas):
        areas = get_random_areas(n_of_areas, grid)
        cycles += 1
        if cycles > 100:
            break

print_area_grid(areas)

area_grid = generate_areas(areas, grid)

print_area_grid(area_grid)
#print(area_grid)

fill_grid_borders((shape_x, shape_y))

fill_area_limits(grid, area_grid)

connections_grid = get_random_connections(areas)
#print_area_grid(connections_grid)
#print(connections_grid)

fill_connections(grid, connections_grid)

fill_start(areas, connections_grid, grid)

fill_walls_around_limits(grid, connections_grid)

print_grid(grid)









