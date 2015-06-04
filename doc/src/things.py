#! python3

import pygame
from Mind import Orientation


class GameEndedError(Exception):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class plat(Orientation.Object):
    def __init__(self, name, Type, props, Map, obj):
        super().__init__(name, Type, props, Map, obj)
        self.x, self.y = self.obj.get_xy()
        self.width = self.obj.width
        self.height = self.obj.height
        self.screen = self.Map.screen
        self.name = "platforms"
        self.Map.clone_obj("player", "type").add_plat(self)

    def blit(self):
        self.X, self.Y = self.get_blit()
        pygame.draw.rect(self.screen, self.Map.cc[1], pygame.Rect(self.X,
          self.Y, self.width, self.height))

    def get_blit(self):
        return (self.x - self.Map.x, self.y - self.Map.y)


class player(Orientation.Subject):
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, None, Map, obj)
        self.Pictures = [pygame.image.load("doc/art/drw/ply/" + str(x + 1)
          + ".bmp") for x in range(3)]
        for picture in self.Pictures:
            picture.set_colorkey((255, 255, 255))
        self.obj.width, self.obj.height = self.width, self.height =\
          self.Pictures[0].get_size()
        self.pictures = {c: [pic.copy() for pic in self.Pictures] for c in
          Map.col}
        for y in range(self.height):
            for x in range(self.width):
                for n, picture in enumerate(self.Pictures):
                    if picture.get_at((x, y)) == (0, 0, 0):
                        for col in self.Map.col:
                            self.pictures[col][n].set_at((x, y), col)

        self.fy = 0
        self.plats = []
        self.key = self.Map.game.key
        self.ground = False
        self.state = 0
        self.new = True
        self.history = []
        self.last = [self.x, self.y, 0]
        self.point = Orientation.point(self.x + self.width / 2, self.y +
          self.height / 2, self.Map.in_map)
        self.sh = self.Map.height

    def add_plat(self, plat):
        self.plats.append(plat)

    def blit(self):
        self.picture = self.pictures[self.Map.cc[0]][self.state]

        if self.Map.cc[0] in (self.Map.green, self.Map.blue, self.Map.red):
            self.factor = 1 if self.Map.cc[0] == self.Map.green else 0.5\
              if self.Map.cc[0] == self.Map.blue else 2
            self.fy += 0.12 * self.factor
            self.move(0, self.fy * self.factor)

            self.obj.x = self.x
            self.obj.y = self.y

            self.point.x = self.x + self.width / 2
            self.point.y = self.y + self.height / 2

            self.ground = False
            for pl in self.plats:
                self.cll = self.obj.collide(pl.obj)
                if self.cll[1]:
                    if min(filter(lambda x: x, self.cll[:-1])) ==\
                      self.cll[1]:
                        self.y = pl.y - self.height
                        self.fy = 0
                        self.ground = pl
                    else:
                        if min(self.cll[0], self.cll[2]) == self.cll[0]:
                            self.x = pl.x + pl.width
                        else:
                            self.x = pl.x - self.width
                if self.cll[3]:
                    if min(filter(lambda x: x, self.cll[1:] +
                      [self.cll[0]])) == self.cll[3]:
                        self.y = pl.y + pl.height
                        self.fy = 0
                    else:
                        if min(self.cll[0], self.cll[2]) == self.cll[0]:
                            self.x = pl.x + pl.width
                        else:
                            self.x = pl.x - self.width

            if self.key["left"]:
                self.move(-2 * self.factor, 0)
            if self.key["right"]:
                self.move(2 * self.factor, 0)
            if self.key["left"] or self.key["right"]:
                self.state = max((self.state + self.new) % 3, 1)
                self.new = not self.new
            else:
                self.state = 0
            if self.key["up"] == 1 and self.ground:
                self.fy = -6
            self.New = [(self.x - self.last[0]) / self.factor, self.fy *
              self.factor]
            if self.history and self.New == self.history[-1][:2]:
                self.history[-1][2] += 1
            else:
                self.history.append(self.New + [0])
            self.last = [self.x, self.y]

        if self.Map.cc[0] == self.Map.yellow:
            if self.history:
                self.move_r(*self.history[-1][:2])
                if self.history[-1][2]:
                    self.history[-1][2] -= 1
                else:
                    del self.history[-1]

        if self.y > self.sh:
            raise GameEndedError("You died. It's also a choice but is it good one?" if self.Map.n < 7 else "You won! Or you didn't?")

        super().blit()

    def move_r(self, x, y):
        self.move(-x, -y)


