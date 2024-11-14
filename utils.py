import pygame as pg
import settings

from typing import Final


image_path = 'images'
def load_image(image: str, width: int) -> pg.Surface:
    """
    Load an image from the image_path directory and resize it to the specified width.
    Args:
    image (str): The name of the image file.
    width (int): The desired width of the image.
    Returns:
    pg.Surface: The loaded and resized image.
    """
    img = pg.image.load(image_path  + '/' + image + '.png').convert_alpha()
    old_width = img.get_width()
    fac = width * 100 / old_width
    old_height = img.get_height()
    height = old_height * fac / 100 
    return pg.transform.smoothscale(img, (width, height))


class Button:
    BUTTON_ELEVATION: Final[int] = 5

    def __init__(self, surf: pg.Surface, text: str, center_pos: tuple[int], size: tuple[int], color: str) -> None:
        """
        Initialize a button on the specified surface, with the specified text, center position, size, and color.
        Args:
        surf (pg.Surface): The surface to draw the button on.
        text (str): The text to display on the button.
        center_pos (tuple[int]): The center position of the button.
        size (tuple[int]): The size of the button.
        color (str): The color of the button. (green or red)
        """
        self.font: pg.font.Font = pg.font.SysFont('comicsans', 32)
        self.surf: pg.Surface = surf
        self.text: str = text
    
        self.center_pos: tuple[int] = center_pos
        self.size: tuple[int] = size
        self.color: str = color
        self.button_color: tuple[int] = settings.BUTTON_COLORS[self.color]['color']
        self.elevation: int = self.BUTTON_ELEVATION
        self.button_rect: pg.Rect = pg.Rect(self.center_pos[0] - self.size[0] // 2, self.center_pos[1] - self.size[1] // 2, *self.size)

    def render(self) -> None:
        """ Render the button on the surface. """
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['shadow_color'], self.button_rect, border_radius=5)
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['frame_color'], self.button_rect, width=2, border_radius=5)
        pg.draw.rect(self.surf, self.button_color, (self.button_rect[0], self.button_rect[1] - self.button_elevation, self.button_rect[2], self.button_rect[3]), border_radius=5)
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['frame_color'], (self.button_rect[0], self.button_rect[1] - self.button_elevation, self.button_rect[2], self.button_rect[3]), width= 2, border_radius=5)
        text_surf: pg.Surface = self.font.render(self.text, True, settings.WHITE)
        self.surf.blit(text_surf, (settings.HALF_WIDTH - text_surf.get_width() // 2, self.button_rect[1] + settings.BUTTON_HEIGHT // 2 - text_surf.get_height() // 2 - 5 - self.button_elevation))

    def check_collision(self) -> None | bool:
        """
        Check if the mouse is hovering over the button and if this button is pressed.
        Returns:
        bool: True if the button is pressed, otherwise None.
        """
        mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.button_color = settings.BUTTON_COLORS[self.color]['hover_color']
            if pg.mouse.get_pressed()[0]:
                self.elevation = 0
                return True
            else:
                self.elevation = self.BUTTON_ELEVATION
                return None
        else:
            self.button_color = settings.BUTTON_COLORS[self.color]['color']