#!/usr/bin/python3

import sys, pygame
import time
pygame.init()

myfont = pygame.font.SysFont ("monospace", 40)

N=4  # number of snails

size = width, height = 640, 480


class lettuce (object):


    def __init__ (self):
        self.sizes = [0, 10, 30, 50, 70, 90, 100]
        self.current_size = self.sizes.pop ()
        self.rect = None
        self.__load_image ()


    def __load_image (self):
        self.surface = pygame.image.load ('lettuce_%d%%.gif' % self.current_size)
        if self.rect is None:
            self.rect = self.surface.get_rect ()


    def take_a_bite (self):
        try:
            self.current_size = self.sizes.pop ()

        except IndexError:
            pass

        self.__load_image ()


    def move (self, speed):
        self.rect = self.rect.move (speed)


    @property
    def left (self):
        return self.rect.left


    @property
    def right (self):
        return self.rect.right


    def blit (self, screen):
        screen.blit (self.surface, self.rect)


class snail (object):

    NORMAL=0
    SURPRISED=1

    def __init__ (self):
        self.rect = None
        self.state = snail.NORMAL
        self.speed = [1, 0]

        self.__load_image ()


    def __load_image (self):
        if self.state is snail.NORMAL:
            self.surface = pygame.image.load ('snail-normal.gif')
        else:
            self.surface = pygame.image.load ('snail-surprised.gif')

        if self.rect is None:
            self.rect = self.surface.get_rect ()

        if self.speed[0] < 0:
            self.surface = pygame.transform.flip (self.surface, True, False)


    def move (self, speed=None):
        if speed is None:
            speed = self.speed

        self.rect = self.rect.move (speed)


    def set_surprised (self):
        if self.state is not snail.SURPRISED:
            self.state = snail.SURPRISED
            self.__load_image ()


    def set_normal (self):
        if self.state is not snail.NORMAL:
            self.state = snail.NORMAL
            self.__load_image ()


    def flip (self):
        self.speed = [-self.speed[0], self.speed[1]]
        self.__load_image ()


    @property
    def left (self):
        return self.rect.left


    @property
    def right (self):
        return self.rect.right


    def blit (self, screen):
        screen.blit (self.surface, self.rect)


    def update_speed (self, lettuce):
        sign = self.speed[0]/abs (self.speed[0])
        s = sign + (sign * 6 * abs (lettuce.current_size / (lettuce.right - self.left)))
        self.speed[0] = s


background = pygame.image.load ("background.gif")
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snail Race!!')

snails = [ snail () for i in range(N) ]
lettuces = [ lettuce () for i in range(N) ]

lettuce_keys = { pygame.K_1 : [ 0, [-5, 0] ],
                 pygame.K_2 : [ 0, [ 5, 0] ],
                 pygame.K_9 : [ 1, [-5, 0] ],
                 pygame.K_0 : [ 1, [ 5, 0] ],
                 pygame.K_z : [ 2, [-5, 0] ],
                 pygame.K_x : [ 2, [ 5, 0] ],
                 pygame.K_n : [ 3, [-5, 0] ],
                 pygame.K_m : [ 3, [ 5, 0] ] }

for i in range(N):
    snails[i].move([0, (height/N)*0.20+i*(height/N)])
    lettuces[i].move([(width/2), (height/N)*0.20+i*(height/N)])

winner = None

while winner is None:
    screen.blit(background, background.get_rect())

    for i, (snail, lettuce) in enumerate (zip (snails, lettuces)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in lettuce_keys:
                    j, move = lettuce_keys[event.key]
                    lettuces[j].move(move)

        snail.update_speed (lettuce)
        snail.move()

        if snail.right > width * 0.94:
            winner = i
            break

        if snail.right > lettuce.left-50 and snail.speed[0] > 0:
            snail.set_surprised ()

        if snail.right > lettuce.left and snail.speed[0] > 0:
            lettuce.take_a_bite ()
            snail.set_normal ()
            snail.flip ()

        if snail.left < 50 and snail.speed[0] < 0:
            snail.set_surprised ()

        if snail.left < 0 and snail.speed[0] < 0:
            snail.set_normal ()
            snail.flip ()

        snail.blit (screen)
        lettuce.blit (screen)

    pygame.display.flip()
    time.sleep (0.05)


while True:
    label = myfont.render ("Snail %d wins!!!" % (i+1), 1, (255,255,0))
    screen.blit (label, (width*0.2, height*0.5))
    pygame.display.flip()
    time.sleep (0.5)
    screen.blit(background, background.get_rect())
    pygame.display.flip()
    time.sleep (0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
