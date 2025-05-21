import pygame

n = 9
m = 10
cell_size = 50
grid_line_width = 4 # Толщина линний
margin = 10  # Отступ

width = n * cell_size + (n - 1) * grid_line_width + 2 * margin
heights = m * cell_size + (m - 1) * grid_line_width + 2 * margin

pygame.init()
screen = pygame.display.set_mode((width, heights))
pygame.display.set_caption("_ИДЗ_3_")
icon = pygame.image.load("utka20.png")
pygame.display.set_icon(icon)

running = True

while running:
    screen.fill((22, 8, 48))

    # Вертикальные
    for i in range(1, n): 
        x = margin + i * cell_size + (i - 1) * grid_line_width 
        pygame.draw.line(screen, (89, 65, 135), (x, margin), (x, heights - margin), grid_line_width)

    # Горизонтальные
    for i in range(1, m): 
        y = margin + i * cell_size + (i - 1) * grid_line_width 
        pygame.draw.line(screen, (89, 65, 135), (margin, y), (width - margin, y), grid_line_width)  

            
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()