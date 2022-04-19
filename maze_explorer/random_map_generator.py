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
        if 0 < count < 3:
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
        -1: "\033[1;30;47m██"+ "\033[0m",
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
                adjacents = list(utils.get_adjacents((y, x), include_straight=True, include_diagonals=False, multiplier=2))
                diag_adjacents = [[(1, 2), (-1, 2)], [(1, -2), (-1, -2)], [(2, 1), (2, -1)],[(-2, 1), (-2, -1)],]
                occ_count = 0
                possible_walls = []
                for index, adjacent in enumerate(adjacents):
                    if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                        continue
                    if grid[adjacent[0]][adjacent[1]].status == "occupied":
                        occ_count += 1
                    elif connection_grid[adjacent[0]][adjacent[1]] == 0:
                        possible_walls.append(diag_adjacents[index])
                        

                final_walls = []
                random.shuffle(possible_walls)
                if occ_count == 0:
                    final_walls = possible_walls[0:2]
                elif occ_count == 1:
                    final_walls = possible_walls[0:1]

                for wall in final_walls:
                    for w in wall:
                        grid[y+ w[0]][x + w[1]].status = "occupied"
                        adjacents = utils.get_adjacents((y+ w[0], x + w[1]), include_straight=True, include_diagonals=False)
                        for adjacent in adjacents:
                            if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                                continue
                            if grid[adjacent[0]][adjacent[1]].node_type == "vortex":
                                grid[adjacent[0]][adjacent[1]].status = "occupied"
                    
                    """
                    wall_adjs = []
                    for adjacent in utils.get_adjacents(wall, include_straight=True, include_diagonals=False):
                        if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                            continue
                        if grid[adjacent[0]][adjacent[1]].node_type == "wall":
                            wall_adjs.append(adjacent)
                    """
                    """
                    for wall_adj in wall_adjs:
                        grid[wall_adj[0]][wall_adj[1]].status = "occupied"
                    
                        adjacents = utils.get_adjacents(wall_adj, include_straight=True, include_diagonals=False)
                        for adjacent in adjacents:
                            if adjacent[0] < 0 or adjacent[0] >= len(grid) or adjacent[1] < 0 or adjacent[1] >= len(grid[0]):
                                continue
                            if grid[adjacent[0]][adjacent[1]].node_type == "vortex":
                                grid[adjacent[0]][adjacent[1]].status = "occupied"
                    """
def get_vortex_tile_type(grid, vortex_pos):
    #assert grid[vortex_pos[1]][vortex_pos[0]].node_type == "vortex"
    counts = {}
    adjacents = utils.get_adjacents(vortex_pos, include_straight=False, include_diagonals=True)
    for adjacent in adjacents:
        if adjacent[0] < 0 or adjacent[1] >= len(grid) or adjacent[1] < 0 or adjacent[0] >= len(grid[0]):
            continue
        tile_type = grid[adjacent[1]][adjacent[0]].tile_type
        if tile_type not in counts:
            counts[tile_type] = 0
        counts[tile_type] += 1
    
    for tile_type in counts:
        if counts[tile_type] > 2:
            return tile_type

