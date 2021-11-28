import pygame
import random

from typing import List
from os import PathLike

from src.scene import Scene, HelpScene
from src.object import Object
from src.speech_box import SpeechBox, TextLine


class JigsawScene(Scene):
    def __init__(self, game):
        super().__init__(game)

        self.progress = 0

        self.lines = pygame.image.load(game.image_map["lines0"]).convert_alpha()
        self.characters = [
            pygame.image.load(game.image_map["character"][2]).convert_alpha()
        ]

        self.help = HelpScene(game, pygame.image.load(game.image_map["drag_object"]).convert_alpha())

        color = game.app_colors["main_font"]

        self.speeches = [
            SpeechBox(game, [
                TextLine("Play the puzzle to see the", color=color),
                TextLine("picture!", color=color),
            ], (134, 650), bg_color=game.app_colors["speech_bubble_bg"]),
        ]

        self.jigsaw = Jigsaw(self.game, self.game.image_map["jigsaw"], (50, 50), self.game.app_config["jigsaw_divide"], 1.3)
        load = self.jigsaw.full
        self.jigsaw.position = (self.game.app_config["window_size"][0] / 2 - load.get_width() / 2,
                                self.game.app_config["jigsaw_y_pos"])

    def update(self) -> None:
        self.jigsaw.update()

    def render(self) -> None:
        self.wn.fill(self.game.app_colors["main_bg"])
        self.wn.blit(self.lines, (0, 262))

        self.jigsaw.render()

        self.wn.blit(self.characters[self.progress], (-28, 603))

        self.speeches[self.progress].render()


class Jigsaw(Object):
    # the whole point of the reversed list is to allow this intuitive design:
    #   - when you click on a piece, it pops to the front of the view
    #   - when you click on top of multiple pieces, it always selects the top piece

    def __init__(self, game, photo, position, divide=3, scale=1.0):
        super(Jigsaw, self).__init__(game)

        self.position = position
        self.completed = 0
        # region creating pieces
        scatter = self.game.app_config["jigsaw_spawn_scatter"]

        self.pieces = []
        self.pieces_reversed = []

        full = pygame.image.load(photo).convert()
        size = full.get_size()
        full = pygame.transform.scale(full, (size[0] * scale, size[1] * scale))

        self.full = full

        pieces = []
        sub_size = (int(size[0] / divide * scale), int(size[1] / divide * scale))

        for y in range(0, size[1] - 1, sub_size[1]):
            for x in range(0, size[0] - 1, sub_size[0]):
                rect = pygame.Rect(x, y, *sub_size)

                try: pieces.append([full.subsurface(rect).convert_alpha(),
                                    rect])
                except ValueError: pass

        for index, img_data in enumerate(pieces):
            img = img_data[0]
            rect = img_data[1]

            b = JigsawBorder(
                top=rect[1] == 0,
                right=rect[0] >= full.get_size()[0] - sub_size[0] - 2,
                bottom=rect[1] >= full.get_size()[1] - sub_size[1] - 2,
                left=rect[0] == 0
            )

            self.pieces.append(JigsawPiece(
                game,
                img,
                (random.randint(207 - scatter/2, 207 + scatter/2),
                 random.randint(207 - scatter/2, 207 + scatter/2)),
                self,
                rect[0:2],
                border=b,
                snap_dist=20
            ))

        self.cache_reversed()
        # endregion

        # region creating visible grid reference
        self.grid_surf = pygame.Surface(full.get_size(), pygame.SRCALPHA)
        self.grid_surf.fill(self.game.app_colors["jigsaw_grid_bg"])
        self.grid_surf.fill((255, 255, 255, self.game.app_colors["jigsaw_bg_alpha"]), None, pygame.BLEND_RGBA_MULT)

        for i in range(divide + 1):
            y = i * sub_size[1]
            coords = [[0, y], [full.get_width(), y]]

            if i == divide:
                coords[0][1] = full.get_height() - self.game.app_config["jigsaw_outline_size"]
                coords[1][1] = full.get_height() - self.game.app_config["jigsaw_outline_size"]

            pygame.draw.line(self.grid_surf, self.game.app_colors["jigsaw_grid_outline"], *coords,
                             self.game.app_config["jigsaw_outline_size"])

        for i in range(divide + 1):
            x = i * sub_size[0]
            coords = [[x, 0], [x, full.get_height()]]

            if i == divide:
                coords[0][0] = full.get_width() - self.game.app_config["jigsaw_outline_size"]
                coords[1][0] = full.get_width() - self.game.app_config["jigsaw_outline_size"]

            pygame.draw.line(self.grid_surf, self.game.app_colors["jigsaw_grid_outline"], *coords,
                             self.game.app_config["jigsaw_outline_size"])

        # endregion

        self.selected = None

    def update(self) -> None:
        for piece in self.pieces:
            piece.update()

        x, y = self.pieces_reversed[-1].position[0] - self.position[0], self.pieces_reversed[-1].position[1] - self.position[1]
        sx, sy = self.pieces_reversed[-1].snap

    def render(self) -> None:
        self.wn.blit(self.grid_surf, self.position)

        for piece in self.pieces_reversed:
            piece.render()

    def cache_reversed(self) -> None:
        self.pieces_reversed = self.pieces.copy()
        self.pieces_reversed.reverse()


