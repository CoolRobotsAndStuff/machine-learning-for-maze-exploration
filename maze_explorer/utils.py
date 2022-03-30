def get_adjacents(position, diagonals=False):
    adjacents = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    diagonals = [[1, 1], [-1, 1], [1, -1], [-1, -1]] if diagonals else []
    for adj in adjacents + diagonals:
        yield (position[0] + adj[0], position[1] + adj[1])