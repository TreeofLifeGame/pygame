import pygame

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
import src.ui as ui


class TellUsScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        def progress():
            game.scene += 1

        self.characters = [
            pygame.image.load(game.image_map["character"][0]).convert_alpha()
        ]

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.sparkles = pygame.image.load(game.image_map["sparkles1"]).convert_alpha()

        self.help = HelpScene(game, pygame.image.load(game.image_map["tap_white"]).convert_alpha())

        color = game.app_colors["main_font"]

        self.speech = SpeechBox(game, [
            TextLine("Talk to a parent or", color=color, bold=True),
            TextLine("guardian about what you", color=color, bold=True),
            TextLine("think happens when a", color=color, bold=True),
            TextLine("person or animal leaves", color=color, bold=True),
            TextLine("there living body.", color=color, bold=True)
        ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"], button=True, button_callback=progress)

        self.txt_inp_data = ui.TextInputData(
            pygame.Rect(20, 300, self.game.app_config["window_size"][0] - 40, 50),
            self.game,
            16,
            "Enter your answer or thoughts here...",
            game.app_colors["textbox_text"],
            game.app_colors["textbox_placeholder"],
            game.app_fonts["regular"],
            True,
            False,
            False,
            game.app_colors["textbox_bg"],
            3,
            game.app_colors["main_font"],
            2,
            20,
            15
        )

        self.last_txt_return = ui.TextInputReturn()

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])
        self.wn.blit(self.lines, (0, 262))
        self.wn.blit(self.sparkles, (58, 216))

        self.last_txt_return = ui.text_input(self.wn, self.txt_inp_data, self.last_txt_return)

        self.wn.blit(self.characters[0], (-28, 603))
        self.speech.render()
