import pygame
#from pygame import display, movie


FPS = 144
pygame.init()

#music = pygame.mixer.Sound("fall.wav")

clock = pygame.time.Clock()



screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
background = pygame.image.load('fallest2.jpg')

bg = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))

width = 1000

playing = True
while playing:

    for event in pygame.event.get():
        screen.blit(bg, (0, 0))
    pygame.display.update()


pygame.quit()
