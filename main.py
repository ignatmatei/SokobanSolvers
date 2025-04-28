import os
import sys
import time

from sokoban.map import Map
from search_methods.lrta_star import LRTAStar
from search_methods.beam_search import BeamSearch
from search_methods.heuristics import (
    manhattan_distance,
    euclidean_distance,
    chebyshev_distance,
)

# --- Additional heuristics ---
def zero_heuristic(state):
    """Returnează mereu zero, imitând BFS."""
    return 0

def boxes_out_of_place(state):
    """Numără câte cutii nu sunt pe pozițiile finale."""
    count = 0
    for box in state.boxes.values():
        if (box.x, box.y) not in [(tx, ty) for tx,ty in state.targets]:
            count += 1
    return count

def sum_manhattan_boxes_to_storage(state):
    """Suma celor mai mici distanțe Manhattan de la fiecare cutie la cea mai apropiată destinație."""
    total = 0
    for box in state.boxes.values():
        min_dist = min(abs(box.x - tx) + abs(box.y - ty) for tx,ty in state.targets)
        total += min_dist
    return total
# --- Available heuristics ---
heuristics = {
    'manhattan': manhattan_distance,
    'euclidean': euclidean_distance,
    'chebyshev': chebyshev_distance,
    'zero': zero_heuristic,
    'boxes_out_of_place': boxes_out_of_place,
    'sum_manhattan_boxes_to_storage': sum_manhattan_boxes_to_storage
}

# --- Solvers ---
solvers = {
    'lrta*': LRTAStar,
    'beam-search': BeamSearch
}

# --- Maps to test ---
maps_to_test = [
    "easy_map1.yaml", "easy_map2.yaml",
    "medium_map1.yaml", "medium_map2.yaml",
    "hard_map1.yaml", "hard_map2.yaml",
    "large_map1.yaml", "large_map2.yaml",
    "super_hard_map1.yaml"
]

maps_folder = "tests/"  # Folderul unde se află hărțile

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <algorithm>")
        print("Example: python main.py lrta*")
        sys.exit(1)

    algorithm_name = sys.argv[1].lower()

    if algorithm_name not in solvers:
        print(f"Unknown algorithm '{algorithm_name}'. Available: {list(solvers.keys())}")
        sys.exit(1)

    # Creează folderul de output
    os.makedirs("output", exist_ok=True)

    for map_file in maps_to_test:
        map_path = os.path.join(maps_folder, map_file)
        if not os.path.exists(map_path):
            print(f"Map file '{map_file}' not found, skipping...")
            continue

        original_map = Map.from_yaml(map_path)

        for heuristic_name, heuristic_fn in heuristics.items():
            crt_map = original_map.copy()

            SolverClass = solvers[algorithm_name]
            agent = SolverClass(crt_map, heuristic_fn=heuristic_fn)

            start_time = time.time()
            path = agent.run(max_steps=20000)
            end_time = time.time()

            if path:
                solved = path[-1].is_solved()
                steps_taken = len(path)
            else:
                solved = False
                steps_taken = 0

            time_taken = round(end_time - start_time, 3)

            # Creează un fișier de output pentru fiecare combinație mapă-heuristică
            output_filename = f"output/output_{map_file.replace('.yaml', '')}_{heuristic_name}.txt"
            with open(output_filename, "w") as f:
                f.write(f"Algorithm: {algorithm_name.upper()}\n")
                f.write(f"Map: {map_file}\n")
                f.write(f"Heuristic: {heuristic_name}\n")
                if solved:
                    f.write(f"Solution found in {steps_taken} steps.\n")
                    f.write(f"Time taken: {time_taken} seconds.\n")
                else:
                    f.write(f"No solution found within step limit.\n")
                    f.write(f"Steps taken: {steps_taken}\n")
                    f.write(f"Time taken: {time_taken} seconds.\n")

    print(f"All results saved in 'output/' folder.")

