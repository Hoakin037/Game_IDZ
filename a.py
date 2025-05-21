import pygame

n = 6
m = 6
width = n*50 + (n-1)*4 + 10
heights = m*50 + (m-1)*4 + 10

pygame.init()
screen = pygame.display.set_mode((width, heights))
pygame.display.set_caption("_ИДЗ_3_")
icon = pygame.image.load("ИДЗ_3/utka20.png")
pygame.display.set_icon(icon)


running = True

while running:
    screen.fill((207, 182, 252))
    for i in range(55, width-10, 53):
            i += 3
            if i < width:
                #Вертикальные
                pygame.draw.line(screen, (0,0,0), (i, 5), (i, width-5), width=3)
            #Горизонтальные
            pygame.draw.line(screen, (0,0,0), (5, i), (width-5, i), 3)
            
            
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()