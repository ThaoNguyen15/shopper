import os, sys
import pygame

import pygame.locals as l


class PyShopMain():
    """The class that handles visualization for shopping algo"""
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def play(self):
        # Draw initial state
        # Calculate Path
        # Animate the calculated path
        # Exit
        # TODO: delete this block after testing
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
        sys.exit()

if __name__ == '__main__':
    g = PyShopMain()
    g.play()
