from game import game
from mister_x import MisterX
from board import Board
from board import board_subset
from win import win
from turn import heuristic_1_turn
from turn import heuristic_2_turn
from turn import bfs
import random


def main():
    board = Board("board.txt")
    num_vertices = board.get_num_vertices()

    for num_det in range(5,10):
        for i in range(1000):
            print(i)
            pos = [random.randint(1, num_vertices) - 1 for _ in range(num_det+1)]
            # print(pos)
            x = MisterX(pos[0], board)
        
            detective_locs = pos[1:]
            assert(len(detective_locs) < num_vertices)
        
            distances = bfs(board, pos[0])
            sum = 0.0
            for det_loc in detective_locs:
                sum += distances[det_loc]
            avg = sum / len(detective_locs)
        
            turn_ctr, positions = game(detective_locs, x.get_location(), board, x.oracleMrXMoveRandom, heuristic_1_turn, win)
        
            with open("heur1_det" + str(num_det) + ".txt", 'a') as file:
                file.write(str(avg) + "," + str(turn_ctr) + "\n")


if __name__ == "__main__":
    main()