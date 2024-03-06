from board import SYTransport
from board import Board
import random

class MisterX:
    def __init__(self, startingLocation: int, board: Board) -> None:
        self.location = startingLocation
        self.board = board
    
    def oracleMrXMove(self) -> tuple[int, SYTransport]:
        neighbors = self.board.get_neighbors(self.location)
        rand_neighbor = neighbors[random.randint(0, len(neighbors)-1)]
        
        self.location = rand_neighbor[0]
        match rand_neighbor[1]:
            case 1:
                transport_enum = SYTransport.TAXI
            case 2:
                transport_enum = SYTransport.BUS
            case 3:
                transport_enum = SYTransport.RAIL
        
        return (self.location, transport_enum)