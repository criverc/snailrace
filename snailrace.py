import sys, pygame
import time
pygame.init()

N=4  # number of snails

size = width, height = 640, 480

background = pygame.image.load ("background.gif")
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snail Race!!')

snail = [ pygame.image.load("snail-normal.gif") for i in range(N) ]
snailrect = [ snail[i].get_rect() for i in range(N) ]
lettuce = [ pygame.image.load ("lettuce.gif") for i in range(N) ]
lettuce_rect = [ lettuce[i].get_rect() for i in range(N) ]

speed = [ [1, 0] for i in range(N) ]

lettuce_keys = { pygame.K_1 : [ 0, [-5, 0] ],
                 pygame.K_2 : [ 0, [ 5, 0] ],
                 pygame.K_9 : [ 1, [-5, 0] ],
                 pygame.K_0 : [ 1, [ 5, 0] ],
                 pygame.K_z : [ 2, [-5, 0] ],
                 pygame.K_x : [ 2, [ 5, 0] ],
                 pygame.K_n : [ 3, [-5, 0] ],
                 pygame.K_m : [ 3, [ 5, 0] ] }

for i in xrange(N):
    snailrect[i] = snailrect[i].move([0, i*(height/N)])
    lettuce_rect[i] = lettuce_rect[i].move([(width/2), i*(height/N)])

while 1:
    screen.blit(background, background.get_rect())

    for i in xrange (N):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if lettuce_keys.has_key (event.key):
                    j, move = lettuce_keys[event.key]
                    lettuce_rect[j] = lettuce_rect[j].move(move)

        snailrect[i] = snailrect[i].move(speed[i])
        if snailrect[i].right > lettuce_rect[i].left-50 and speed[i][0]>0:
            snail[i] = pygame.image.load("snail-surprised.gif")

        if snailrect[i].left < 0 or snailrect[i].right > lettuce_rect[i].left:
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
        screen.blit(lettuce[i], lettuce_rect[i])

    pygame.display.flip()

    time.sleep (0.01)