def get_valid_adjacents(pos, grid, invalid_tile_types=[]):
    middle_adjacents = utils.get_adjacents(pos, include_straight=True, include_diagonals=False)
    final_adjacents = utils.get_adjacents(pos, include_straight=True, include_diagonals=False, multiplier=2)
    
    valid_adjacents = []
    for m_adjacent, f_adjacent in zip(middle_adjacents, final_adjacents):

        is_valid = True
        if m_adjacent[0] < 0 or m_adjacent[0] >= len(grid[0]) or m_adjacent[1] < 0 or m_adjacent[1] >= len(grid):
            #print("INVALID BECAUSE MIDDLE OUT OF BOUNDS")
            is_valid = False
        elif grid[m_adjacent[1]][m_adjacent[0]].status == "occupied":
            #print("INVALID BECAUSE MIDDLE OCCUPIED")
            is_valid = False
    
        if f_adjacent[0] < 0 or f_adjacent[0] >= len(grid[0]) or f_adjacent[1] < 0 or f_adjacent[1] >= len(grid):
            is_valid = False
            #print("INVALID BECAUSE FINAL OUT OF BOUNDS")
        elif grid[f_adjacent[1]][f_adjacent[0]].status == "occupied":
            #print("INVALID BECAUSE FINAL OCCUPIED")
            is_valid = False
        v_tile_type = get_vortex_tile_type(grid, (f_adjacent[0], f_adjacent[1]))
        if v_tile_type is not None:
            if v_tile_type in invalid_tile_types:
                is_valid = False
                #print("NOT VALID FOR INVALID TILES")
        if is_valid:
            valid_adjacents.append(f_adjacent)

    return valid_adjacents

def bfs(grid, start_node, end_node, invalid_tile_types=[]):
    queue = list()
    queue.append(start_node)
    visited = set()
    visited.add(start_node)
    while queue:
        node = queue.pop(0)
        if node == end_node:
            return True, visited
        adjacents = get_valid_adjacents(node, grid, invalid_tile_types)
        for adjacent in adjacents:
            if adjacent in visited or adjacent in queue:
                continue
            queue.append(adjacent)
            visited.add(adjacent)
    return False, visited


def check_travesability_between_limits(start_tile_type, goal_tile_type, grid):
    invalid_tile_types = ["connection1-2", "connection1-3", "connection2-3"]
    if start_tile_type in invalid_tile_types:
        invalid_tile_types.remove(start_tile_type)
    if goal_tile_type in invalid_tile_types:
        invalid_tile_types.remove(goal_tile_type)

    start_vortex = None
    goal_vortex = None

    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node.node_type == "vortex":
                v_tile_type = get_vortex_tile_type(grid, (x, y))
                if v_tile_type is None or v_tile_type == "undefined":
                    continue
                if v_tile_type == start_tile_type:
                    start_vortex = (x, y)
                if v_tile_type == goal_tile_type:
                    goal_vortex = (x, y)
    
    """
    grid[start_vortex[1]][start_vortex[0]].status = "occupied"
    adj = get_valid_adjacents(start_vortex, grid, invalid_tile_types)
    for adjacent in adj:
        grid[adjacent[1]][adjacent[0]].status = "occupied"
    """
    
    
    if start_vortex is None or goal_vortex is None:
        return False
        
    
    accesible, visited = bfs(grid, start_vortex, goal_vortex, invalid_tile_types)

    """
    print(visited)

    for v in visited:
        grid[v[1]][v[0]].status = "occupied"
    """

    return accesible

def check_area_traversability(area_n, grid):
    tile_types_in_grid = []
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node.node_type == "vortex":
                v_tile_type = get_vortex_tile_type(grid, (x, y))
                if v_tile_type is None or v_tile_type == "undefined":
                    continue
                tile_types_in_grid.append(v_tile_type)
  
    if area_n == 1:
        is_valid = True
        if "connection1-2" in tile_types_in_grid:
            if not check_travesability_between_limits("start", "connection1-2", grid):
                is_valid = False
        if "connection1-3" in tile_types_in_grid:
            if not check_travesability_between_limits("start", "connection1-3", grid):
                is_valid = False
    

    elif area_n == 2:
        is_valid = True
        if "connection2-3" in tile_types_in_grid and "connection1-3" in tile_types_in_grid:
                if not check_travesability_between_limits("connection1-3", "connection2-3", grid):
                    is_valid = False

        elif "connection1-2" in tile_types_in_grid:
            if not check_travesability_between_limits("start", "connection1-2", grid):
                is_valid = False

    elif area_n == 3:
        is_valid = True
        if "connection2-3" in tile_types_in_grid:
            if "connection1-2" in tile_types_in_grid:
                if not check_travesability_between_limits("connection1-2", "connection2-3", grid):
                    is_valid = False

        elif "connection1-3" in tile_types_in_grid:
            if not check_travesability_between_limits("start", "connection1-3", grid):
                is_valid = False

    return is_valid
    

