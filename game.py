from collections.abc import Callable
from board import SYTransport
from board import Board
from turn import heuristic_1_turn

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
    while not win(board, D, mr_x_curr_pos):
        visibility_ctr += 1
        visibility_ctr %= 3
        
        move = misterXOracle()
        logbook.append(move[1])
        if visibility_ctr == 0:
            visible.append(move[0])
        
        mr_x_curr_pos = move[0]
        # print(mr_x_curr_pos)

        # recheck win condition (after mr. x moves, before detectives move)
        if win(board, D, mr_x_curr_pos):
            break

        if visibility_ctr == 0:
            D = turn(board, positions[-3:], logbook[-3:], visible[-1])
        else:
            D = turn(board, positions[-visibility_ctr:], logbook[-visibility_ctr:], visible[-1])
        positions.append(D)

    return positions