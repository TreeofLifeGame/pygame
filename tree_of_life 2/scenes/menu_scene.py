import pygame

from src.scene import Scene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
import src.ui as ui


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.sparkles = pygame.image.load(game.image_map["sparkles2"]).convert_alpha()
        self.character = pygame.image.load(game.image_map["character"][5]).convert_alpha()

        self.sign_up = pygame.image.load(game.image_map["sign_up"]).convert_alpha()
        self.log_in = pygame.image.load(game.image_map["log_in"]).convert_alpha()
        self.about = pygame.image.load(game.image_map["about"]).convert_alpha()
        self.return_to_game = pygame.image.load(game.image_map["return_to_game"]).convert_alpha()

        self.leaf_count_surf = pygame.Surface((331, 72), pygame.SRCALPHA)
        pygame.draw.rect(self.leaf_count_surf, self.game.app_colors["point_count_bg"], (0, 0, 331, 72), border_radius=7)
        ui.text(self.leaf_count_surf, f"You have {self.game.leaf_points} points", (166, 36), 28, self.game.app_colors["point_count_font"], self.game.app_fonts["bold"], True, "center-center")

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])

        self.wn.blit(self.lines, (0, 262))
        self.wn.blit(self.sparkles, (76, 323))
        self.wn.blit(self.character, (113, 329))

        self.wn.blit(self.leaf_count_surf, (43, 90))

        ui.icon_button(self.wn, self.sign_up, (65, 441))
        ui.icon_button(self.wn, self.log_in, (65, 505))
        ui.icon_button(self.wn, self.about, (65, 569))

        if ui.icon_button(self.wn, self.return_to_game, (65, 633)) and self.game.mouse_was_released:
            self.game.temp_scene = None

        kwargs = {
            "wn": self.wn,
            "size": 18,
            "color": self.game.app_colors["main_font"],
            "font": self.game.app_fonts["bold"],
            "align": "top-center"
        }
        x = self.game.app_config["window_size"][0]/2

        lines = [
            "Create an account to save your points!",
            "By earning points you can unlock new",
            "green adventures, games, and much",
            "more...See you inside!"
        ]

        for index, line in enumerate(lines):
            ui.text(txt=line, position=(x, 200 + (index * 23)), **kwargs)
