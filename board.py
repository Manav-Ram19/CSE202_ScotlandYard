from enum import Enum
import numpy as np

def board_subset(filename: str, 
                 size: int) -> None:
    output_filename = filename[:-4] + "_" + str(size) + ".txt"
    with open(filename, 'r') as original_file:
        lines = original_file.readlines()[1:]

    with open(output_filename, 'w') as out_file:
        out_file.write(str(size) + "\n")
        for line in lines:
            line_split = line.split()
            if int(line_split[0]) < size and int(line_split[1]) < size:
                print(line)
                out_file.write(line)

class SYTransport(Enum):
    TAXI=1
    BUS=2
    RAIL=3

class Board(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.num_vertices = 0
        self.adj_matrix = np.zeros(0)
        self.adj_list = {}
        self.create_board()
        
    def create_board(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        
        self.num_vertices = int(lines[0])
        self.adj_matrix = np.zeros((self.num_vertices, self.num_vertices))
        for vert in range(self.num_vertices):
            self.adj_list[vert] = []
        
        rem_lines = lines[1:]
        for line in rem_lines:
            line_split = line.replace("\n", "").split(" ")
            line_final = [int(line_split[0]), int(line_split[1]), SYTransport[line_split[2]].value]

            assert(line_final[0] != line_final[1])
            assert(line_final[0] < self.num_vertices)
            assert(line_final[1] < self.num_vertices)

            self.adj_matrix[line_final[0]][line_final[1]] = line_final[2]
            self.adj_matrix[line_final[1]][line_final[0]] = line_final[2]
            
            self.adj_list[line_final[0]].append((line_final[1], line_final[2]))
            self.adj_list[line_final[1]].append((line_final[0], line_final[2]))
    
    def get_num_vertices(self):
        return self.num_vertices
    
    def get_adj_matrix(self):
        return self.adj_matrix
    
    def get_adj_list(self):
        return self.adj_list
    
    def get_neighbors(self, vert: int):
        return self.adj_list[vert]

    def get_neighbors_by_transport(self, vert: int, transport: SYTransport):
        adj_list_vert = self.adj_list[vert]
        out = []
        for path in adj_list_vert:
            if path[1] == transport.value:
                out.append(path)
        return out