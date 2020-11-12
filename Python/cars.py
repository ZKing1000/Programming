import pygame,random
on = 1
rez = (1024,576)
destinations = [(random.randint(0,rez[0]),random.randint(0,rez[1])) for x in range(random.randint(10,20))]
print(destinations)
av = [0,0]
for x in destinations:
    av[0] += x[0]
    av[1] += x[1]
av = [av[0]/float(len(destinations)),av[1]/float(len(destinations))]
screen = pygame.display.set_mode(rez)
mid = (rez[0]/2.0,rez[1])
clock = pygame.time.Clock()
streetWidth = 9
streetColor = (0,0,0)
cars = []
carDimentions = (4,6)
while on:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = 0

    screen.fill((30,200,30))
    pygame.draw.line(screen,streetColor,mid,av,streetWidth)
    pygame.draw.line(screen,(255,255,255),mid,av,1)
    for x in destinations:
        pygame.draw.line(screen,streetColor,av,x,streetWidth)
        pygame.draw.line(screen,(255,255,255),av,x,1)
        pygame.draw.circle(screen,(255,100,100),x,5)
    pygame.display.update()