class enemy(Orientation.map_obj):
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, None, Map, obj)
        self.Pictures = [pygame.image.load("doc/art/drw/enm/" + str(x + 1)
          + ".bmp") for x in range(3)]
        for picture in self.Pictures:
            picture.set_colorkey((255, 255, 255))
        self.obj.width, self.obj.height = self.width, self.height =\
          self.Pictures[0].get_size()
        self.pictures = {c: [pic.copy() for pic in self.Pictures] for c in
          Map.col}
        for y in range(self.height):
            for x in range(self.width):
                for n, picture in enumerate(self.Pictures):
                    if picture.get_at((x, y)) == (0, 0, 0):
                        for col in self.Map.col:
                            self.pictures[col][n].set_at((x, y), col)

        self.fy = 0
        self.ground = False
        self.state = 0
        self.new = False
        self.last = [self.x, self.y]
        self.history = []
        self.centre = Orientation.point(self.x + self.width / 2, self.y +
          self.height / 2, self.Map, quiet=True)
        self.view = Orientation.circle(self.centre, 200, self.Map.in_map)
        self.pl = self.Map.clone_obj("player", "type")
        self.plats = self.pl.plats
        self.jump = None

    def blit(self):
        self.picture = self.pictures[self.Map.cc[2]][self.state]

        if self.Map.cc[2] in (self.Map.green, self.Map.blue, self.Map.red):
            self.factor = 1 if self.Map.cc[0] == self.Map.green else 0.5\
              if self.Map.cc[0] == self.Map.blue else 2
            self.fy += 0.12 * self.factor
            self.move(0, self.fy * self.factor)

            self.obj.x = self.x
            self.obj.y = self.y

            self.ground = False
            for pl in self.plats:
                self.cll = self.obj.collide(pl.obj)
                if self.cll[1]:
                    if min(filter(lambda x: x, self.cll[:-1])) ==\
                      self.cll[1]:
                        self.y = pl.y - self.height
                        self.fy = 0
                        self.ground = pl
                    else:
                        if min(self.cll[0], self.cll[2]) == self.cll[0]:
                            self.x = pl.x + pl.width
                        else:
                            self.x = pl.x - self.width
                if self.cll[3]:
                    if min(filter(lambda x: x, self.cll[1:] +
                      [self.cll[0]])) == self.cll[3]:
                        self.y = pl.y + pl.height
                        self.fy = 0
                    else:
                        if min(self.cll[0], self.cll[2]) == self.cll[0]:
                            self.x = pl.x + pl.width
                        else:
                            self.x = pl.x - self.width
            if self.pl.point in self.view:
                if self.pl.point.x < self.view.centre.x:
                    if self.ground == self.pl.ground:
                        self.move_x(-min(1, self.centre.x -
                          self.pl.point.x))
                    else:
                        if self.ground and self.pl.ground:
                            if self.ground.y > self.pl.ground.y:
                                self.dx = self.x - (self.pl.ground.x +
                                  self.pl.ground.width)
                                self.dy = self.ground.y - self.pl.ground.y
                                if self.dy <= 153 and self.dx < 101 and\
                                  (self.dx <= 51 or self.dy < (101 -
                                  self.dx) * 0.12):
                                    self.jump = "left"
                                    self.fy -= 6
                                    self.ground = False
                                else:
                                    self.move_x(-min(1, self.x -
                                      self.ground.x))
                            else:
                                self.move_x(1 if self.centre.x >
                                  self.ground.width / 2 else -1)
                                
                elif self.pl.point.x > self.view.centre.x:
                    if self.ground == self.pl.ground:
                        self.move_x(min(1, self.pl.point.x -
                          self.centre.x))
                    else:
                        if self.ground and self.pl.ground:
                            if self.ground.y > self.pl.ground.y:
                                self.dx = self.pl.ground.x - (self.x +
                                  self.width)
                                self.dy = self.ground.y - self.pl.ground.y
                                if self.dy <= 153 and self.dx < 101 and\
                                  (self.dx <= 51 or self.dy < (101 -
                                  self.dx) * 0.12):
                                    self.jump = "right"
                                    self.fy -= 6
                                    self.ground = False
                                else:
                                    self.move_x(min(1, self.ground.x +
                                      self.ground.width - self.x))
                            else:
                                self.move_x(1 if self.centre.x >
                                  self.ground.width / 2 else -1)
            else:
                self.state = 0

            if self.ground:
                self.jump = None

            self.centre.x = self.x + self.width / 2
            self.centre.y = self.y + self.height / 2

            if self.jump:
                self.move_x(-1 if self.jump == "left" else 1)

            self.New = [(self.x - self.last[0]) / self.factor, self.fy *
              self.factor]
            if self.history and self.New == self.history[-1][:2]:
                self.history[-1][2] += 1
            else:
                self.history.append(self.New + [0])
            self.last = [self.x, self.y]

        if self.Map.cc[0] == self.Map.yellow:
            if self.history:
                self.move_r(*self.history[-1][:2])
                if self.history[-1][2]:
                    self.history[-1][2] -= 1
                else:
                    del self.history[-1]

        if any(self.obj.collide(self.pl.obj)):
            raise GameEndedError("You died. It's also a choice but is it good one?")

        super().blit()

    def move_x(self, x):
        self.x += x * self.factor
        self.state = max((self.state + self.new) % 3, 1)
        self.new = not self.new

    def move_r(self, x, y):
        self.move(-x, -y)


class statue(Orientation.map_obj):
    def __init__(self, name, Type, props, picture, Map, obj):
        super().__init__(name, Type, props, pygame.image.load("doc/art/drw/com.bmp"), Map, obj)
        self.player = self.Map.clone_obj("player", "type")
        self.picture.set_colorkey((255, 255, 255))
        self.obj.width, self.obj.height = self.width, self.height =\
          self.picture.get_size()
        self.pictures = {c: self.picture.copy() for c in Map.col}
        for y in range(self.height):
            for x in range(self.width):
                if self.picture.get_at((x, y)) == (0, 0, 0):
                    for col in self.Map.col:
                        self.pictures[col].set_at((x, y), col)

    def blit(self):
        self.picture = self.pictures[self.Map.cc[-1]]
        super().blit()
        if any(self.obj.collide(self.player.obj)):
            if self.Map.n == 7:
                raise GameEndedError("You won! Or you didn't?")
            self.Map.Next()
