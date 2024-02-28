import pygame as pg


class Game:
    def __init__(self):
        pg.init()

        self.WIDTH = self.HEIGHT = 500
        self.LINE_THIKNESS = (self.WIDTH + self.HEIGHT) // 200
        self.field_size = (self.WIDTH + self.HEIGHT) // 6
        self.padding = (self.WIDTH + self.HEIGHT) // 100

        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.font = pg.font.SysFont('comicsans', 32)

        self.clock = pg.time.Clock()
        self.running = True
        self.won = False
        self.player = 1
        self.clicked = False
        self.mouse_pos = (-1, -1)
        
        self.BG_COLOR = (255, 255, 200)
        self.playing_field = self.clear_field()

    def clear_field(self):
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def check_winning(self):
        for i in range(3):
            if sum(self.playing_field[i]) == 3 or sum(self.playing_field[i]) == -3:
                return True
            if sum(row[i] for row in self.playing_field) == 3 or sum(row[i] for row in self.playing_field) == -3:
                return True
    
        if self.playing_field[0][0] + self.playing_field[1][1] + self.playing_field[2][2] == 3 or self.playing_field[0][0] + self.playing_field[1][1] + self.playing_field[2][2] == -3:
            return True
        if self.playing_field[0][2] + self.playing_field[1][1] + self.playing_field[2][0] == 3 or self.playing_field[0][2] + self.playing_field[1][1] + self.playing_field[2][0] == -3:
            return True
        
        return False

    def swab_player(self):
        self.player *= -1
        return True

    def mark_field(self):
        if self.clicked:
            if 0 <= self.mouse_pos[0] < self.WIDTH // 3:
                x = 0
            elif self.WIDTH // 3 <= self.mouse_pos[0] < self.WIDTH // 3 * 2:
                x = 1
            elif  self.WIDTH // 3 * 2 <= self.mouse_pos[0] < self.WIDTH:
                x = 2
            if 0 <= self.mouse_pos[1] < self.HEIGHT // 3:
                y = 0
            elif self.HEIGHT // 3 <= self.mouse_pos[1] < self.HEIGHT // 3 * 2:
                y = 1
            elif  self.HEIGHT // 3 * 2 <= self.mouse_pos[1] < self.HEIGHT:
                y = 2
            self.playing_field[y][x] = self.player
            if not self.won:
                self.printing = self.swab_player()

    def get_input(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
                self.mouse_pos = pg.mouse.get_pos()

    def draw_circle(self, j, i):
        centerx = (self.WIDTH // 3 * i) + self.field_size // 2
        centery = (self.HEIGHT // 3 * j) + self.field_size // 2
        pg.draw.circle(self.window, 'red', (centerx, centery), (self.field_size // 2) - self.padding, self.LINE_THIKNESS * 2)

    def draw_cross(self, j, i):
        centerx = self.WIDTH // 3 * i + self.field_size // 2
        centery = self.HEIGHT // 3 * j + self.field_size // 2
        pg.draw.line(self.window, 'darkgreen', (centerx - (self.field_size // 2) + self.padding * 2, centery - (self.field_size // 2) + self.padding * 2), (centerx + (self.field_size // 2) - self.padding * 2, centery + (self.field_size // 2) - self.padding * 2), self.LINE_THIKNESS * 2)
        pg.draw.line(self.window, 'darkgreen', (centerx - (self.field_size // 2) + self.padding * 2, centery + (self.field_size // 2) - self.padding * 2), (centerx + (self.field_size // 2) - self.padding * 2, centery - (self.field_size // 2) + self.padding * 2), self.LINE_THIKNESS * 2)

    def get_player_number(self):
        return 1 if self.player == 1 else 2

    def draw_window(self):
        player_number = self.get_player_number()
        pg.display.set_caption(f'Tic Tac Toe                   Player {player_number} is on')
        self.window.fill(self.BG_COLOR)
        for i in range(3):
            if i > 0:
                pg.draw.line(self.window, 'black', (self.WIDTH // 3 * i, 0), (self.WIDTH // 3 * i, self.HEIGHT), self.LINE_THIKNESS)
                pg.draw.line(self.window, 'black', (0, self.HEIGHT // 3 * i), (self.HEIGHT, self.HEIGHT // 3 * i), self.LINE_THIKNESS)
            for j in range(3):
                if self.playing_field[j][i] == 1:
                    self.draw_cross(j, i)
                elif self.playing_field[j][i] == -1:
                    self.draw_circle(j, i)
        
        pg.display.update()

    def run(self):
        while self.running:
            self.printing = False
            self.clock.tick(30)
            self.get_input()
            self.mark_field()
            self.won = self.check_winning()
            self.draw_window()            
            if self.clicked:
                self.clicked = False
            if self.won:
                print('won')
                self.running = False

        pg.quit()
                    

if __name__ == '__main__':
    Game().run()