class JigsawBorder:
    def __init__(self, top=False, right=False, bottom=False, left=False):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left


class JigsawPiece(Object):
    def __init__(self, game, surf, position, jigsaw, snap, hover_tint=10, border: JigsawBorder = None,
                 snap_dist=10):
        super(JigsawPiece, self).__init__(game)

        self.surface = surf
        self.position = position
        self.jigsaw = jigsaw
        self.border = border
        self.snap = snap
        self.snap_dist = snap_dist

        self.render_borders(self.surface)

        self.hover_surf = self.surface.copy()
        self.hover_surf.fill([hover_tint] * 3, special_flags=pygame.BLEND_RGB_SUB)

        self.hover = False
        self.in_position = False

    def render(self) -> None:
        check = self.hover and (self.jigsaw.selected is None or self.jigsaw.selected is self)
        self.wn.blit(self.hover_surf if check else self.surface, self.position)

    def update(self) -> None:
        if self.in_position:
            return

        mouse_pressed = self.game.mouse_down
        mouse_coords = self.game.mouse_pos
        mouse_rel = self.game.mouse_rel

        self.hover = self.check_collide(mouse_coords)

        if self.jigsaw.selected is None:  # no piece is already selected
            if self.hover:
                if mouse_pressed:
                    # the mouse is clicked on the puzzle piece
                    self.jigsaw.selected = self
                    self.jigsaw.pieces.remove(self)
                    self.jigsaw.pieces.insert(0, self)
                    self.jigsaw.cache_reversed()

        elif not mouse_pressed:  # a.k.a. we just stopped holding down on the piece
            # let go
            self.jigsaw.selected = None
        elif self.jigsaw.selected is self:
            # this piece is currently being dragged around and is selected
            self.position = (self.position[0] + mouse_rel[0], self.position[1] + mouse_rel[1])

        if self.check_snap() and not mouse_pressed:
            self.in_position = True
            self.position = self.snap[0] + self.jigsaw.position[0], self.snap[1] + self.jigsaw.position[1]
            self.hover = False

            self.jigsaw.pieces.remove(self)
            self.jigsaw.pieces.insert(len(self.jigsaw.pieces), self)
            self.jigsaw.cache_reversed()

            self.jigsaw.completed += 1

            if self.jigsaw.completed == len(self.jigsaw.pieces):
                self.game.scene += 1

    def check_snap(self) -> bool:
        x, y = self.position[0] - self.jigsaw.position[0], self.position[1] - self.jigsaw.position[1]

        sx, sy = self.snap
        sd = self.snap_dist

        return (sx - sd <= x <= sx + sd) and (sy - sd <= y <= sy + sd)

    def check_collide(self, point) -> bool:
        return pygame.Rect(*self.position, *self.surface.get_size()).collidepoint(*point)

    def render_borders(self, surf) -> None:
        b = self.border
        s = self.game.app_config["jigsaw_outline_size"]

        args = (surf, self.game.app_colors["jigsaw_outline"])

        # subtracting 's' because pygame draws from top-left meaning the line would not actually
        # display on the surface as it would be cut off
        tl = (0, 0)
        tr = (surf.get_width() - s, 0)
        bl = (0, surf.get_height() - s)
        br = (surf.get_width() - s, surf.get_height() - s)

        if b.top:
            pygame.draw.line(*args, tl, (tr[0] + s, tr[1]), s)
        if b.right:
            pygame.draw.line(*args, tr, (br[0], br[1] + s), s)
        if b.bottom:
            pygame.draw.line(*args, bl, (br[0] + s, br[1]), s)
        if b.left:
            pygame.draw.line(*args, tl, (bl[0], bl[1] + s), s)

        border_radius = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(border_radius, (255, 255, 255, 255), (0, 0, *surf.get_size()),
                         border_radius=self.game.app_config["jigsaw_border_radius"])
        surf.blit(border_radius, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
