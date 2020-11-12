import pygame
pygame.init()
pygame.display.set_mode((5,5))
while 1:
	first = raw_input()
	second = raw_input()
	size = input()
	pygame.image.save(pygame.transform.scale(pygame.image.load(first).convert_alpha(),size),second)

