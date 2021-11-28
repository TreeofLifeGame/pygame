import json

import pygame


class JSON:
    @staticmethod
    def load(path) -> dict:
        with open(path) as f:
            return json.load(f)

    @staticmethod
    def dump(path, data) -> None:
        with open(path, "w") as f:
            json.dump(data, path)


class Fade:
    @staticmethod
    def fadein(game, render_func, **kwargs) -> None:
        surf = pygame.Surface(game.app_config["window_size"])
        surf.fill(game.app_colors["fade_color"])

        for alpha in range(0, 255, game.app_config["fade_step"]):
            surf.set_alpha(alpha)
            render_func(**kwargs)
            game.wn.blit(surf, (0, 0))
            pygame.display.update()
            pygame.time.delay(game.app_config["fade_wait"])

    @staticmethod
    def fadeout(game, render_func, **kwargs) -> None:
        surf = pygame.Surface(game.app_config["window_size"])
        surf.fill(game.app_colors["fade_color"])

        for alpha in range(255, 0, -game.app_config["fade_step"]):
            surf.set_alpha(alpha)
            render_func(**kwargs)
            game.wn.blit(surf, (0, 0))
            pygame.display.update()
            pygame.time.delay(game.app_config["fade_wait"])

    @staticmethod
    def transition(game, old_surf, render_func, **kwargs) -> None:
        surf = old_surf.copy()
        for alpha in range(255, 0, -game.app_config["fade_step"]):
            surf.set_alpha(alpha)
            render_func(**kwargs)
            game.wn.blit(surf, (0, 0))
            pygame.display.update()
            pygame.time.delay(game.app_config["fade_wait"])
