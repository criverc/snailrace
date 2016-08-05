import sys, pygame
import time
pygame.init()

N=4  # number of snails

size = width, height = 640, 480

background = pygame.image.load ("background.gif")
screen = pygame.display.set_mode(size)

snail = [ pygame.image.load("snail-normal.gif") for i in range(N) ]
snailrect = [ snail[i].get_rect() for i in range(N) ]
speed = [ [i+1, 0] for i in range(N) ]

for i in xrange(N):
    snailrect[i] = snailrect[i].move([0, i*(height/N)])

while 1:
    screen.blit(background, background.get_rect())

    for i in xrange (N):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        snailrect[i] = snailrect[i].move(speed[i])
        if snailrect[i].right > width-50 and speed[i][0]>0:
            snail[i] = pygame.image.load("snail-surprised.gif")

        if snailrect[i].left < 0 or snailrect[i].right > width:
            snail[i] = pygame.image.load("snail-normal.gif")
            speed[i][0] = -speed[i][0]
            if speed[i][0] < 0:
                snail[i] = pygame.transform.flip (snail[i], True, False)

        if snailrect[i].left < 50 and speed[i][0]<0:
            snail[i] = pygame.image.load("snail-surprised.gif")
            snail[i] = pygame.transform.flip (snail[i], True, False)

        if snailrect[i].top < 0 or snailrect[i].bottom > height:
            speed[i][1] = -speed[i][1]

        screen.blit(snail[i], snailrect[i])

    pygame.display.flip()

    time.sleep (0.01)
