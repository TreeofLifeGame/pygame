import pygame
import sys

from src.helpers import JSON, Fade
from src.scene import Scene

import src.ui as ui

from scenes.welcome_scene import WelcomeScene
from scenes.jigsaw_scene import JigsawScene
from scenes.jigsaw_complete_scene import JigsawCompleteScene
from scenes.dead_plant_scene import DeadPlantScene
from scenes.tell_us_scene import TellUsScene
from scenes.drag_down_scene import DragDownScene
from scenes.drag_down_complete_scene import DragDownCompleteScene
from scenes.menu_scene import MenuScene


class Game:
    def __init__(self):
        self.app_config = JSON.load("data/app_config.json")
        self.image_map = JSON.load("data/image_map.json")
        self.app_colors = JSON.load("data/app_colors.json")
        self.app_fonts = JSON.load("data/app_fonts.json")

        self.wn = pygame.display.set_mode(self.app_config["window_size"])
        pygame.display.set_caption(self.app_config["window_title"])

        self.clock = pygame.time.Clock()
        self.fps = self.app_config["window_fps"]

        self.leaf_points = 0

        self.scenes = [
            WelcomeScene(self),
            JigsawScene(self),
            JigsawCompleteScene(self),
            DeadPlantScene(self),
            TellUsScene(self),
            DragDownScene(self),
            DragDownCompleteScene(self)
        ]

        self.scene = 0
        self.temp_scene = None  # type: Scene

        pygame.mouse.set_cursor(pygame.cursors.diamond)

        self._was_mouse_down = False
        self._old_scene = self.scene
        self._old_temp_scene = self.temp_scene

        self.danger_icon = pygame.image.load(self.image_map["danger0"]).convert_alpha()
        self.volume_off = pygame.image.load(self.image_map["volume_off"]).convert_alpha()
        self.volume_on = pygame.image.load(self.image_map["volume_on"]).convert_alpha()
        self.menu_button = pygame.image.load(self.image_map["menu"]).convert_alpha()

        self.volume_toggle = True

        self.mouse_pos = (0, 0)
        self.mouse_down = False
        self.mouse_rel = (0, 0)

        self.mouse_was_released = False
        self.mouse_was_pressed = False

        self.events = []

    def run(self) -> None:
        self.clock.tick(self.fps)

        while True:
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    self.exit()

            self.update(self.scene)
            self.render(self.scene)
            pygame.display.update()

    def render(self, target) -> None:
        if self.temp_scene is None:
            self.scenes[target].render()

            m = self.mouse_was_released

            if ui.icon_button(self.wn, self.danger_icon, (17, 25)) and m:
                self.load_temp_scene(self.scenes[target].help)

            if ui.icon_button(self.wn, self.volume_on if self.volume_toggle else self.volume_off, (68, 29)) and m:
                self.volume_toggle = not self.volume_toggle

            if ui.icon_button(self.wn, self.menu_button, (284, 24)) and m:
                self.load_temp_scene(MenuScene(self))

        else:
            self.temp_scene.render()

    def update(self, target) -> None:
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_rel = pygame.mouse.get_rel()
        self.mouse_down = pygame.mouse.get_pressed(3)[0]

        self.mouse_was_pressed = self.mouse_down and not self._was_mouse_down
        self.mouse_was_released = not self.mouse_down and self._was_mouse_down

        if self.temp_scene is None:
            try:
                self.scenes[target].update()
            except IndexError:
                print("either something went wrong, or the app has finished all of its levels.")
                sys.exit()
        else:
            self.temp_scene.update()

        if self._old_scene != self.scene:
            # we just transitioned scene
            Fade.transition(self, self.wn, self.render, target=self.scene)

        if self._old_temp_scene != self.temp_scene and self.temp_scene is not None:
            # we just transitioned temp scene
            Fade.transition(self, self.wn, self.render, target=self.temp_scene)
        elif self._old_temp_scene != self.temp_scene:
            # we just closed a temp scene
            Fade.transition(self, self.wn, self.render, target=self.scene)

        self._was_mouse_down = self.mouse_down

        self._old_scene = self.scene
        self._old_temp_scene = self.temp_scene

    def load_temp_scene(self, scene: Scene):
        self.temp_scene = scene

    def exit(self) -> None:
        self.scenes[self.scene].exit()
        pygame.quit()
        sys.exit()
