import pygame
import time


class TextData:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.w, self.h = x, y, width, height


class TextInputData:
    def __init__(self, rect, game, size=32, placeholder="Text input...", txt_color=(0, 0, 0),
                 placeholder_color=(100, 100, 100),
                 font=None, aa=True, bold=False, italic=False, bg_color=(255, 255, 255), hover_tint=3,
                 cursor_color=(0, 0, 0), cursor_width=4, border_radius=0, padding=30):
        self.rect = rect  # type: pygame.Rect
        self.game = game
        self.size = size  # type: int
        self.placeholder = placeholder  # type: str
        self.txt_color = txt_color
        self.placeholder_color = placeholder_color
        self.font = font  # type: str
        self.aa = aa  # type: bool
        self.bold = bold  # type: bool
        self.italic = italic  # type: bool
        self.bg_color = bg_color
        self.hover_tint = hover_tint  # type: int
        self.cursor_color = cursor_color
        self.cursor_width = cursor_width  # type: int
        self.border_radius = border_radius  # type: int
        self.padding = padding  # type: int


class TextInputReturn:
    def __init__(self, txt="", selected=False, text_pos=0, last_typed=0):
        self.txt = txt
        self.selected = selected
        self.text_pos = text_pos
        self.last_typed = last_typed


def text(wn, txt, position, size=32, color=(0, 0, 0), font=None, aa=True, align="top-left", bold=False,
         italic=False) -> None:

    surf = get_font(font, size, bold, italic).render(txt, aa, color)
    wn.blit(surf, align_font(position, align, surf))


def text_data(txt, position, size=32, font=None, align="top-left", bold=False, italic=False) -> TextData:
    surf = get_font(font, size, bold, italic).render(txt, False, (0, 0, 0))
    pos = align_font(position, align, surf)
    data = TextData(*pos, surf.get_width(), surf.get_height())
    return data


def get_font(name, size, bold=False, italic=False) -> pygame.font.Font:
    try:
        return pygame.font.Font(name, size)
    except FileNotFoundError:
        return pygame.font.SysFont(name, size, bold=bold, italic=italic)


def text_button(wn, txt, position, size=32, text_color=(0, 0, 0), bg_color=(255, 255, 255),
                bg_color_hover=(230, 230, 230),
                font=None, aa=True, align="top-left", padding=5, border_radius=0, bold=False, italic=False) -> bool:
    data = text_data(txt, position, size, font, align, bold, italic)
    rect = pygame.Rect(data.x - padding, data.y - padding, data.w + padding * 2, data.h + padding * 2)

    hover = rect.collidepoint(*pygame.mouse.get_pos())
    color = bg_color_hover if hover else bg_color

    pygame.draw.rect(wn, color, rect, border_radius=border_radius)
    text(wn, txt, position, size, text_color, font, aa, align, bold, italic)

    return hover


def icon_button(wn, surf, position, align="top-left", hover_tint=(5, 5, 5)) -> bool:
    icon = surf.copy()
    pos = align_font(position, align, icon)
    rect = pygame.Rect(*pos, *icon.get_size())
    hover = rect.collidepoint(*pygame.mouse.get_pos())

    if hover:
        icon.fill(hover_tint, special_flags=pygame.BLEND_RGB_SUB)

    wn.blit(icon, pos)
    return hover


def align_font(position, align, surf) -> list:
    pos = list(position)
    split = align.split("-")

    if split[0] == "bottom":
        pos[1] -= surf.get_height()
    elif split[0] == "center":
        pos[1] -= surf.get_height() / 2

    if split[1] == "right":
        pos[0] -= surf.get_width()
    elif split[1] == "center":
        pos[0] -= surf.get_width() / 2

    return pos


def text_input(wn, data: TextInputData, last: TextInputReturn) -> TextInputReturn:
    pygame.key.set_repeat(250, 50)

    mouse_pos = data.game.mouse_pos
    mouse_click = data.game.mouse_was_released
    mouse_hover = data.rect.collidepoint(mouse_pos)

    selected = last.selected
    txt = last.txt
    text_pos = last.text_pos
    last_typed = last.last_typed

    ###########################################################

    surf = pygame.Surface((data.rect.w, data.rect.h), pygame.SRCALPHA)
    surf.fill(data.bg_color)
    if mouse_hover:
        surf.fill([data.hover_tint]*3, special_flags=pygame.BLEND_RGB_SUB)

    border_radius = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(border_radius, (255, 255, 255, 255), (0, 0, *surf.get_size()),
                     border_radius=data.border_radius)
    surf.blit(border_radius, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    ###########################################################

    if txt == "":
        text(surf, data.placeholder, [data.padding]*2, data.size, data.placeholder_color, data.font, data.aa,
             "top-left", data.bold, data.italic)
    else:
        text(surf, txt, [data.padding]*2, data.size, data.txt_color, data.font, data.aa,
             "top-left", data.bold, data.italic)

    ###########################################################

    if mouse_click:
        selected = mouse_hover

    if selected:
        if time.time() % 1 < 0.4 or time.time() - last_typed < 0.4:
            # draw caret cursor
            cutoff = txt[:text_pos]
            text_data_cutoff = text_data(cutoff, [data.padding]*2, data.size, data.font, "top-left", data.bold, data.italic)
            pygame.draw.rect(surf, data.cursor_color, (data.padding + text_data_cutoff.w, data.padding, data.cursor_width, data.size))

        for event in data.game.events:
            if event.type == pygame.KEYDOWN:
                arr = list(txt)
                changed = False

                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    text_pos += (-(event.key == pygame.K_LEFT) + (event.key == pygame.K_RIGHT))
                    if text_pos < 0:
                        text_pos = 0
                    elif text_pos >= len(txt):
                        text_pos = len(txt)

                    changed = True

                elif event.key == pygame.K_BACKSPACE:
                    try:
                        arr.pop(text_pos - 1)
                        text_pos -= 1
                    except IndexError:
                        pass

                    changed = True

                elif event.key == pygame.K_DELETE:
                    try:
                        arr.pop(text_pos)
                    except IndexError:
                        pass

                    changed = True

                try:
                    is_char = 128 > ord(event.unicode) > 19
                except TypeError:
                    is_char = False

                if is_char and not changed:
                    unicode = event.unicode
                    arr.insert(text_pos, unicode)
                    text_pos += 1

                    changed = True

                if changed:
                    last_typed = time.time()

                txt = "".join(arr)

    ###########################################################

    wn.blit(surf, (data.rect.x, data.rect.y))

    return TextInputReturn(txt, selected, text_pos, last_typed)
