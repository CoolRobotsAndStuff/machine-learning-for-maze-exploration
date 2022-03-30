def get_adjacents(position, include_straight = True, include_diagonals=False):
    straight = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    diagonals = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    adjacents = []
    if include_straight:
        adjacents += straight
    if include_diagonals:
        adjacents += diagonals
    for adj in adjacents:
        yield (position[0] + adj[0], position[1] + adj[1])