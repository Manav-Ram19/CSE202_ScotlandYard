from board import SYTransport
from board import Board
from turn import bfs
import random

class MisterX:
    def __init__(self, startingLocation: int, board: Board) -> None:
        self.location = startingLocation
        self.board = board
    
    def oracleMrXMoveRandom(self, detective_locations: list) -> tuple[int, SYTransport]:
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

    def oracleMrXMoveFurthest(self, detective_locations: list) -> tuple[int, SYTransport]:
        neighbors = self.board.get_neighbors(self.location)

        best_avg = 0
        best_neighbor = neighbors[0]
        for neighbor in neighbors:
            distances = bfs(self.board, neighbor[0])
            sum = 0.0
            for det_loc in detective_locations:
                sum += distances[det_loc]
            avg = sum / len(detective_locations)

            if avg > best_avg:
                best_avg = avg
                best_neighbor = neighbor

        self.location = best_neighbor[0]
        match best_neighbor[1]:
            case 1:
                transport_enum = SYTransport.TAXI
            case 2:
                transport_enum = SYTransport.BUS
            case 3:
                transport_enum = SYTransport.RAIL

        return (self.location, transport_enum)

    def oracleMrXMoveAverage(self, detective_locations: list) -> tuple[int, SYTransport]:
        neighbors = self.board.get_neighbors(self.location)

        averages = []
        for neighbor in neighbors:
            distances = bfs(self.board, neighbor[0])
            sum = 0.0
            for det_loc in detective_locations:
                sum += distances[det_loc]
            avg = sum / len(detective_locations)

            averages.append([avg, neighbor])

        averages_sorted = sorted(averages, key = lambda x : x[0])
        best_neighbor = averages_sorted[len(averages_sorted) // 2][1]

        self.location = best_neighbor[0]
        match best_neighbor[1]:
            case 1:
                transport_enum = SYTransport.TAXI
            case 2:
                transport_enum = SYTransport.BUS
            case 3:
                transport_enum = SYTransport.RAIL

        return (self.location, transport_enum)

    def get_location(self):
        return self.location