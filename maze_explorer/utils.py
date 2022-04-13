# Returns the adjacnets of a position
def get_adjacents(position, include_straight = True, include_diagonals=False, multiplier=1):
    straight = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    diagonals = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    for st in straight:
        st[0] *= multiplier
        st[1] *= multiplier
    for d in diagonals:
        d[0] *= multiplier
        d[1] *= multiplier
    adjacents = []
    if include_straight:
        adjacents += straight 
    if include_diagonals:
        adjacents += diagonals
    for adj in adjacents:
        yield (position[0] + adj[0], position[1] + adj[1])

def is_even(number):
    return number % 2 == 0

def is_odd(number):
    return number % 2 != 0