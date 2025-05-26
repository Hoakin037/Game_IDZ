import pygame
from random import randint
import platform
import asyncio

class Player:
    def __init__(self, punch_power, n, m, name, health_pickups):
        self.place = self.choose_player_place(n, m, health_pickups)
        self.punch_power = punch_power
        self.hp = 100
        self.name = name
        self.health_pickups = health_pickups

    def choose_player_place(self, n, m, health_pickups):
        while True:
            pos = (randint(0, n-1), randint(0, m-1))
            if pos not in health_pickups:
                return pos

    def move(self, direction, n, m, other_place):
        x, y = self.place
        new_x, new_y = x, y
        if direction == "up" and y > 0:
            new_y -= 1
        elif direction == "down" and y < m-1:
            new_y += 1
        elif direction == "left" and x > 0:
            new_x -= 1
        elif direction == "right" and x < n-1:
            new_x += 1
        
        if (new_x, new_y) != other_place:
            self.place = (new_x, new_y)
            if self.place in self.health_pickups:
                self.hp += 20
                print(f"{self.name} picked up a health kit! HP now {self.hp}")
                self.health_pickups.remove(self.place)

    def move_in_label(self, key, game_label, other_place):
        if key == pygame.K_UP:
            self.move("up", game_label.n, game_label.m, other_place)
        elif key == pygame.K_DOWN:
            self.move("down", game_label.n, game_label.m, other_place)
        elif key == pygame.K_LEFT:
            self.move("left", game_label.n, game_label.m, other_place)
        elif key == pygame.K_RIGHT:
            self.move("right", game_label.n, game_label.m, other_place)

    def hit_player(self, other, place1, place2):
        x1, y1 = place1[0], place1[1]
        x2, y2 = place2[0], place2[1]

        if self.name == "Player 1":
            attack_positions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1)
            ]
        else:
            attack_positions = [
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ]

        can_attack = False
        for i, j in attack_positions:
            if x1 + i == x2 and y1 + j == y2:
                can_attack = True
                other.hp -= self.punch_power
                #print(f"{self.name} нанес удар {other.name}! HP {other.name} теперь {other.hp}")
                break
        #if not can_attack:
            #print(f"{self.name} не может атаковать {other.name}: не в зоне атаки. Позиция {self.name}: {self.place}, Позиция {other.name}: {other.place}")

