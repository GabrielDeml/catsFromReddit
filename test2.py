import pygame
picture = pygame.image.load("/home/gabe/PycharmProjects/cats/chgy3xeve9n41.jpg")
screen = pygame.display.set_mode((1600, 900))
picture = pygame.transform.scale(picture, (1280, 720))
rect = picture.get_rect()
rect = rect.move((50, 50))
screen.blit(picture, rect)
pygame.display.flip()