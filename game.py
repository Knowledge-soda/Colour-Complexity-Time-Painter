#! python3

import pygame
import Mind

from doc.src import mapload, colors


class Game:
    def __init__(self):
        self.col = self.green, self.yellow, self.blue,\
          self.red, self.orange, self.brown, self.purple = (0, 90, 0),\
          (255, 255, 25), (80, 80, 255), (160, 0, 0), (255, 140, 25),\
          (80, 40, 0), (0, 0, 90)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.init()

        self.PL = [Mind.Imagination.PLACE() for x in range(2)]
        self.G = Mind.Imagination.Game(self.PL[0])

        self.key = Mind.Imagination.Keyboard(Mind.Imagination.ARROWS +
          Mind.Imagination.HIT + [(pygame.K_ESCAPE, "quit")])
        self.G.declare(Mind.Imagination.Vertical_menu, distance=200,
          off=(-10, 0), off_type="%", keyboard=self.key)

        self.font = pygame.font.SysFont("Times new roman", 50)
        self.G.define(type=Mind.Imagination.text_option, font=self.font,
          color=self.green, pos_do=Mind.Imagination.joined(
          [Mind.Imagination.ch_color(self.brown),
          Mind.Imagination.ch_pos((10, 0))]), anti_pos_do=
          Mind.Imagination.reset())

        self.Main_menu = self.G.set_from(places=self.PL[0])

        self.Main_menu.set_from(True, text="Start", do=Mind.Imagination.
          link(self.PL[1]))
        self.Main_menu.set_from(False, True, text="Game Title",
          type=Mind.Imagination.fake_txt_opt)
        self.Main_menu.set_from(text="Quit", do=Mind.Imagination.Quit)

        self.Main_menu.set_options()

        self.Map = mapload.Map(1, self)
        self.Map.set_camera_pos(0, 800)

        self.cp = colors.color_picker(self)

        self.clock = pygame.time.Clock()

    def main(self):
        while self.G.run():

            self.screen.fill((255, 255, 255))
            
            self.G.blit()

            if self.PL[1]:
                self.key.update()
                self.Map.blit()
                self.cp.blit()

            if self.key["quit"]:
                self.G.kill()

            pygame.display.flip()
            self.clock.tick(60)


game = Game()
game.main()

pygame.quit()
