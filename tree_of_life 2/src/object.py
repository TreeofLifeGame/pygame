class Object:
    def __init__(self, game):
        self.game = game
        self.wn = game.wn

    def render(self) -> None:
        pass

    def update(self) -> None:
        pass

    def exit(self) -> None:
        pass
