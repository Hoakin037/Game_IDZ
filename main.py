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
        return (randint(0, n-1), randint(0, m-1))

    def move(self, direction, n, m):
        x, y = self.place
        if direction == "up" and y > 0:
            y -= 1
        elif direction == "down" and y < m-1:
            y += 1
        elif direction == "left" and x > 0:
            x -= 1
        elif direction == "right" and x < n-1:
            x += 1
        self.place = (x, y)

class GameLabel:
    def __init__(self):
        self.cell_size = 50
        self.grid_line_width = 4
        self.margin = 10
        self.n = 10
        self.m = 10
        self.width = self.n * self.cell_size + (self.n - 1) * self.grid_line_width + 2 * self.margin
        self.heights = self.m * self.cell_size + (self.m - 1) * self.grid_line_width + 2 * self.margin
        self.player = None

    def set_label(self, n, m):
        try:
            n, m = int(n), int(m)
            if 5 <= n <= 20 and 5 <= m <= 20:  # Ограничение размеров
                self.n, self.m = n, m
                self.width = self.n * self.cell_size + (self.n - 1) * self.grid_line_width + 2 * self.margin
                self.heights = self.m * self.cell_size + (self.m - 1) * self.grid_line_width + 2 * self.margin
                self.player = Player(10, self.n, self.m)  # Создаем игрока
            else:
                print("Размеры сетки должны быть от 5 до 20")
        except ValueError:
            print("Введите два числа, разделенных пробелом")

    def set_button_and_input_box(self, screen_width, screen_height):
        input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50)
        button = pygame.Rect(screen_width // 2 - 57, screen_height // 2 + 40, 115, 50)
        return input_box, button

    def draw_input_label(self, screen, input_box, button, input_text, active):
        screen.fill((33, 20, 74))
        font = pygame.font.SysFont("arial", 36)

        # Инструкция
        instruction = font.render("Введите n m (например, 10 10)", True, (255, 255, 255))
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, screen.get_height() // 2 - 80))

        # Поле ввода
        pygame.draw.rect(screen, (255, 255, 255) if active else (0, 0, 0), input_box, 2)
        text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Кнопка
        pygame.draw.rect(screen, (116, 96, 179), button)
        button_text = font.render("Начать", True, (255, 255, 255))
        screen.blit(button_text, (button.x + 10, button.y + 5))

    def init_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.heights))
        pygame.display.set_caption("_ИДЗ_3_")
        try:
            icon = pygame.image.load("utka20.png")
            pygame.display.set_icon(icon)
        except pygame.error:
            print("Warning: Could not load icon image")
        return screen

    def draw_player(self, place, screen, color):
        x, y = place
        cell_x = self.margin + x * (self.cell_size + self.grid_line_width) + 3
        cell_y = self.margin + y * (self.cell_size + self.grid_line_width) + 3
        pygame.draw.rect(screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

    def draw_lines(self, screen):
        for i in range(1, self.n):
            x = self.margin + i * (self.cell_size + self.grid_line_width)
            pygame.draw.line(screen, (89, 65, 135), (x, self.margin), (x, self.heights - self.margin), self.grid_line_width)
        for i in range(1, self.m):
            y = self.margin + i * (self.cell_size + self.grid_line_width)
            pygame.draw.line(screen, (89, 65, 135), (self.margin, y), (self.width - self.margin, y), self.grid_line_width)

    async def launch_game(self):
        running = True
        screen = self.init_screen()
        input_text = ""
        active = False
        show_input = True
        input_box, button = self.set_button_and_input_box(self.width, self.heights)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if show_input and input_box.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                    if show_input and button.collidepoint(event.pos) and input_text:
                        try:
                            n, m = input_text.split()
                            self.set_label(n, m)
                            screen = pygame.display.set_mode((self.width, self.heights))
                            input_box, button = self.set_button_and_input_box(self.width, self.heights)
                            show_input = False
                            input_text = ""
                        except ValueError:
                            print("Введите два числа, разделенных пробелом")
                elif event.type == pygame.KEYDOWN:
                    if show_input and active:
                        if event.key == pygame.K_RETURN and input_text:
                            try:
                                n, m = input_text.split()
                                self.set_label(n, m)
                                screen = pygame.display.set_mode((self.width, self.heights))
                                input_box, button = self.set_button_and_input_box(self.width, self.heights)
                                show_input = False
                                input_text = ""
                            except ValueError:
                                print("Введите два числа, разделенных пробелом")
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode
                    elif not show_input:
                        if event.key == pygame.K_r:  # Возврат к вводу
                            show_input = True
                            input_text = ""
                            active = False
                        elif self.player:
                            if event.key == pygame.K_UP:
                                self.player.move("up", self.n, self.m)
                            elif event.key == pygame.K_DOWN:
                                self.player.move("down", self.n, self.m)
                            elif event.key == pygame.K_LEFT:
                                self.player.move("left", self.n, self.m)
                            elif event.key == pygame.K_RIGHT:
                                self.player.move("right", self.n, self.m)

            screen.fill((22, 8, 48))
            if show_input:
                self.draw_input_label(screen, input_box, button, input_text, active)
            else:
                self.draw_lines(screen)
                if self.player:
                    self.draw_player(self.player.place, screen, (94, 218, 230))

            pygame.display.flip()
            await asyncio.sleep(1.0 / 60)

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