WIDTH = HEIGHT = 500
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
LINE_THIKNESS = (WIDTH + HEIGHT) // 200
FIELD_SIZE = (WIDTH + HEIGHT) // 6
PADDING = (WIDTH + HEIGHT) // 100

BG_COLOR = (255, 255, 200)
BLACK = (0, 0, 0)
RED =  (235, 0, 0)
GREEN = (56, 155, 60)
GREY = (100, 100, 100)
WHITE = (247, 247, 247)

BUTTON_COLORS = {
    'green': {'color': (56, 155, 60), 'hover_color': (76, 175, 80), 'shadow_color': (16, 115, 20), 'frame_color': (6, 95, 20)},
    'red': {'color': (235, 0, 0), 'hover_color': (255, 50, 50), 'shadow_color': (175, 0, 0), 'frame_color': (100, 0, 0)}
    }

BUTTON_WIDTH = HALF_WIDTH
BUTTON_HEIGHT = HEIGHT // 10
AGAIN_RECT_X = HALF_WIDTH - BUTTON_WIDTH // 2
AGAIN_RECT_Y = HALF_HEIGHT - BUTTON_HEIGHT // 2 + 40
QUIT_RECT_X = HALF_WIDTH - BUTTON_WIDTH // 2
QUIT_RECT_Y = FIELD_SIZE * 2 + 20
