from typing import Final

WIDTH: Final[int] = 500
HEIGHT: Final[int] = 500
HALF_WIDTH: Final[int] = int(WIDTH // 2)
HALF_HEIGHT: Final[int] = int(HEIGHT // 2)
LINE_THICKNESS: Final[int] = int((WIDTH + HEIGHT) // 200)
FIELD_SIZE: Final[int] = int((WIDTH + HEIGHT) // 6)
PADDING: Final[int] = int((WIDTH + HEIGHT) // 100)

BG_COLOR: Final[tuple[int]] = (255, 255, 200)
BLACK: Final[tuple[int]] = (0, 0, 0)
RED: Final[tuple[int]] = (235, 0, 0)
GREEN: Final[tuple[int]] = (56, 155, 60)
GREY: Final[tuple[int]] = (100, 100, 100)
WHITE: Final[tuple[int]] = (247, 247, 247)

BUTTON_COLORS: Final[dict[dict[tuple[int]]]] = {
    'green': {'color': (56, 155, 60), 'hover_color': (76, 175, 80), 'shadow_color': (16, 115, 20), 'frame_color': (6, 95, 20)},
    'red': {'color': (235, 0, 0), 'hover_color': (255, 50, 50), 'shadow_color': (175, 0, 0), 'frame_color': (100, 0, 0)}
    }

BUTTON_WIDTH: Final[int] = HALF_WIDTH
BUTTON_HEIGHT: Final[int] = int(HEIGHT // 10)
AGAIN_RECT_X: Final[int] = int(HALF_WIDTH - BUTTON_WIDTH // 2)
AGAIN_RECT_Y: Final[int] = int(HALF_HEIGHT - BUTTON_HEIGHT // 2 + 40)
QUIT_RECT_X: Final[int] = int(HALF_WIDTH - BUTTON_WIDTH // 2)
QUIT_RECT_Y: Final[int] = FIELD_SIZE * 2 + 20
