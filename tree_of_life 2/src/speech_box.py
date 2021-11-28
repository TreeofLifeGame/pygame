import pygame
import src.ui as ui

from typing import List
from src.object import Object


class TextLine:
    def __init__(self, txt, bold=False, color=(0, 0, 0), offset=0):
        self.text = txt
        self.bold = bold
        self.color = color
        self.offset = offset


class SpeechBox(Object):
    def __init__(self, game, text_lines: List[TextLine], position, size=18, line_height=6, bg_color=(255, 255, 255),
                 button=False, button_callback=None):
        super(SpeechBox, self).__init__(game)

        self.text = text_lines
        self.position = position
        self.button = button
        self.button_callback = button_callback

        self.button_surf = pygame.image.load(self.game.image_map["next0"]).convert_alpha()

        rad = game.app_config["speech_bubble_border_radius"]
        padding = game.app_config["speech_bubble_padding"]
        speech_space = game.app_config["speech_bubble_point_size"]

        max_width = 0
        height = padding
        increment = size + line_height

        # get height and max width of all lines
        for index, line in enumerate(text_lines):
            f = game.app_fonts["bold" if line.bold else "regular"]
            data = ui.text_data(line.text, position, size, f)
            max_width = data.w if data.w > max_width else max_width
            height += increment + line.offset

        if button:
            height += 30

        self.height = height

        # create the speech surface
        max_width += padding * 2
        self.surf = pygame.Surface((max_width + speech_space, height + speech_space + padding), pygame.SRCALPHA)
        pygame.draw.rect(self.surf, bg_color, (speech_space, 0, max_width, height + padding),
                         border_top_left_radius=rad,
                         border_top_right_radius=rad,
                         border_bottom_right_radius=rad)

        # draw the sticky-outey bit at the bottom left
        pygame.draw.polygon(self.surf, bg_color, [
            (0, self.surf.get_height()),
            (speech_space, self.surf.get_height() - speech_space * 2),
            (speech_space * 2, self.surf.get_height() - speech_space)
        ])

        offsets = 0  # to make sure all lines after an offset get spaced properly
        for index, line in enumerate(text_lines):
            offsets += line.offset

            f = game.app_fonts["bold" if line.bold else "regular"]
            y = (index * increment + offsets) + padding
            ui.text(self.surf, line.text, (padding + speech_space, y), size, line.color, f)

    def render(self) -> None:
        self.game.wn.blit(self.surf, (self.position[0], self.position[1] - self.surf.get_height()))

        if self.button:
            pos = self.position
            hovered = ui.icon_button(self.wn, self.button_surf, (pos[0] + 100, pos[1] - 10), "center-left", (5, 5, 5))

            if self.button_callback is not None and hovered and self.game.mouse_was_released:
                self.button_callback()
