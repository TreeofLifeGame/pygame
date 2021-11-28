import pygame

from src.object import Object
import src.ui as ui


class SuperLeafDialogue(Object):
    def __init__(self, game, amount, y_pos=300, color=(255, 234, 158), padding=20):
        super(SuperLeafDialogue, self).__init__(game)

        self.background = pygame.Surface((self.game.app_config["window_size"][0] - padding * 2,
                                          self.game.app_config["super_leaf_dialogue_height"]), pygame.SRCALPHA)
        size = self.background.get_size()
        pygame.draw.rect(self.background, color, (0, 0, *size),
                         border_radius=self.game.app_config["super_leaf_dialogue_border_radius"])

        ui.text(self.background, f"You earned {amount} super leaves!", (size[0] / 2, 50), 23,
                self.game.app_colors["super_leaf_dialogue_font"], self.game.app_fonts["bold"], True, "top-center", True)

        self.pos = (padding, y_pos)
        self.button_surf = pygame.image.load(self.game.image_map["collect_reward"]).convert_alpha()

    def render(self) -> None:
        self.wn.blit(self.background, self.pos)

        hover = ui.icon_button(self.wn, self.button_surf, (self.game.app_config["window_size"][0] / 2,
                                                           self.pos[1] + 130), "center-center")
        if hover and self.game.mouse_was_released:
            self.game.scene += 1
            self.game.leaf_points += 5
