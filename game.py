from collections.abc import Callable
from board import SYTransport
from board import Board
from turn import heuristic_1_turn, heuristic_2_turn

def game(detective_start_locations: list, 
         mr_x_start_location: int,
         board: Board,
         misterXOracle: Callable[[], tuple[int, SYTransport]],
         turn: Callable[[], list],
         win: Callable[[], bool]) -> None:

    D = detective_start_locations 
    positions = [D]

    logbook = []
    visible = [mr_x_start_location]
    mr_x_curr_pos = -1
    visibility_ctr = 0

    # debug_det_log = []
    # debug_x_log = []
    
    turn_ctr = 0
    while not win(board, D, mr_x_curr_pos):
        
        move = misterXOracle(positions[-1])
        
        # debug_x_log.append(move)
        # print("X_LOG:", debug_x_log)
        # print("DET_LOG:", debug_det_log)
        
        if visibility_ctr == 0:
            visible.append(move[0])
            logbook = []
            if len(positions) == 4:
                positions = [positions[-1]]
            # else:
            #     print("not 4")
        else:
            logbook.append(move[1])
        
        mr_x_curr_pos = move[0]
        # print(mr_x_curr_pos)

        # recheck win condition (after mr. x moves, before detectives move)
        if win(board, D, mr_x_curr_pos):
            break

        D = turn(board, positions, logbook, visible[-1])
        # debug_det_log.append(D)

        visibility_ctr += 1
        visibility_ctr %= 3
            
        turn_ctr += 1
        print(turn_ctr)
        positions.append(D)
        
    print(turn_ctr)
    return positions