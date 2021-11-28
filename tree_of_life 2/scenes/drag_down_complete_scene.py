import pygame

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
from src.leaf_dialogue import SuperLeafDialogue
import src.ui as ui


class DragDownCompleteScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.sparkles = pygame.image.load(game.image_map["sparkles1"]).convert_alpha()
        self.characters = [
            pygame.image.load(game.image_map["character"][3]).convert_alpha()
        ]

        self.help = HelpScene(game, pygame.image.load(game.image_map["collect_your_reward"]).convert_alpha())

        color = game.app_colors["main_font"]

        self.speech = SpeechBox(game, [
            TextLine("What! You did it again?!", color=color),
            TextLine("Collect points to unlock", color=color, bold=True, offset=10),
            TextLine("some really cool games", color=color, bold=True),
            TextLine("and activities!", color=color, bold=True)
        ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"])

        self.flower = pygame.image.load(game.image_map["flower"][4]).convert_alpha()
        self.dialogue = SuperLeafDialogue(self.game, 5, 300, self.game.app_colors["super_leaf_dialogue"], 20)

    def update(self) -> None:
        pass

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])

        self.wn.blit(self.lines, (0, 262))
        self.wn.blit(self.sparkles, (58, 216))
        self.wn.blit(self.characters[0], (-28, 603))
        self.wn.blit(self.flower, (62, -26))

        self.dialogue.render()
        self.speech.render()
