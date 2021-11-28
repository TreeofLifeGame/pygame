import pygame
import math

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine
import src.ui as ui


class DragDownScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        def progress():
            self.progress += 1

            if self.progress == 3:
                self.drag_down.activated = False
                self.help.img = pygame.image.load(game.image_map["tap_next"]).convert_alpha()

            if self.progress == 4:
                self.game.scene += 1
                self.progress = 3

        self.progress = 0

        self.characters = [
            pygame.image.load(game.image_map["character"][1]).convert_alpha()
        ]
        self.flowers = [
            [pygame.image.load(game.image_map["flower"][0]).convert_alpha(), (136, 288)],
            [pygame.image.load(game.image_map["flower"][1]).convert_alpha(), (134, 258)],
            [pygame.image.load(game.image_map["flower"][2]).convert_alpha(), (134, 258)],
            [pygame.image.load(game.image_map["flower"][3]).convert_alpha(), (76, 135)]
        ]

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.drag_down = DragDown(self.game, pygame.image.load(game.image_map["decompose0"]), (47, 96), progress, 4)

        self.help = HelpScene(game, pygame.image.load(game.image_map["drag_down"]).convert_alpha())

        color = game.app_colors["main_font"]

        self.speeches = [
            SpeechBox(game, [
                TextLine("The physical body of any", color=color),
                TextLine("living being will break", color=color),
                TextLine("down when it dies. It will", color=color),
                TextLine("return into the soil as", color=color),
                TextLine("nutrients that feed the", color=color),
                TextLine("bacteria in soil and new", color=color),
                TextLine("plants growing from it.", color=color),
                TextLine("Follow the arrow direction", color=color, bold=True),
                TextLine("and drag down!", color=color, bold=True),
            ], (134, 715), bg_color=game.app_colors["speech_bubble_bg"]),

            SpeechBox(game, [
                TextLine("The physical body of any", color=color),
                TextLine("living being will break", color=color),
                TextLine("down when it dies. It will", color=color),
                TextLine("return into the soil as", color=color),
                TextLine("nutrients that feed the", color=color),
                TextLine("bacteria in soil and new", color=color),
                TextLine("plants growing from it.", color=color),
                TextLine("Follow the arrow direction", color=color, bold=True),
                TextLine("and drag down!", color=color, bold=True),
            ], (134, 715), bg_color=game.app_colors["speech_bubble_bg"]),

            SpeechBox(game, [
                TextLine("The physical body of any", color=color),
                TextLine("living being will break", color=color),
                TextLine("down when it dies. It will", color=color),
                TextLine("return into the soil as", color=color),
                TextLine("nutrients that feed the", color=color),
                TextLine("bacteria in soil and new", color=color),
                TextLine("plants growing from it.", color=color),
                TextLine("Follow the arrow direction", color=color, bold=True),
                TextLine("and drag down!", color=color, bold=True),
            ], (134, 715), bg_color=game.app_colors["speech_bubble_bg"]),

            SpeechBox(game, [
                TextLine("Wow! Living beings that", color=color),
                TextLine("die will give new life to", color=color),
                TextLine("other beings no matter", color=color),
                TextLine("how big or small!", color=color),
            ], (134, 715), bg_color=game.app_colors["speech_bubble_bg"], button=True, button_callback=progress),
        ]

    def update(self) -> None:
        self.drag_down.update()

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])
        self.wn.blit(self.lines, (0, 262))

        self.wn.blit(self.flowers[self.progress][0], self.flowers[self.progress][1])
        pygame.draw.rect(self.wn, self.game.app_colors["dirt"], (0, 456, *self.game.app_config["window_size"]))

        self.drag_down.render()

        self.wn.blit(self.characters[0], (-28, 603))

        self.speeches[self.progress].render()


class DragDown(Object):
    def __init__(self, game, surf, position, callback=None, activation_speed=5):
        super(DragDown, self).__init__(game)

        self.surf = surf
        self.position = position
        self.activation_speed = activation_speed
        self.callback = callback

        self.rect = pygame.Rect(*self.position, *self.surf.get_size())
        self.checking = False

        self.activated = True

    def update(self) -> None:
        if not self.activated:
            return

        if self.game.mouse_was_pressed and self.rect.collidepoint(self.game.mouse_pos):
            self.checking = True

        if self.checking:
            rel = self.game.mouse_rel

            if rel[1] > 0:
                speed = math.hypot(*rel)

                if speed >= self.activation_speed:
                    if self.callback is not None: self.callback()
                    self.checking = False

        if self.game.mouse_was_released:
            self.checking = False

    def render(self) -> None:
        if not self.activated:
            return

        self.wn.blit(self.surf, self.position)
