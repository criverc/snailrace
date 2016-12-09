#!/usr/bin/python3

import sys
import os
import time
import pygame

#Added os for joining paths when loading music
import snailracerc

pygame.init()

FONT = pygame.font.SysFont("monospace", 40)

NO_SNAILS = 4  # number of snails

SIZE = WIDTH, HEIGHT = 640, 480


class Lettuce(object):


    def __init__(self):
        self.sizes = [0, 10, 30, 50, 70, 90, 100]
        self.current_size = self.sizes.pop()
        self.rect = None
        self.__load_image()


    def __load_image(self):
        self.surface = pygame.image.load(os.path.join(snailracerc.path,
                                                      'lettuce_%d%%.gif' % self.current_size))
        if self.rect is None:
            self.rect = self.surface.get_rect()


    def take_a_bite(self):
        try:
            self.current_size = self.sizes.pop()
        except IndexError:
            pass
        self.__load_image()


    def move(self, speed):
        self.rect = self.rect.move(speed)


    @property
    def left(self):
        return self.rect.left


    @property
    def right(self):
        return self.rect.right


    def blit(self, screen):
        screen.blit(self.surface, self.rect)


class Snail(object):


    NORMAL = 0
    SURPRISED = 1


    def __init__(self):
        self.rect = None
        self.state = Snail.NORMAL
        self.speed = [1, 0]

        self.__load_image()


    def __load_image(self):
        if self.state is Snail.NORMAL:
            self.surface = pygame.image.load(os.path.join(snailracerc.path, 'snail-normal.gif'))
        else:
            self.surface = pygame.image.load(os.path.join(snailracerc.path, 'snail-surprised.gif'))

        if self.rect is None:
            self.rect = self.surface.get_rect()

        if self.speed[0] < 0:
            self.surface = pygame.transform.flip(self.surface, True, False)


    def move(self, speed=None):
        if speed is None:
            speed = self.speed

        self.rect = self.rect.move(speed)


    def set_surprised(self):
        if self.state is not Snail.SURPRISED:
            self.state = Snail.SURPRISED
            self.__load_image()


    def set_normal(self):
        if self.state is not Snail.NORMAL:
            self.state = Snail.NORMAL
            self.__load_image()


    def flip(self):
        self.speed = [-self.speed[0], self.speed[1]]
        self.__load_image()


    @property
    def left(self):
        return self.rect.left


    @property
    def right(self):
        return self.rect.right


    def blit(self, screen):
        screen.blit(self.surface, self.rect)


    def update_speed(self, lettuce):
        sign = self.speed[0]/abs(self.speed[0])
        new_speed = sign + (sign * 6 * abs(lettuce.current_size / (lettuce.right - self.left)))
        self.speed[0] = new_speed


BACKGROUND = pygame.image.load(os.path.join(snailracerc.path, "background.gif"))
SCREEN = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption('Snail Race!!')

__snails__ = [Snail() for i in range(NO_SNAILS)]
__lettuces__ = [Lettuce() for i in range(NO_SNAILS)]

__lettuce_keys__ = {pygame.K_1 : [0, [-5, 0]],
                    pygame.K_2 : [0, [5, 0]],
                    pygame.K_9 : [1, [-5, 0]],
                    pygame.K_0 : [1, [5, 0]],
                    pygame.K_z : [2, [-5, 0]],
                    pygame.K_x : [2, [5, 0]],
                    pygame.K_n : [3, [-5, 0]],
                    pygame.K_m : [3, [5, 0]]}

for i in range(NO_SNAILS):
    __snails__[i].move([0, (HEIGHT/NO_SNAILS) * 0.20 + i * (HEIGHT/NO_SNAILS)])
    __lettuces__[i].move([(WIDTH/2), (HEIGHT/NO_SNAILS) * 0.20 + i * (HEIGHT/NO_SNAILS)])

__winner__ = None
# Load music to game
pygame.mixer.music.load(os.path.join(snailracerc.path, "intro.ogg"))
pygame.mixer.music.play(-1)

while __winner__ is None:
    SCREEN.blit(BACKGROUND, BACKGROUND.get_rect())

    for i, (snail, lettuce) in enumerate(zip(__snails__, __lettuces__)):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in __lettuce_keys__:
                    j, move = __lettuce_keys__[event.key]
                    __lettuces__[j].move(move)

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        snail.update_speed(lettuce)
        snail.move()

        if snail.right > WIDTH * 0.94:
            __winner__ = i
            break

        if snail.right > lettuce.left-50 and snail.speed[0] > 0:
            snail.set_surprised()

        if snail.right > lettuce.left and snail.speed[0] > 0:
            lettuce.take_a_bite()
            snail.set_normal()
            snail.flip()

        if snail.left < 50 and snail.speed[0] < 0:
            snail.set_surprised()

        if snail.left < 0 and snail.speed[0] < 0:
            snail.set_normal()
            snail.flip()

        snail.blit(SCREEN)
        lettuce.blit(SCREEN)

    pygame.display.flip()
    time.sleep(0.05)


while True:
    LABEL = FONT.render("Snail %d wins!!!" % (i+1), 1, (255, 255, 0))
    SCREEN.blit(LABEL, (WIDTH*0.2, HEIGHT*0.5))
    pygame.display.flip()
    time.sleep(0.5)
    SCREEN.blit(BACKGROUND, BACKGROUND.get_rect())
    pygame.display.flip()
    time.sleep(0.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
