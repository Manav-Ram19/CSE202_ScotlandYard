from game import game
from mister_x import MisterX
from board import Board
import random


def main():
    board = Board("board.txt")
    num_vertices = board.get_num_vertices()
    
    x = MisterX(random.randint(1,num_vertices-1), board)
    game(x.oracleMrXMove)
    

if __name__ == "__main__":
    main()