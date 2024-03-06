from collections.abc import Callable
from board import SYTransport

def game(
        misterXOracle: Callable[[], tuple[int, SYTransport]]) -> None:
    print(misterXOracle())
    print(misterXOracle())