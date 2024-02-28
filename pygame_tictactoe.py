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
        self.again_question = True
        
        self.BG_COLOR = (255, 255, 200)
        self.playing_field = self.clear_field()

    def clear_field(self):
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def create_end_text(self):
        player_number = self.get_player_number()
        winning_text = (f'Player {player_number} wins!')
        self.winning_text_surf = self.font.render(winning_text, True, ('darkgreen' if player_number == 1 else 'darkred'))
        again_text = ('Play again?')
        self.again_text_surf = self.font.render(again_text, True, 'darkgreen')
        quit_text = ('Quit game?')
        self.quit_text_surf = self.font.render(quit_text, True, 'darkred')

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
        


    def swab_player(self):
        if not self.won:
            self.player *= -1

    def mark_field(self):
        if self.clicked and not self.won:
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
            if self.playing_field[y][x] == 0:
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
        centerx = (self.WIDTH // 3 * i) + self.field_size // 2
        centery = (self.HEIGHT // 3 * j) + self.field_size // 2
        pg.draw.circle(self.window, 'darkred', (centerx, centery), (self.field_size // 2) - self.padding, self.LINE_THIKNESS * 2)

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
        if self.won:
            self.window.blit(self.winning_text_surf, (self.WIDTH // 2 - self.winning_text_surf.get_width() // 2, self.HEIGHT // 3 - self.winning_text_surf.get_height() // 2))
            self.window.blit(self.again_text_surf, (self.WIDTH // 2 - self.again_text_surf.get_width() // 2, self.HEIGHT // 2 - self.again_text_surf.get_height() // 2))
            self.window.blit(self.quit_text_surf, (self.WIDTH // 2 - self.quit_text_surf.get_width() // 2, self.HEIGHT // 3 * 2 - self.quit_text_surf.get_height() // 2))
        
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