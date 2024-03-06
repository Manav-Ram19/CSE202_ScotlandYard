from board import Board

def win(board: Board,
        detective_locations: list,
        mr_x_curr_pos: int) -> bool:
    
    for loc in detective_locations:
        if loc == mr_x_curr_pos:
            return True
            
    return False