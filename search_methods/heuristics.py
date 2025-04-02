
def Manhattan(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)
def Euclidean(node, goal):
    return ((node.x - goal.x)**2 + (node.y - goal.y)**2)**0.5
def Chebyshev(node, goal):
    return max(abs(node.x - goal.x), abs(node.y - goal.y))
def Octile(node, goal):
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return dx + dy + (2**0.5 - 2) * min(dx, dy)
def Diagonal(node, goal):
    dx = abs(node.x - goal.x)
    dy = abs(node.y - goal.y)
    return (dx + dy) + (2**0.5 - 2) * min(dx, dy)

