#! python3

import sys

import pygame
from Mind import Orientation, Imagination

from . import things


class Map(Orientation.tiled_map):
    def __init__(self, n, game):
        self.n = n
        self.game = game
        self.col = self.green, self.yellow, self.blue, self.red,\
          self.orange, self.brown, self.purple = self.game.col
        self.pr = Imagination.printer(100, 100, self.game.font, self.brown)
        sys.__stdout__ = sys.stdout
        sys.stdout = self.pr
        self.key = self.game.key
        self.key.extend([(pygame.K_e, "Easter Egg")])
        if self.n == 1:
            print("They sent me in this weird game to return Simplicity.")
            print("To steal those Statues of Complexity with big noses!")
        elif self.n == 2:
            print("I'm a bit mad at them.")
            print("They haven't even made good game.")
        elif self.n == 3:
            print("It's buggy, unfinished, without sounds.")
            print("Why should I listen to them?")
        elif self.n == 4:
            print("They are against Complexity and they praise Simplicity.")
            print("And I'm quite complex as Time Painter.")
        elif self.n == 5:
            print("They will probably steal my Colours.")
            print("But Simplicity obviously have it's price.")
        elif self.n == 6:
            print("Should I work for people who will steal my time because")
            print("I'm different?")
            print("Should I help others and end Complexity of Colours?")
        elif self.n == 7:
            print("It's your choice! Simplicity vs Complexity,")
            print("normall vs different, one-coloured vs more-coloured,")
            print("mass vs individual, marytr vs tortuer.")
            print("You can pick last Statue or send me outside the Screen.")
        super().__init__("doc/art/map/" + str(n), [{}, {"platforms":
          pl_group}, {"player": things.player, "enemy": things.enemy,
          "statue": things.statue}])

    def blit(self):
        super().blit()
        self.pr.blit()
        if self.key["Easter Egg"]:
            if self.n not in (3, 6):
                self.pr.text = ""
            if self.n == 1:
                print("I've decided to make this weird game for 96h Jam.")
                print("But they didn't want me to make any games!")
            if self.n == 2:
                print("I'm a bit mad at them.")
                print("I haven't even made good game.")
            if self.n == 4:
                print("They are against complexity and they praise normall.")
                print("And I'm quite complex as game maker.")
            if self.n == 5:
                print("They will probably destroy my will and hope.")
                print("But normall life obviously have it's price.")
            if self.n == 7:
                print("It's my choice! Life vs Programming,")
                print("normall vs different, hard-worker vs game-maker,")
                print("mass vs individual, marytr vs tortuer.")
                print("You can do anything but that's my choice!")
                print("And I will chose the Right way!")

    def Next(self):
        self.__init__(self.n + 1, self.game)


class pl_group(Orientation.element):
    def __init__(self, name, props, objects, Map):
        super().__init__(name, props, Map)
        self.objects = objects

    @classmethod
    def __tmx_x_init__(cls, obj, Map):
        super().__tmx_x_init__(obj, Map)
        objects = []
        for P in obj:
            if P.tag == "object":
                objects.append(things.plat.__tmx_x_init__(P, Map))
        return pl_group(cls.name, cls.properties, objects, Map)

    def blit(self):
        for obj in self.objects:
            obj.blit()
    
