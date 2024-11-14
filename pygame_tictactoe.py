import pygame as pg
import settings
from utils import load_image, Button

from typing import TypeVar

Button_object = TypeVar("Button_object")

class Game:
    def __init__(self) -> None:
        """ Initializes the game class. """
        pg.init()

        self.window: pg.display = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.font: pg.font.Font = pg.font.SysFont("comicsans", 32)

        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True
        self.won: bool = False
        self.player = 1
        self.clicked: bool = False
        self.mouse_pos = (-1, -1)
        self.again_question: bool = True
        self.move_counter = 0
        self.tie: bool = False
        self.play_again: bool = None
        self.quit: bool = None
        
        self.playing_field: list[list[int]] = self.clear_field()

        self.winner_banner: pg.Surface = load_image("winner_banner", settings.WIDTH - settings.PADDING * 2)
        self.end_screen_dimming: pg.Surface = pg.Surface((settings.WIDTH, settings.HEIGHT))
        self.end_screen_dimming.fill(settings.GREY)
        self.end_screen_dimming.set_alpha(240)

        self.again_button: Button_object = Button(self.window, "Play again!", (settings.HALF_WIDTH, settings.HALF_HEIGHT), (settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 'green')
        self.quit_button: Button_object = Button(self.window, "Quit game!", (settings.HALF_WIDTH, settings.HALF_HEIGHT + settings.FIELD_SIZE // 2), (settings.BUTTON_WIDTH, settings.BUTTON_HEIGHT), 'red')

    def clear_field(self) -> list[list[int]]:
        """
        Returns the playing field filled with zeros.
        Returns:
        list[list[int]]: The playing field.
        """
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def check_again(self) -> None:
        """ Checks if self.play_again is true and starts a new game if so. """
        if self.play_again:
            pg.time.wait(500)
            self.running = True
            self.won = False
            self.player = 1
            self.clicked = False
            self.mouse_pos = (-1, -1)
            self.again_question = True
            self.move_counter = 0
            self.tie = False
            self.play_again = None
            self.quit = None
        
            self.playing_field = self.clear_field()
            
    def create_winner_banner(self) -> None:
        """ Creates a banner with the winner's number. """
        if not self.tie:
            player_number = self.get_player_number()
            winning_text = (f"Player {player_number} wins!")
            self.winner_text_surf = self.font.render(winning_text, True, (settings.GREEN if player_number == 1 else settings.RED))
        else:
            winning_text = (f"It's a tie!")
            self.winner_text_surf = self.font.render(winning_text, True, settings.BLACK)

    def check_winning(self) -> None:
        """ Checks if someone has won or if it is a tie. """
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
            self.create_winner_banner()
        
        if self.move_counter >= 9 and not self.won:
            self.tie = True
            self.create_winner_banner()

    def swap_player(self) -> None:
        """ Swaps the current player. (1 or -1) """
        if not self.won:
            self.player *= -1

    def mark_field(self) -> None:
        """ Marks the field where the player clicked. """
        if 0 <=  self.mouse_pos[0] <= settings.WIDTH and 0 <=  self.mouse_pos[1] <= settings.HEIGHT:
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
                    self.swap_player()

    def get_input(self) -> None:
        """ Gets the input from the player. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                self.clicked = True
                self.mouse_pos = pg.mouse.get_pos()
        
        self.play_again = self.again_button.check_collision()
        self.quit = self.quit_button.check_collision()

    def draw_circle(self, j, i) -> None:
        """ Draws a circle for player two's O. """
        centerx = (settings.FIELD_SIZE * i) + settings.FIELD_SIZE // 2
        centery = (settings.FIELD_SIZE * j) + settings.FIELD_SIZE // 2
        pg.draw.circle(self.window, settings.RED, (centerx, centery), (settings.FIELD_SIZE // 2) - settings.PADDING, settings.LINE_THICKNESS * 2)

    def draw_cross(self, j, i) -> None:
        """ Draws a cross for player one's X. """
        centerx = settings.FIELD_SIZE * i + settings.FIELD_SIZE // 2
        centery = settings.FIELD_SIZE * j + settings.FIELD_SIZE // 2
        pg.draw.line(self.window, settings.GREEN, (centerx - (settings.FIELD_SIZE // 2) + settings.PADDING * 2, centery - (settings.FIELD_SIZE // 2) + settings.PADDING * 2), (centerx + (settings.FIELD_SIZE // 2) - settings.PADDING * 2, centery + (settings.FIELD_SIZE // 2) - settings.PADDING * 2), settings.LINE_THICKNESS * 2)
        pg.draw.line(self.window, settings.GREEN, (centerx - (settings.FIELD_SIZE // 2) + settings.PADDING * 2, centery + (settings.FIELD_SIZE // 2) - settings.PADDING * 2), (centerx + (settings.FIELD_SIZE // 2) - settings.PADDING * 2, centery - (settings.FIELD_SIZE // 2) + settings.PADDING * 2), settings.LINE_THICKNESS * 2)

    def get_player_number(self) -> int:
        """ Returns the current player number. """
        return 1 if self.player == 1 else 2

    def draw_buttons(self) -> None:
        """ Draws the buttons. """
        self.again_button.render()
        self.quit_button.render()

    def draw_window(self) -> None:
        """ Draws the game window. """
        player_number = self.get_player_number()
        pg.display.set_caption(f"Tic Tac Toe                   Player {player_number} is on")
        self.window.fill(settings.BG_COLOR)
        for i in range(3):
            if i > 0:
                pg.draw.line(self.window, settings.BLACK, (settings.FIELD_SIZE * i, 0), (settings.FIELD_SIZE * i, settings.HEIGHT), settings.LINE_THICKNESS)
                pg.draw.line(self.window, settings.BLACK, (0, settings.FIELD_SIZE * i), (settings.HEIGHT, settings.FIELD_SIZE * i), settings.LINE_THICKNESS)
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

    def run(self) -> None:
        """ Runs the game. """
        while self.running:
            self.clock.tick(30)
            self.get_input()
            self.mark_field()
            self.draw_window()

            if self.won or self.tie:
                self.check_again()
            
            if self.clicked:
                self.clicked = False
            
            if self.quit:
                self.running = False
                       
        pg.quit()
                    

if __name__ == '__main__':
    Game().run()