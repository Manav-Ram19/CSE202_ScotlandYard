from game import game
from mister_x import MisterX
from board import Board
from win import win
import random


def main():
    board = Board("board.txt")
    num_vertices = board.get_num_vertices()

    x = MisterX(random.randint(1,num_vertices-1), board)

    detective_locs = [0,1,2]
    assert(len(detective_locs) < num_vertices)
    
    positions = game(detective_locs, board, x.oracleMrXMove, win)
    

if __name__ == "__main__":
    main()