class GameLabel:
    def __init__(self):
        self.cell_size = 50
        self.grid_line_width = 4
        self.margin = 10
        self.n = 10
        self.m = 10
        self.width = self.n * self.cell_size + (self.n - 1) * self.grid_line_width + 2 * self.margin
        self.heights = self.m * self.cell_size + (self.m - 1) * self.grid_line_width + 2 * self.margin
        self.player1 = None
        self.player2 = None
        self.current_player = 1
        self.font = None
        self.health_pickups = [] # Аптечка

    # Инициализация экрана
    def init_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.heights))
        pygame.display.set_caption("_ИДЗ_3_")
        self.font = pygame.font.SysFont("arial", 24)
        try:
            icon = pygame.image.load("utka20.png")
            pygame.display.set_icon(icon)
        except pygame.error:
            print("Изображение не найдено!")
        return screen

    # Установка игрового поля
    def set_label(self, n, m):
        try:
            n, m = int(n), int(m)
            if n < 4 or m < 4:
                print("Ошибка: Размеры сетки должны быть не менее 4 по каждому измерению")
                return False
            if 4 <= n <= 20 and 4 <= m <= 20:
                self.n, self.m = n, m
                self.width = self.n * self.cell_size + (self.n - 1) * self.grid_line_width + 2 * self.margin
                self.heights = self.m * self.cell_size + (self.m - 1) * self.grid_line_width + 2 * self.margin
                
                # Инициализация аптечек
                self.health_pickups = []
                while len(self.health_pickups) < 3:
                    pos = (randint(0, n-1), randint(0, m-1))
                    if pos not in self.health_pickups:
                        self.health_pickups.append(pos)
                
                # Создание игроков
                self.player1 = Player(10, self.n, self.m, "Player 1", self.health_pickups)
                self.player2 = Player(20, self.n, self.m, "Player 2", self.health_pickups)
                while self.player1.place == self.player2.place or self.player2.place in self.health_pickups:
                    self.player2 = Player(20, self.n, self.m, "Player 2", self.health_pickups)
                return True
            else:
                print("Размеры сетки должны быть от 4 до 20")
                return False
        except ValueError:
            print("Введите два числа, разделенных пробелом")
            return False

    # Установка кнопки и поля для ввода
    def set_button_and_input_box(self, screen_width, screen_height):
        input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50)
        button = pygame.Rect(screen_width // 2 - 57, screen_height // 2 + 40, 115, 50)
        return input_box, button

    # Отрисовка экрана ввода
    def draw_input_label(self, screen, input_box, button, input_text, active):
        screen.fill((182, 3, 252))
        font = pygame.font.SysFont("arial", 36)
        instruction = font.render("Введите n m (например, 10 10)", True, (255, 255, 255))
        
        screen.blit(instruction, (screen.get_width() // 2 - instruction.get_width() // 2, screen.get_height() // 2 - 80))
        pygame.draw.rect(screen, (255, 255, 255) if active else (0, 0, 0), input_box, 2)
        text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, (116, 96, 179), button)
        button_text = font.render("Начать", True, (255, 255, 255))
        screen.blit(button_text, (button.x + 10, button.y + 5))

    # Отрисовка игроков
    def draw_player(self, place, screen, color):
        x, y = place
        cell_x = self.margin + x * (self.cell_size + self.grid_line_width) + 3
        cell_y = self.margin + y * (self.cell_size + self.grid_line_width) + 3
        pygame.draw.rect(screen, color, (cell_x, cell_y, self.cell_size, self.cell_size))

    # Отрисовка аптечки
    def draw_health_pickup(self, place, screen):
        x, y = place
        cell_x = self.margin + x * (self.cell_size + self.grid_line_width) + 3
        cell_y = self.margin + y * (self.cell_size + self.grid_line_width) + 3
        pygame.draw.rect(screen, (0, 255, 0), (cell_x, cell_y, self.cell_size, self.cell_size))

    # Отрисовка игровой сетки
    def draw_lines(self, screen):
        for i in range(1, self.n):
            x = self.margin + i * (self.cell_size + self.grid_line_width)
            pygame.draw.line(screen, (89, 65, 135), (x, self.margin), (x, self.heights - self.margin), self.grid_line_width)
        for i in range(1, self.m):
            y = self.margin + i * (self.cell_size + self.grid_line_width)
            pygame.draw.line(screen, (89, 65, 135), (self.margin, y), (self.width - self.margin, y), self.grid_line_width)

    # Отображение текущих характеристик
    def draw_hud(self, screen):
        player1_hp = self.font.render(f"Player 1 HP: {self.player1.hp}", True, (94, 218, 230))
        player2_hp = self.font.render(f"Player 2 HP: {self.player2.hp}", True, (255, 99, 71))
        turn = self.font.render(f"Turn: Player {self.current_player}", True, (255, 255, 255))
        
        screen.blit(player1_hp, (10, 10))
        screen.blit(player2_hp, (self.width - player2_hp.get_width() - 10, 10))
        screen.blit(turn, (self.width // 2 - turn.get_width() // 2, 10))

    # Обработка кликов мыши
    def handle_mouse_input(self, event, show_input, input_box, button, input_text, screen):
        if show_input and input_box.collidepoint(event.pos):
            return True, input_text, show_input, screen, input_box, button
        else:
            active = False
            if show_input and button.collidepoint(event.pos) and input_text:
                try:
                    n, m = input_text.split()
                    if self.set_label(n, m):
                        screen = pygame.display.set_mode((self.width, self.heights))
                        input_box, button = self.set_button_and_input_box(self.width, self.heights)
                        show_input = False
                        input_text = ""
                except ValueError:
                    print("Введите два числа, разделенных пробелом")
            return active, input_text, show_input, screen, input_box, button

    #Обработка начала игры через клавиатуру
    def handle_key_input(self, event, show_input, active, input_text, screen, input_box, button):
        if show_input and active:
            if event.key == pygame.K_RETURN and input_text:
                try:
                    n, m = input_text.split()
                    if self.set_label(n, m):
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
        return input_text, show_input, screen, input_box, button

    # Проверка статуса игры
    def check_game_over(self):
        if self.player1.hp <= 0:
            print("Игрок 2 победил! Игра окончена.")
            return True
        elif self.player2.hp <= 0:
            print("Игрок 1 победил! Игра окончена.")
            return True
        return False

    # Игровой цикл
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
                    active, input_text, show_input, screen, input_box, button = self.handle_mouse_input(event, show_input, input_box, button, input_text, screen)
                elif event.type == pygame.KEYDOWN:
                    input_text, show_input, screen, input_box, button = self.handle_key_input(event, show_input, active, input_text, screen, input_box, button)
                    if not show_input:
                        if event.key == pygame.K_r:
                            show_input = True
                            input_text = ""
                            active = False
                        elif self.current_player == 1 and self.player1:
                            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                                print(f"Ход Player 1. Позиция до хода: {self.player1.place}")
                                old_place = self.player1.place
                                self.player1.move_in_label(event.key, self, self.player2.place)
                                print(f"Позиция Player 1 после хода: {self.player1.place}")
                                if old_place != self.player1.place:
                                    self.player1.hit_player(self.player2, self.player1.place, self.player2.place)
                                    if self.check_game_over():
                                        running = False
                                    else:
                                        self.current_player = 2
                        elif self.current_player == 2 and self.player2:
                            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                                print(f"Ход Player 2. Позиция до хода: {self.player2.place}")
                                old_place = self.player2.place
                                self.player2.move_in_label(event.key, self, self.player1.place)
                                print(f"Позиция Player 2 после хода: {self.player2.place}")
                                if old_place != self.player2.place:
                                    self.player2.hit_player(self.player1, self.player2.place, self.player1.place)
                                    if self.check_game_over():
                                        running = False
                                    else:
                                        self.current_player = 1

            screen.fill((182, 3, 252))
            if show_input:
                self.draw_input_label(screen, input_box, button, input_text, active)
            else:
                self.draw_lines(screen)
                for pickup in self.health_pickups:
                    self.draw_health_pickup(pickup, screen)
                if self.player1:
                    self.draw_player(self.player1.place, screen, (94, 218, 230))
                if self.player2:
                    self.draw_player(self.player2.place, screen, (255, 99, 71))
                self.draw_hud(screen)

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