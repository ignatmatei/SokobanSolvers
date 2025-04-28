from sokoban.map import Map
from search_methods.heuristics import manhattan_distance
import heapq

class BeamSearch:
    def __init__(self, initial_state: Map, beam_width=100, heuristic_fn=manhattan_distance):
        self.beam_width = beam_width
        self.heuristic_fn = heuristic_fn
        self.initial_state = initial_state
        self.path = []

    def hash_state(self, state: Map) -> str:
        return str(state)

    def run(self, max_steps=10000):
        frontier = [(self.heuristic_fn(self.initial_state), self.initial_state, [])]  # (heuristic, state, path_so_far)
        visited = set()

        for step in range(max_steps):
            if not frontier:
                print(f"Frontier empty at step {step}. Stopping.")
                break

            all_successors = []
            for _, current_state, path_so_far in frontier:
                if current_state.is_solved():
                    self.path = path_so_far + [current_state]
                    return self.path

                current_key = self.hash_state(current_state)
                if current_key in visited:
                    continue
                visited.add(current_key)

                for move in current_state.filter_possible_moves():
                    new_state = current_state.copy()
                    try:
                        new_state.apply_move(move)
                    except:
                        continue
                    new_path = path_so_far + [current_state]
                    h = self.heuristic_fn(new_state)
                    all_successors.append((h, new_state, new_path))

            if not all_successors:
                print(f"No successors generated at step {step}. Stopping.")
                break

            # Sort all successors by heuristic value
            all_successors.sort(key=lambda x: x[0])

            # Pick top beam_width successors
            frontier = all_successors[:self.beam_width]

        # Max steps reached
        if frontier:
            best = min(frontier, key=lambda x: x[0])
            self.path = best[2] + [best[1]]

        return self.path

