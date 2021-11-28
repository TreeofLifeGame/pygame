import pygame

import src.game as game


def main() -> None:
    pygame.init()
    game.Game().run()


if __name__ == '__main__':
    main()
