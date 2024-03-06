from collections.abc import Callable
from board import SYTransport
from board import Board
from turn import turn

def game(detective_locations: list, 
         board: Board,
         misterXOracle: Callable[[], tuple[int, SYTransport]],
         win: Callable[[], bool]) -> None:

    D = detective_locations
    positions = [D]

    logbook = []
    visible = []
    mr_x_curr_pos = -1
    visibility_ctr = 0
    while not win(board, D, mr_x_curr_pos):
        visibility_ctr += 1
        
        move = misterXOracle()
        logbook.append(move[1])
        if visibility_ctr % 3 == 0:
            visible.append(move[0])
        
        mr_x_curr_pos = move[0]
        # print(mr_x_curr_pos)

        D = turn(board, D, logbook, visible)
        positions.append(D)

    return positions