def vortex_tile_type(grid):
    vortex_tile_types = np.zeros((len(grid), len(grid[0])), dtype=str)
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node.node_type == "vortex":
                vortex_tile_types[y, x] = get_vortex_tile_type(grid, (x, y))
            else:
                 vortex_tile_types[y, x] = " "
    print(vortex_tile_types)

def get_mask_from_grid(grid, areas_grid, fill_special_tiles = True):
    mask = np.ones((len(grid), len(grid[0])), dtype=int)
    mask.fill(-1)

    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            value = areas_grid[y, x]
            
            if node.status == "occupied":
                    mask[y, x] = 0
            elif node.node_type == "vortex" and fill_special_tiles:
                v_tyle_type = get_vortex_tile_type(grid, (x, y))
                if v_tyle_type is not None and v_tyle_type != "undefined":
                    mask[y, x] = 0
                    adjacents = utils.get_adjacents((x,y), include_straight=True, include_diagonals=True)
                    for adjacent in adjacents:
                        if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                            continue
                        mask[adjacent[1], adjacent[0]] = 0
                
            elif node.node_type == "tile":
                if node.tile_type != "undefined" and fill_special_tiles:
                    mask[y, x] = 0
    #print_area_grid(mask)
    for y, row in enumerate(mask):
        for x, node in enumerate(row):
            value = areas_grid[y, x]
            if node == -1:
                if value != 0 and value != -1:
                    mask[y, x] = value
                else:
                    color_counts = {1: 0, 2: 0, 3: 0}
                    adjacents = utils.get_adjacents((x,y), include_straight=True, include_diagonals=True)
                    for adjacent in adjacents:
                        if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                            continue
                        if area_grid[adjacent[1], adjacent[0]] in color_counts:
                                color_counts[area_grid[adjacent[1], adjacent[0]]] += 1
                    max_value = 0
                    final_color = -1
                    for color in color_counts:
                        if color_counts[color] > max_value:
                            max_value = color_counts[color]
                            final_color = color                 
                    mask[y, x] = final_color
                        
                    
    return mask

def fill_special_tiles(grid, mask):
    special_tiles = ("checkpoint", "swamp") 
    odds = 0.6
    colour_counts = {}
    max_density = 0.01
    for colour in (1, 2, 3):
        colour_count = 0
        for y, row in enumerate(mask):
            for x, node in enumerate(row):
                if node == colour:
                    colour_count += 1
        if colour_count > 0:
            colour_counts[colour] = random.randint(0, int(colour_count * max_density) + 1)
    
    for colour in colour_counts:
        cycles = 0
        while cycles < colour_counts[colour]:
            random_vortex = get_random_vortex_position(grid, False)
            
            if (random_vortex[0] - 2) % 4 != 0:
                continue
            if (random_vortex[1] - 2) % 4 != 0:
                continue
            
            if mask[random_vortex[1], random_vortex[0]] != colour:
                continue
            if random.random() > odds:
                tile_type = "swamp"
            else:
                tile_type = "checkpoint"
            adjacents = utils.get_adjacents(random_vortex, include_straight=False, include_diagonals=True)
            for adjacent in adjacents:
                if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                    continue
                grid[adjacent[1]][adjacent[0]].tile_type = tile_type
            cycles += 1



