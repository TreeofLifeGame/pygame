import pygame

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
from src.leaf_dialogue import SuperLeafDialogue

import src.ui as ui


class DeadPlantScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.progress = 0

        def progress():
            self.progress += 1

            if self.progress == 1:
                self.help.img = pygame.image.load(game.image_map["tap_on_object"]).convert_alpha()

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.characters = [
            pygame.image.load(game.image_map["character"][4]).convert_alpha()
        ]

        self.plants = [
            pygame.image.load(game.image_map["dead_plant0"]).convert_alpha(),
            pygame.image.load(game.image_map["dead_plant1"]).convert_alpha()
        ]

        self.help = HelpScene(game, pygame.image.load(game.image_map["tap_next"]).convert_alpha())

        color = game.app_colors["main_font"]

        self.speeches = [
            SpeechBox(game, [
                TextLine("Sometimes, like a plant,", color=color),
                TextLine("we don't get to fully grow.", color=color),
                TextLine("Living beings can die from", color=color),
                TextLine("an illness, accident or", color=color),
                TextLine("simply because of age...", color=color)
            ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"], button=True, button_callback=progress),

            SpeechBox(game, [
                TextLine("What do you think", color=color),
                TextLine("happens to the body when", color=color),
                TextLine("someone or a living being", color=color),
                TextLine("dies?", color=color),
                TextLine("Tap on the dead plant to", color=color, bold=True, offset=10),
                TextLine("give us your answer!", color=color, bold=True)
            ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"])
        ]

        self.plant_rect = self.plants[1].get_rect()

    def update(self) -> None:
        if self.progress == 1:
            # "click on the dead plant to give us your answer"

            if self.plant_rect.collidepoint(*pygame.mouse.get_pos()):
                if self.game.mouse_was_released:
                    self.game.scene += 1

    def render(self) -> None:
        self.plant_rect.y = self.game.app_config["window_size"][1] - self.plants[self.progress].get_height()

        self.wn.fill(self.game.app_colors["main_bg"])

        self.wn.blit(self.lines, (0, 262))
        self.wn.blit(self.plants[self.progress], self.plant_rect.topleft)
        self.wn.blit(self.characters[0], (-28, 603))

        self.speeches[self.progress].render()

