#! python3

import pygame


class color_picker:
    def __init__(self, game):
        self.game = game
        self.col = self.green, self.yellow, self.blue, self.red,\
          self.orange, self.brown, self.purple = self.game.col
        self.screen = self.game.screen
        self.key = self.game.key
        self.key.extend([(pygame.K_y, "lc"), (pygame.K_z, "lc"),
          (pygame.K_x, "rc"), (pygame.K_c, "con"), (pygame.K_a, "add"),
          (pygame.K_d, "del"), (pygame.K_r, "rep"), (pygame.K_s, "stop")])
        self.Map = self.game.Map
        self.font = self.game.font
        self.down = False
        self.action = None
        self.index1 = 0
        self.index2 = 0
        self.final = [self.green]
        self.Map.cc = [self.green] * 7
        self.rct = pygame.Surface((30, 30))

    def add(self):
        if self.col[self.index2] not in self.final:
            self.final.append(self.col[self.index2])
        self.set_c()

    def replace(self):
        if self.col[self.index2] not in self.final:
            self.final[self.index1] = self.col[self.index2]
        self.set_c()

    def delete(self):
        if self.index1:
            del self.final[self.index1]
        self.set_c()

    def set_c(self):
        for x, c in enumerate(self.Map.cc):
            if x < len(self.final):
                self.Map.cc[x] = self.final[x]
            elif x in (1, 2, 4):
                self.Map.cc[x] = self.Map.cc[0]
            elif x in (3, 5):
                self.Map.cc[x] = self.Map.cc[1]
            else:
                self.Map.cc[x] = self.Map.cc[2]

    def blit(self):
        for x, c in enumerate(self.final):
            self.rct.set_alpha(255 if x == self.index1 else 150)
            self.rct.fill(c)
            self.screen.blit(self.rct, (10 + x * 35, 10))
        for x, c in enumerate(self.col):
            self.rct.set_alpha(255 if x == self.index2 else 150)
            self.rct.fill(c)
            self.screen.blit(self.rct, (10 + x * 35, 50))
        if self.key["lc"] == 1:
            if self.down:
                self.index2 -= 1
            else:
                self.index1 -= 1
        if self.key["rc"] == 1:
            if self.down:
                self.index2 += 1
            else:
                self.index1 += 1
        self.index1 %= len(self.final)
        self.index2 %= len(self.col)
        if self.key["add"] == 1:
            self.action = "add"
            self.down = True
        if self.key["rep"] == 1:
            self.action = "replace"
        if self.key["del"] == 1:
            self.action = "delete"
        if self.key["con"] == 1 and self.action:
            if self.action == "replace" and not self.down:
                self.down = True
            else:
                getattr(self, self.action)()
                self.action = None
                self.down = False
        if self.key["stop"] == 1:
            self.action = None
            self.down = False
        if self.action:
            self.t = self.font.render(self.action[0].upper(), True,
              self.final[-1])
            self.screen.blit(self.t, (260, 0))
