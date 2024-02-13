from collections.abc import Callable
from board import SYTransport

def game(
        misterXOracle: Callable[[], tuple[SYTransport, int]]) -> None:
    misterXOracle()
    misterXOracle()