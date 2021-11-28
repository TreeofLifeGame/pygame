import pygame
import sys

import src.ui as ui


class Scene:
    def __init__(self, game):
        self.game = game
        self.wn = game.wn
        self.help = None  # type: Scene

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

    def close(self) -> int:  # returns amount of points collected
        pass

    def exit(self) -> None:  # exit is exiting the game, closing is exiting the scene
        pygame.quit()
        sys.exit()


class HelpScene(Scene):
    def __init__(self, game, img):
        super(HelpScene, self).__init__(game)

        self.img = img

        self.back_surf = pygame.image.load(game.image_map["back"]).convert_alpha()
        self.menu_surf = pygame.image.load(game.image_map["menu"]).convert_alpha()

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])
        self.wn.blit(self.img, (18, 180))

        m = self.game.mouse_was_released

        if ui.icon_button(self.wn, self.back_surf, (18, 24)) and m:
            self.game.temp_scene = None
            del self
            return

        ui.icon_button(self.wn, self.menu_surf, (284, 24))
