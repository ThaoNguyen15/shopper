import os, sys
import pygame

import pygame.locals as l

if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')

### Helper Functions #######
def load_image(name, colorkey=None):
    # Source: http://www.pygame.org/docs/tut/ChimpLineByLine.html
    fullname = os.path.join('data/images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print('Cannot load image:{0}'.format(name))
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

###########################

class PyShopMain():
    """The class that handles visualization for shopping algo"""
    def __init__(self, width=640, height=480):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))

    def load_sprites(self):
        self.shopper = pyShopper()
        self.shopper_sprites = pygame.sprite.RenderPlain((self.shopper))
        
    def play(self):
        self.load_sprites()
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255,255,255))
        
        self.screen.blit(self.background, (0, 0))
        self.shopper_sprites.draw(self.screen)
        pygame.display.flip()
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

class pyShopper(pygame.sprite.Sprite):
    def __init__(self):
        super(self.__class__()).__init__(self)
        self.image, self.rect = load_image('panda.png', -1)

    
if __name__ == '__main__':
    g = PyShopMain()
    g.play()
