import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("_ИДЗ_3_")
icon = pygame.image.load("ИДЗ_3/utka20.png")
pygame.display.set_icon(icon)

square = pygame.Surface((100, 100))
square.fill("White")

running = True

while running:
    screen.fill((207, 182, 252))
    screen.blit(square, (250, 250))
    pygame.draw.line(screen, (0, 0, 0), [100, 100], [100, 10])
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

class DrawGameLabel:
    def __init__(self, playerA_coordinates, playerB_coordinates, n, m):
        self.screen = self.set_screen(n, m)
        self.playerA_coordinates = playerA_coordinates
        self.playerB_coordinates = playerB_coordinates

    def set_screen(self, n: int, m: int):
        width = n*50 + (n-1)*4 + 10 
        heights = m*50 + (m-1)*4 + 10
        return pygame.display.set_mode((width, heights))
   
    
    def draw_lines(self, width: int, heights: int):

        for i in range(50, heights - 5, 50):
            if i < width - 50:
                pygame.draw.line(self.screen, (0,0,0), (i, 5), (i, heights - 5), width=3)
            
            pygame.draw.line(self.screen, (0,0,0), (5, i), (width - 5, i), 3)
            
            i+= 3
