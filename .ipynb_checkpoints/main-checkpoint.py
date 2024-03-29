from game import game
from mister_x import MisterX
from board import Board
from board import board_subset
from win import win
from turn import heuristic_1_turn
from turn import heuristic_2_turn
import random


def main():
    board = Board("board.txt")
    num_vertices = board.get_num_vertices()

    # for i in range(100):
    #x = MisterX(random.randint(1,num_vertices-1), board)
    x = MisterX(12, board)

    #detective_locs = [41,46,124,142,167]
    detective_locs = [0,1,2]
    assert(len(detective_locs) < num_vertices)

    positions = game(detective_locs, x.get_location(), board, x.oracleMrXMoveRandom, heuristic_2_turn, win)


if __name__ == "__main__":
    main()