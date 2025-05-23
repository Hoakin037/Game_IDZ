import pygame
import platform
import asyncio

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Поле ввода и кнопка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)

# Шрифты
font = pygame.font.SysFont("arial", 36)

# Поле ввода
input_box = pygame.Rect(200, 200, 400, 50)
input_text = ""
active = False

# Кнопка "Начать"
button = pygame.Rect(350, 300, 115, 50)
button_text = font.render("Начать", True, WHITE)

def draw():
    screen.fill(WHITE)
    
    # Отрисовка поля ввода
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = font.render(input_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    
    # Отрисовка кнопки
    pygame.draw.rect(screen, BLUE, button)
    screen.blit(button_text, (button.x + 10, button.y + 5))
    
    pygame.display.flip()

def setup():
    pass  # Инициализация уже выполнена выше

async def update_loop():
    global input_text, active
    running = True
    
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
                    print(f"Введено: {input_text}")
            elif event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    print(f"Введено: {input_text}")
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
        
        draw()
        await asyncio.sleep(1.0 / 60)  # 60 FPS

    pygame.quit()

async def main():
    setup()
    await update_loop()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())