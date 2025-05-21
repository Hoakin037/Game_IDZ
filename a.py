import pygame
from random import randint

class Player:
    def __init__(self, punch_power, n, m):
        self.place = self.choose_player_place(n, m)
        self.punch_power = punch_power
        self.hp = 100

    def choose_player_place(self, n, m):
        x = randint(0, n)
        y = randint(0, m)
        return (x, y)
    

    
class GameLabel:
    def __init__(self, n, m):
        self.cell_size = 50
        self.grid_line_width = 4 # Толщина линний
        self.margin = 10  # Отступ
        self.width = n * self.cell_size + (n - 1) * self.grid_line_width + 2 * self.margin
        self.heights = m * self.cell_size + (m - 1) * self.grid_line_width + 2 * self.margin
        self.n = n
        self.m = m

    def init_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.heights))
        pygame.display.set_caption("_ИДЗ_3_")
        icon = pygame.image.load("utka20.png")
        pygame.display.set_icon(icon)

        return screen

    def draw_player(self, place, screen, color):
        x, y = place
        cell_x = self.margin + x * (self.cell_size + self.grid_line_width) - 1
        cell_y = self.margin + y * (self.cell_size + self.grid_line_width) - 1
        pygame.draw.rect(screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))
        

    def draw_lines(self, screen):
        # Вертикальные
        for i in range(1, self.n): 
            x = self.margin + i * self.cell_size + (i - 1) * self.grid_line_width 
            pygame.draw.line(screen, (89, 65, 135), (x, self.margin), (x, self.heights - self.margin), self.grid_line_width)

        # Горизонтальные
        for i in range(1, self.m): 
            y = self.margin + i * self.cell_size + (i - 1) * self.grid_line_width 
            pygame.draw.line(screen, (89, 65, 135), (self.margin, y), (self.width - self.margin, y), self.grid_line_width)

    def launch_game(self):
        running = True
        screen = self.init_screen()

        while running:
            screen.fill((22, 8, 48))

            self.draw_lines(screen)
            self.draw_player((4,6), screen, (94, 218, 230))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

game = GameLabel(9, 10)
game.launch_game()