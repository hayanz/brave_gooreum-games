import pygame
from scenes import *
from objects import *
from options import *

pygame.init()
pygame.display.set_caption("Brave Gooreum")


# define the class of whole game
class Game:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.display = pygame.display.set_mode((self.row * TILE, self.col * TILE))

    # define the function to run the game
    def play(self):

        row, col = self.row, self.col
        display = self.display
        start = Start(row, col, display).run()
        if not start:
            return
        skip = Intro(row, col, display).run()
        if skip is None:
            return
        if not skip:
            ready = HowToPlay(row, col, display).run()
            if not ready:
                return
        while True:
            playing = Playing(row, col, display)
            game_over = playing.run()
            if game_over is None:
                break
            elif game_over:
                lose = GameOver(row, col, display)
                lose.set_score(playing.score)
                restart = lose.run()
            else:
                win = GameClear(row, col, display)
                win.set_score(playing.score)
                restart = win.run()
            if not restart:
                break


if __name__ == "__main__":
    Game(row=WIDTH, col=HEIGHT).play()

pygame.quit()
