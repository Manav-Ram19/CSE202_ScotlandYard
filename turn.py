from board import Board
from collections import deque
from collections import defaultdict
from itertools import product

COVERAGE_THRESHOLD = 50

def heuristic_1_turn(board: Board,
        detective_logbook: list,
        mr_x_logbook: list,
        last_visible: int) -> list:

    possible_locations = get_possible_x_locations(board, detective_logbook, mr_x_logbook, last_visible)
    if len(possible_locations) == 1:
        return min_avg_distance(board, detective_logbook[-1], possible_locations[0])

    largest_avg_distance = get_largest_distance(board, detective_logbook[-1], possible_locations)
    return min_avg_distance(board, detective_logbook[-1], largest_avg_distance)
    # return [0,0,0] #temp, game ends as soon as Mr. X goes to vertex 0


def get_possible_x_locations(board: Board, 
                             detective_logbook: list,
                             mr_x_logbook: list,
                             last_visible: int) -> list:

    distance = 0
    neighbors = [last_visible]
    while distance < len(mr_x_logbook):
        transport = mr_x_logbook[distance]
        
        new_neighbors = []
        for neighbor in neighbors:
            new_neighbors.append(board.get_neighbors_by_transport(neighbor, transport))
        flattened_new_neighbors = list(set([item[0] for sublist in new_neighbors for item in sublist]))

        new_neighbors_no_det = []
        for n in flattened_new_neighbors:
            if n not in detective_logbook[distance+1]:
                new_neighbors_no_det.append(n)
        
        neighbors = flattened_new_neighbors
        distance += 1
    return neighbors


def min_avg_distance(board: Board, 
                     detective_locations: list, 
                     last_visible: int) -> list:

    #print(last_visible)
    distances = bfs(board, last_visible)
    neighbors = []
    for det_loc in detective_locations:
        curr_neighbors = [neighbor[0] for neighbor in board.get_neighbors(det_loc)]
        curr_neighbors.append(det_loc)
        neighbors.append(curr_neighbors)
    combinations = list(product(*neighbors))
    comb_unique = [combo for combo in combinations if len(set(combo)) == len(combo)]
    #potential worth to remove permutations so you avoid checking something 
    #like both (0,1,2) and (1,2,0) since they're guaranteed to have same
    #average distance

    best_combo = ()
    best_avg = float('inf')
    for combo in comb_unique:
        # print(combo)
        sum = 0.0
        for det_loc in combo:
            sum += distances[det_loc]
        avg = sum / len(detective_locations)
        # print(avg)
        if avg < best_avg:
            best_avg = avg
            best_combo = combo

    # print(neighbors)
    # print(combinations)
    # print(comb_unique)
    return list(best_combo)



def bfs(board: Board, 
        start: int) -> dict:
    distances = {}
    for i in range(board.get_num_vertices()):
        distances[i] = float('inf')
        distances[start] = 0

    queue = deque([start])

    while queue:
        curr_vert = queue.popleft()

        for neighbor in board.get_neighbors(curr_vert):
            neighbor_vert = neighbor[0]
            if distances[neighbor_vert] == float('inf'):
                distances[neighbor_vert] = distances[curr_vert] + 1
                queue.append(neighbor_vert)

    return distances

def get_largest_distance(board: Board,
                         detective_locations: list,
                         mr_x_possible_locations: list) -> int:
    total_distances = defaultdict(int)
    for det_loc in detective_locations:
        distances_det = bfs(board, det_loc)
        for x_loc in mr_x_possible_locations:
            total_distances[x_loc] += distances_det[x_loc]

    return min(total_distances.values())

def calculate_coverage(board: Board,
                      detective_locations: list,
                      mr_x_possible_locations: list) -> int:
    seen = set()
    counter = 0
    unique_mr_x_locations = set(mr_x_possible_locations)
    for det_loc in detective_locations:
        covered_locations = list(set([neighbor[0] for neighbor in list(board.get_neighbors(det_loc))]))
        covered_locations.append(det_loc)
        for neighbor in covered_locations:
            if neighbor in unique_mr_x_locations and neighbor not in seen:
                counter += 1
                seen.add(neighbor)
    return counter

def maximize_coverage(board: Board,
                    detective_locations: list,
                    mr_x_possible_locations: list) -> tuple [list, int]:
    detectives_remaining = detective_locations
    detectives_completed = []
    new_detective_locations, _ = compute_cover_optimal(board, detectives_remaining, detectives_completed, mr_x_possible_locations)
    return new_detective_locations

def compute_cover_optimal(board: Board,
                          detectives_remaining: list,
                          detectives_completed: list,
                          mr_x_possible_locations: list) -> tuple [list, int]:
    if len(detectives_remaining) == 0:
        return (detectives_completed, calculate_coverage(board, detectives_completed, mr_x_possible_locations))
    current_detective = detectives_remaining[0]
    current_max_coverage = 0
    D_best = []
    cur_detective_next_locations = list(set([neighbor[0] for neighbor in list(board.get_neighbors(current_detective))]))
    cur_detective_next_locations.append(current_detective)
    ctr = 0
    for n in cur_detective_next_locations:
        ctr += 1
        new_d_r = detectives_remaining[1:]
        # print(cur_detective_next_locations)
        # print(str(ctr) + str(new_d_r))
        new_d_c = detectives_completed
        #new_d_r = new_d_r.remove(current_detective)
        new_d_c.append(n)

        d_candidates, coverage_val = compute_cover_optimal(board, new_d_r, new_d_c, mr_x_possible_locations)
        if coverage_val > current_max_coverage or D_best == []:
            D_best = d_candidates
            current_max_coverage = coverage_val
    return (D_best, current_max_coverage)

def heuristic_2_turn(board: Board,
                      detective_logbook: list,
                      mr_x_logbook: list,
                      last_visible: int) -> list:
    possible_locations = get_possible_x_locations(board, detective_logbook, mr_x_logbook, last_visible)
    new_detective_locations = maximize_coverage(board, detective_logbook[-1], possible_locations)
    if calculate_coverage(board, new_detective_locations, possible_locations) / len(possible_locations) > COVERAGE_THRESHOLD:
        return new_detective_locations
    return heuristic_1_turn(board, detective_logbook, mr_x_logbook, last_visible)