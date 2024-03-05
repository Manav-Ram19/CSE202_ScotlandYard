from enum import Enum
import numpy as np

class SYTransport(Enum):
    TAXI=1
    BUS=2
    RAIL=3

class Board(object):
    def __init__(self, filename):
        self.filename = filename
        self.adj_matrix = np.zeros(0)
        self.adj_list = {}
        self.create_board()
        
    def create_board(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        
        num_vertices = int(lines[0])
        self.adj_matrix = np.zeros((num_vertices, num_vertices))
        for vert in range(num_vertices):
            self.adj_list[vert] = []
        
        rem_lines = lines[1:]
        for line in rem_lines:
            line_split = line.replace("\n", "").split(" ")
            line_final = [int(line_split[0]), int(line_split[1]), SYTransport[line_split[2]].value]

            assert(line_final[0] != line_final[1])
            assert(line_final[0] < num_vertices)
            assert(line_final[1] < num_vertices)

            self.adj_matrix[line_final[0]][line_final[1]] = line_final[2]
            self.adj_matrix[line_final[1]][line_final[0]] = line_final[2]
            
            self.adj_list[line_final[0]].append((line_final[1], line_final[2]))
            self.adj_list[line_final[1]].append((line_final[0], line_final[2]))
    
    def get_adj_matrix(self):
        return self.adj_matrix
    
    def get_adj_list(self):
        return self.adj_list
    
    def get_neighbors(self, vert):
        return self.adj_list[vert]