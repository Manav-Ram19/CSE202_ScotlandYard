from board import SYTransport

class MisterX:
    def __init__(self, startingLocation: int) -> None:
        self.location = startingLocation
    
    def oracleMrXMove(self) -> tuple[SYTransport, int]:
        print (self.location)
        self.location += 1
        return (SYTransport.RAIL, 0)