import pygame
from random import randint
import platform
import asyncio

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
    def __init__(self):
        self.cell_size = 50
        self.grid_line_width = 4 # Толщина линний
        self.margin = 10  # Отступ
        
        
    def set_label(self, n, m):
        self.n = n
        self.m = m  
        self.width = self.n * self.cell_size + (self.n - 1) * self.grid_line_width + 2 * self.margin
        self.heights = self.m * self.cell_size + (self.m - 1) * self.grid_line_width + 2 * self.margin


    def set_button_and_input_box(self):
         # Поле ввода
        input_box = pygame.Rect(200, 200, 400, 50)
        # Кнопка "Начать"
        button = pygame.Rect(350, 300, 115, 50)
        
        return input_box, button
    
    def draw_input_label(self, screen, input_box, button):
        screen.fill((33, 20, 74))
        
        # Шрифты
        font = pygame.font.SysFont("arial", 36)

        input_text = ""
        button_text = font.render("Начать", True, (255,255,255))

        # Отрисовка поля ввода
        pygame.draw.rect(screen, (0,0,0), input_box, 2)
        text_surface = font.render(input_text, True, (0,0,0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        
        # Отрисовка кнопки
        pygame.draw.rect(screen, (116, 96, 179), button)
        screen.blit(button_text, (button.x + 10, button.y + 5))

        pygame.display.flip()



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

    async def launch_game(self):
        running = True
        screen = self.init_screen()
        input_text = ""
        button, input_box = self.set_button_and_input_box()

        self.draw_input_label(input_box, button)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверка клика по полю ввода
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    # Проверка клика по кнопке
                    if button.collidepoint(event.pos):
                        n, m = input_text.split()
                        self.set_label(n, m)
                elif event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_RETURN:
                        n, m = input_text.split()
                        self.set_label(n, m)
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode


            self.draw_input_label()

            await asyncio.sleep(1.0 / 60)  # 60 FPS
            screen.fill((22, 8, 48))

            self.draw_lines(screen)
            self.draw_player((4,6), screen, (94, 218, 230))
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

def setup():
        pass

async def main():
    setup()
    game = GameLabel()
    await game.launch_game()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())

