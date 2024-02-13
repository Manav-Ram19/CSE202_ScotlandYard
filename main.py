from game import game
from mister_x import MisterX


def main():
    x = MisterX(3)
    game(x.oracleMrXMove)


if __name__ == "__main__":
    main()