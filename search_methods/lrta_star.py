from sokoban.map import Map
from search_methods.heuristics import manhattan_distance

class LRTAStar:
    def __init__(self, initial_state: Map, heuristic_fn=manhattan_distance):
        self.H = {}  # state hash -> heuristic value
        self.state = initial_state
        self.heuristic_fn = heuristic_fn
        self.path = []  # path of states

    def hash_state(self, state: Map) -> str:
        return str(state)

    def run(self, max_steps=1000):
        current = self.state
        self.path.append(current)

        for step in range(max_steps):
            if current.is_solved():
                print(f"Solved in {step} steps!")
                return self.path

            state_key = self.hash_state(current)
            if state_key not in self.H:
                self.H[state_key] = self.heuristic_fn(current)

            neighbors = []
            for move in current.filter_possible_moves():
                new_state = current.copy()
                try:
                    new_state.apply_move(move)
                except:
                    continue
                new_key = self.hash_state(new_state)
                if new_key not in self.H:
                    self.H[new_key] = self.heuristic_fn(new_state)
                cost = 1 + self.H[new_key]
                neighbors.append((cost, move, new_state))

            if not neighbors:
                print("No valid moves left. Stuck.")
                return self.path

            # Choose neighbor with the lowest estimated cost
            neighbors.sort()
            _, best_move, best_state = neighbors[0]

            # Update heuristic of current state
            self.H[state_key] = neighbors[0][0]

            current = best_state
            self.path.append(current)

        print(f"Stopped after {max_steps} steps.")
        return self.path

