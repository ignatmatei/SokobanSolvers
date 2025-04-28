from sokoban.map import Map
from math import sqrt
def manhattan_distance(state: Map) -> int:
    """Heuristic: sum of minimal distances from each box to the closest target."""
    total = 0
    for box in state.boxes.values():
        distances = [abs(box.x - tx) + abs(box.y - ty) for tx, ty in state.targets]
        if distances:
            total += min(distances)
    return total
def euclidean_distance(state: Map) -> float:
    """Sum of Euclidean distances from boxes to nearest targets."""
    total = 0.0
    for box in state.boxes.values():
        distances = [sqrt((box.x - tx)**2 + (box.y - ty)**2) for tx, ty in state.targets]
        if distances:
            total += min(distances)
    return total

def chebyshev_distance(state: Map) -> int:
    """Sum of Chebyshev distances (max delta x or delta y) from boxes to targets."""
    total = 0
    for box in state.boxes.values():
        distances = [max(abs(box.x - tx), abs(box.y - ty)) for tx, ty in state.targets]
        if distances:
            total += min(distances)
    return total

def zero_heuristic(state: Map) -> int:
    """Zero heuristic for testing (turns LRTA* into basically BFS)."""
    return 0
