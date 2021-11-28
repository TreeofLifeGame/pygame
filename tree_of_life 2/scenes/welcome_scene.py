import pygame

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
import src.ui as ui


class WelcomeScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.progress = 0

        def progress() -> None:
            self.progress += 1

            if self.progress >= len(self.speeches):
                # completed welcome screen
                self.game.scene += 1

        self.egg = Egg(game, [115, 255], game.image_map["egg0"], click_callback=progress)
        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.sparkles = pygame.image.load(game.image_map["sparkles0"]).convert_alpha()
        self.characters = [
            pygame.image.load(game.image_map["character"][0]).convert_alpha(),
            pygame.image.load(game.image_map["character"][1]).convert_alpha()
        ]

        color = game.app_colors["main_font"]

        self.speeches = [
            SpeechBox(game, [
                TextLine("Welcome!", color=color),
                TextLine("What is tree of life?", color=color),
                TextLine("Tap the egg to find out!", color=color, bold=True, offset=10)
            ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"]),
            SpeechBox(game, [
                TextLine("The tree of life is a", color=color),
                TextLine("never-ending cycle that", color=color),
                TextLine("lives through the memories", color=color),
                TextLine("of those who have lost a", color=color),
                TextLine("loved one.", color=color),
                TextLine("Shake the egg!", color=color, bold=True, offset=10)
            ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"]),
        ]

        self.help = HelpScene(game, pygame.image.load(game.image_map["tap_on_object"]).convert_alpha())

    def update(self) -> None:
        self.egg.update()

    def render(self) -> None:
        try:
            self.wn.fill(self.game.app_colors["main_bg"])

            self.wn.blit(self.lines, (0, 262))
            self.wn.blit(self.sparkles, (58, 216))
            self.wn.blit(self.characters[self.progress], (-28, 603))

            ui.text(self.wn, "Tree of Life", [self.wn.get_width()/2, 122], 36, self.game.app_colors["main_font"],
                    self.game.app_fonts["bold"], align="top-center")

            self.egg.render()
            self.speeches[self.progress].render()
        except IndexError:
            pass


class Egg(Object):
    def __init__(self, game, pos, img, hover_brightness=10, click_callback=None):
        super(Egg, self).__init__(game)

        self.img = pygame.image.load(img).convert_alpha()
        self.pos = pos
        self.hover_brightness = hover_brightness
        self.click_callback = click_callback

        self.bounds = pygame.Rect(*self.pos, *self.img.get_size())
        self.hover_img = self.img.copy()
        self.hover_img.fill([hover_brightness]*3, special_flags=pygame.BLEND_RGB_SUB)
        self.click_count = 0
        self.hover = False

    def load_img(self, path) -> None:
        self.img = pygame.image.load(path).convert_alpha()
        self.bounds = pygame.Rect(*self.pos, *self.img.get_size())
        self.hover_img = self.img.copy().fill([self.hover_brightness]*3, special_flags=pygame.BLEND_RGB_ADD)

    def render(self) -> None:
        self.game.wn.blit(self.img if not self.hover else self.hover_img, self.pos)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed(3)[0]

        self.hover = self.bounds.collidepoint(*mouse_pos)

        # this code checks if you have clicked the egg, and if you have, it will run the callback function
        if self.hover and self.game.mouse_was_released:
            self.click_count += 1

            if self.click_callback is not None:
                self.click_callback()