def area_accesibility_bfs(grid, mask, start_pos, area_n):
    visited = set()
    queue = []
    if mask[start_pos[1], start_pos[0]] == area_n:
        queue.append(start_pos)
        visited.add(start_pos)
    else:
        small_adjs = get_valid_adjacents(start_pos, grid, ["hole",])
        for adj in small_adjs:
            if mask[adj[1], adj[0]] == area_n:
                queue.append(adj)
                visited.add(adj)
            big_adjs = get_valid_adjacents(adj, grid, ["hole",])
            for big_adj in big_adjs:
                if mask[big_adj[1], big_adj[0]] == area_n:
                    queue.append(big_adj)
                    visited.add(big_adj)

    while len(queue) > 0:
        current_pos = queue.pop(0)
        adjacents = get_valid_adjacents(current_pos, grid, ["hole"])
        for adjacent in adjacents:
            if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                continue
            if mask[adjacent[1], adjacent[0]] == area_n:
                if adjacent not in visited and adjacent not in queue:
                    queue.append(adjacent)
                    visited.add(adjacent)
    return visited

def get_area_accesibility(grid, mask, area_n):
    if area_n == 1:
        possible_starts = ("start",)
    elif area_n == 2:
        possible_starts = ("connection1-2", "connection2-3")
    elif area_n == 3:
        possible_starts = ("connection2-3", "connection1-3")
    
    tile_types_in_grid = {}
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if node.node_type == "vortex":
                v_tile_type = get_vortex_tile_type(grid, (x, y))
                if v_tile_type is None or v_tile_type == "undefined":
                    continue
                tile_types_in_grid[v_tile_type] = (x, y)


    print("tile_types_in_grid", tile_types_in_grid)
    accesible_set = set()
    for start_type in possible_starts:
        if start_type in tile_types_in_grid:
            start_pos = tile_types_in_grid[start_type]
            visited = area_accesibility_bfs(grid, mask, start_pos, area_n)
            print("area accesibility", len(visited))
            accesible_set = accesible_set.union(visited)
    return len(accesible_set)
    
    
def get_area_vortex_count(grid, mask, area_n):
    vortex_count = 0
    for y, row in enumerate(mask):
        for x, node in enumerate(row):
            if node == area_n and grid[y][x].node_type == "vortex":
                vortex_count += 1
    return vortex_count

    
def check_area_accesibilty(grid, mask, area_n):
    threshold = 0.3

    traversable_verticies = get_area_accesibility(grid, mask, area_n)
    total_verticies = get_area_vortex_count(grid, mask, area_n)
    
    if total_verticies == 0:
        return True
    print("area" + str(area_n), traversable_verticies, total_verticies, traversable_verticies / total_verticies)
    if traversable_verticies > total_verticies:
        raise Exception("Traversable verticies greater than total verticies")

    if traversable_verticies < 4:
        return False
    
    elif traversable_verticies > 20:
        return True

    

    if traversable_verticies / total_verticies > threshold:
        return True
    else:
        return False

def erode(possible_walls, grid):
    final_walls = copy.deepcopy(possible_walls)
    base_probability = 0.01
    expansion_coefficient = 0.2
    temp_walls = copy.deepcopy(final_walls)
    
    for wall in final_walls:
        #rev_wall = (wall[1], wall[0])
        blanks = []
        adjacents = utils.get_adjacents(wall, include_straight=True, include_diagonals=False, multiplier=2)
        for adjacent in adjacents:
            if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                continue
            if grid[adjacent[1]][adjacent[0]].status == "not_occupied":
                blanks.append(adjacent)

        n_of_blanks = len(blanks)
        prob = base_probability + (n_of_blanks / 4) * expansion_coefficient
        if random.random() < prob:
            temp_walls.remove(wall)
    final_walls = copy.deepcopy(temp_walls)
    return final_walls

def fill_in_walls(grid, walls):
    for wall in walls:
        grid[wall[1]][wall[0]].status = "occupied"
        adjacents = utils.get_adjacents(wall, include_straight=True, include_diagonals=False)
        for adjacent in adjacents:
            if adjacent[0] < 0 or adjacent[0] >= len(grid[0]) or adjacent[1] < 0 or adjacent[1] >= len(grid):
                continue
            if grid[adjacent[1]][adjacent[0]].node_type == "vortex":
                grid[adjacent[1]][adjacent[0]].status = "occupied"

