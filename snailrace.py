#!/usr/bin/python3

import sys, pygame
import time
pygame.init()

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
    snails[i].move([0, i*(height/N)])
    lettuces[i].move([(width/2), i*(height/N)])

while True:
    screen.blit(background, background.get_rect())

    for i in range (N):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in lettuce_keys:
                    j, move = lettuce_keys[event.key]
                    lettuces[j].move(move)

        snails[i].move()

        if snails[i].right > lettuces[i].left-50 and snails[i].speed[0] > 0:
            snails[i].set_surprised ()

        if snails[i].right > lettuces[i].left and snails[i].speed[0] > 0:
            snails[i].set_normal ()
            snails[i].flip ()

        if snails[i].left < 50 and snails[i].speed[0] < 0:
            snails[i].set_surprised ()

        if snails[i].left < 0 and snails[i].speed[0] < 0:
            snails[i].set_normal ()
            snails[i].flip ()

        snails[i].blit (screen)
        lettuces[i].blit (screen)

    pygame.display.flip()

    time.sleep (0.01)
