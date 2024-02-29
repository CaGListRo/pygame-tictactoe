import pygame as pg
import settings
from utils import load_image


class Game:
    def __init__(self):
        pg.init()

        self.window = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.font = pg.font.SysFont('comicsans', 32)

        self.clock = pg.time.Clock()
        self.running = True
        self.won = False
        self.player = 1
        self.clicked = False
        self.mouse_pos = (-1, -1)
        self.again_question = True
        self.move_counter = 0
        self.tie = False
        
        self.playing_field = self.clear_field()

        self.winner_banner = load_image('winner_banner', settings.WIDTH - settings.PADDING * 2)
        self.end_screen_dimming = pg.Surface((settings.WIDTH, settings.HEIGHT))
        self.end_screen_dimming.fill(settings.GREY)
        self.end_screen_dimming.set_alpha(240)

        self.again_button_rect = pg.Rect(settings.AGAIN_RECT_X, settings.AGAIN_RECT_Y, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)
        self.quit_button_rect = pg.Rect(settings.QUIT_RECT_X, settings.QUIT_RECT_Y, settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT)

        self.again_button_color = settings.BUTTON_COLORS['green']['color']
        self.quit_button_color = settings.BUTTON_COLORS['red']['color']

    def clear_field(self):
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def create_end_text(self):
        if not self.tie:
            player_number = self.get_player_number()
            winning_text = (f'Player {player_number} wins!')
            self.winner_text_surf = self.font.render(winning_text, True, (settings.GREEN if player_number == 1 else settings.RED))
        else:
            winning_text = (f'It a tie!')
            self.winner_text_surf = self.font.render(winning_text, True, settings.BLACK)
        
        again_text = ('Play again?')
        self.again_text_surf = self.font.render(again_text, True, settings.WHITE)
        quit_text = ('Quit game?')
        self.quit_text_surf = self.font.render(quit_text, True, settings.WHITE)

    def check_winning(self):
        for i in range(3):
            if sum(self.playing_field[i]) == 3 or sum(self.playing_field[i]) == -3:
                self.won =  True
            if sum(row[i] for row in self.playing_field) == 3 or sum(row[i] for row in self.playing_field) == -3:
                self.won =  True
    
        if self.playing_field[0][0] + self.playing_field[1][1] + self.playing_field[2][2] == 3 or self.playing_field[0][0] + self.playing_field[1][1] + self.playing_field[2][2] == -3:
            self.won =  True
        if self.playing_field[0][2] + self.playing_field[1][1] + self.playing_field[2][0] == 3 or self.playing_field[0][2] + self.playing_field[1][1] + self.playing_field[2][0] == -3:
            self.won =  True
        
        if self.won:
            self.create_end_text()
        
        if self.move_counter >= 9 and not self.won:
            self.tie = True
            self.create_end_text()

    def swab_player(self):
        if not self.won:
            self.player *= -1

    def mark_field(self):
        if self.clicked and not self.won and not self.tie:
            if 0 <= self.mouse_pos[0] < settings.FIELD_SIZE:
                x = 0
            elif settings.FIELD_SIZE <= self.mouse_pos[0] < settings.FIELD_SIZE * 2:
                x = 1
            elif  settings.FIELD_SIZE * 2 <= self.mouse_pos[0] < settings.WIDTH:
                x = 2
            if 0 <= self.mouse_pos[1] < settings.HEIGHT // 3:
                y = 0
            elif settings.FIELD_SIZE <= self.mouse_pos[1] < settings.FIELD_SIZE * 2:
                y = 1
            elif  settings.FIELD_SIZE * 2 <= self.mouse_pos[1] < settings.HEIGHT:
                y = 2
            if self.playing_field[y][x] == 0:
                self.move_counter += 1
                print(self.move_counter)
                self.playing_field[y][x] = self.player
                self.check_winning()
                self.swab_player()

    def get_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
                self.mouse_pos = pg.mouse.get_pos()

    def draw_circle(self, j, i):
        centerx = (settings.FIELD_SIZE * i) + settings.FIELD_SIZE // 2
        centery = (settings.FIELD_SIZE * j) + settings.FIELD_SIZE // 2
        pg.draw.circle(self.window, settings.RED, (centerx, centery), (settings.FIELD_SIZE // 2) - settings.PADDING, settings.LINE_THIKNESS * 2)

    def draw_cross(self, j, i):
        centerx = settings.FIELD_SIZE * i + settings.FIELD_SIZE // 2
        centery = settings.FIELD_SIZE * j + settings.FIELD_SIZE // 2
        pg.draw.line(self.window, settings.GREEN, (centerx - (settings.FIELD_SIZE // 2) + settings.PADDING * 2, centery - (settings.FIELD_SIZE // 2) + settings.PADDING * 2), (centerx + (settings.FIELD_SIZE // 2) - settings.PADDING * 2, centery + (settings.FIELD_SIZE // 2) - settings.PADDING * 2), settings.LINE_THIKNESS * 2)
        pg.draw.line(self.window, settings.GREEN, (centerx - (settings.FIELD_SIZE // 2) + settings.PADDING * 2, centery + (settings.FIELD_SIZE // 2) - settings.PADDING * 2), (centerx + (settings.FIELD_SIZE // 2) - settings.PADDING * 2, centery - (settings.FIELD_SIZE // 2) + settings.PADDING * 2), settings.LINE_THIKNESS * 2)

    def get_player_number(self):
        return 1 if self.player == 1 else 2

    def draw_buttons(self):
        pg.draw.rect(self.window, self.again_button_color, self.again_button_rect, border_radius=5)
        self.window.blit(self.again_text_surf, (settings.HALF_WIDTH - self.again_text_surf.get_width() // 2, self.again_button_rect[1] + settings.BUTTON_HEIGHT // 2 - self.again_text_surf.get_height() // 2 - settings.AGAIN_BUTTON_ELEVATION + 5))
        pg.draw.rect(self.window, self.quit_button_color, self.quit_button_rect, border_radius=5)
        self.window.blit(self.quit_text_surf, (settings.HALF_WIDTH - self.quit_text_surf.get_width() // 2, self.quit_button_rect[1] + settings.BUTTON_HEIGHT // 2 - self.quit_text_surf.get_height() // 2 - settings.QUIT_BUTTON_ELEVATION + 5))

    def draw_window(self):
        player_number = self.get_player_number()
        pg.display.set_caption(f'Tic Tac Toe                   Player {player_number} is on')
        self.window.fill(settings.BG_COLOR)
        for i in range(3):
            if i > 0:
                pg.draw.line(self.window, settings.BLACK, (settings.FIELD_SIZE * i, 0), (settings.FIELD_SIZE * i, settings.HEIGHT), settings.LINE_THIKNESS)
                pg.draw.line(self.window, settings.BLACK, (0, settings.FIELD_SIZE * i), (settings.HEIGHT, settings.FIELD_SIZE * i), settings.LINE_THIKNESS)
            for j in range(3):
                if self.playing_field[j][i] == 1:
                    self.draw_cross(j, i)
                elif self.playing_field[j][i] == -1:
                    self.draw_circle(j, i)
        if self.won or self.tie:
            self.window.blit(self.end_screen_dimming, (0, 0))
            self.window.blit(self.winner_banner, (settings.HALF_WIDTH - self.winner_banner.get_width() // 2, (settings.FIELD_SIZE - self.winner_banner.get_height() // 2)))
            self.window.blit(self.winner_text_surf, (settings.HALF_WIDTH - self.winner_text_surf.get_width() // 2, settings.FIELD_SIZE - self.winner_text_surf.get_height() // 2 - 18))
            self.draw_buttons()
        
        pg.display.update()

    def run(self):
        while self.running:
            self.printing = False
            self.clock.tick(30)
            self.get_input()
            self.mark_field()
            self.draw_window()
                       
            if self.clicked:
                self.clicked = False

        pg.quit()
                    

if __name__ == '__main__':
    Game().run()