def fill_walls_area_2(grid, mask, mask_with_tiles):
    max_density = 0.5

    possible_walls = []
    for y, row in enumerate(grid):
        for x, node in enumerate(row):
            if mask_with_tiles[y, x] == 2:
                if node.node_type == "wall":
                    possible_walls.append([x, y])
    
    if len(possible_walls) == 0:
        return grid

    wall_poses = copy.deepcopy(possible_walls)
    my_grid = copy.deepcopy(grid)
    while True:
        wall_poses = erode(wall_poses, my_grid)
        my_grid = copy.deepcopy(grid)

        fill_in_walls(my_grid, wall_poses)
        print_grid(my_grid)

        if len(wall_poses) == 0:
            return grid

        print("AREA TRAVERSABLE", check_area_traversability(2, my_grid))
        traversable = check_area_traversability(2, my_grid) and check_area_traversability(3, my_grid) and check_area_traversability(1, my_grid)
        if check_area_accesibilty(my_grid, mask, 2) and traversable:
            break
    
    return my_grid
            
MAX_SIZE = 32
MIN_SIZE = 12

MIN_AREA_SIZE = 3

MAX_N_AREAS = 3
MIN_N_AREAS = 2

assert (MIN_SIZE ** 2) >= MIN_AREA_SIZE * MIN_N_AREAS

do_break_1 = False
while True:
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
            n_of_areas = MIN_N_AREAS
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

    
    #print_area_grid(connections_grid)
    #print(connections_grid)
    backup_grid = copy.deepcopy(grid)
    total_cycles = 0
    do_break = False
    while not do_break:
        grid = copy.deepcopy(backup_grid)
        
        connections_grid = get_random_connections(areas)

        fill_connections(grid, connections_grid)

        fill_start(areas, connections_grid, grid)

        fill_walls_around_limits(grid, connections_grid)

        backup_grid_1 = copy.deepcopy(grid)
        cycles = 0
        while True:
            print(cycles)
            grid = copy.deepcopy(backup_grid_1)
            fill_walls_around_limits(grid, connections_grid)

            mask_no_tiles = get_mask_from_grid(grid, area_grid, fill_special_tiles=False)
            print_area_grid(mask_no_tiles)
            traversable = check_area_traversability(1, grid) and check_area_traversability(2, grid) and check_area_traversability(3, grid)
            accesible = check_area_accesibilty(grid, mask_no_tiles, 1) and check_area_accesibilty(grid, mask_no_tiles, 2) and check_area_accesibilty(grid, mask_no_tiles, 3)
            if not accesible:
                print("CHANGED BECAUSE NOT ACCESIBLE")
            if traversable and accesible:
                do_break = True
                do_break_1 = True
                break
                
            if cycles > 20:
                break
            cycles += 1
        total_cycles += 1
        if total_cycles > 20:
            break

    if do_break_1:
        break



#vortex_tile_type(grid)

#check_area_navegability("start", "connection1-2", grid)

print("area 1 traversable:", check_area_traversability(1, grid))
print("area 2 traversable:", check_area_traversability(2, grid))
print("area 3 traversable:", check_area_traversability(3, grid))

mask = get_mask_from_grid(grid, area_grid)



#fill_special_tiles(grid, mask)

mask = get_mask_from_grid(grid, area_grid)
print_area_grid(mask)

mask_no_tiles_2 = get_mask_from_grid(grid, area_grid, fill_special_tiles=False)

wall_grid = fill_walls_area_2(grid, mask_no_tiles_2, mask)


grid = copy.deepcopy(wall_grid)

"""
fill_obstacles_area_1()

fill_obstacles_area_2()

fill_obstacles_area3()

check_area_navegability()
"""
print_grid(grid)









