import pygame as pg
import settings


image_path = 'images'
def load_image(image, width):
    img = pg.image.load(image_path  + '/' + image + '.png').convert_alpha()
    old_width = img.get_width()
    fac = width * 100 / old_width
    old_height = img.get_height()
    height = old_height * fac / 100 
    return pg.transform.smoothscale(img, (width, height))


class Button:
    def __init__(self, surf, text, center_pos, size, color):
        self.font = pg.font.SysFont('comicsans', 32)
        self.surf = surf
        self.text = text
    
        self.center_pos = list(center_pos)
        self.size = size
        self.color = color
        self.button_color = settings.BUTTON_COLORS[self.color]['color']
        self.button_elevation = 5
        self.button_rect = pg.Rect(self.center_pos[0] - self.size[0] // 2, self.center_pos[1] - self.size[1] // 2, *self.size)

    def render(self):
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['shadow_color'], self.button_rect, border_radius=5)
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['frame_color'], self.button_rect, width=2, border_radius=5)
        pg.draw.rect(self.surf, self.button_color, (self.button_rect[0], self.button_rect[1] - self.button_elevation, self.button_rect[2], self.button_rect[3]), border_radius=5)
        pg.draw.rect(self.surf, settings.BUTTON_COLORS[self.color]['frame_color'], (self.button_rect[0], self.button_rect[1] - self.button_elevation, self.button_rect[2], self.button_rect[3]), width= 2, border_radius=5)
        text_surf = self.font.render(self.text, True, settings.WHITE)
        self.surf.blit(text_surf, (settings.HALF_WIDTH - text_surf.get_width() // 2, self.button_rect[1] + settings.BUTTON_HEIGHT // 2 - text_surf.get_height() // 2 - 5 - self.button_elevation))

    def check_collision(self):
        mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            self.button_color = settings.BUTTON_COLORS[self.color]['hover_color']
            if pg.mouse.get_pressed()[0]:
                self.button_elevation = 0
                return True
            else:
                self.button_elevation = 5
                return None
        else:
            self.button_color = settings.BUTTON_COLORS[self.color]['color']