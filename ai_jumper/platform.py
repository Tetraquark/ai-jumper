import pygame

import colors

PRECIPICE_LEN_MAX = 160
PRECIPICE_LEN_MIN = 20

PLATFORM_LEN_MIN = 200
PLATFORM_LEN_MAX = 400

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, y, precipiceWidth):
        super(Platform, self).__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(colors.GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = y
        self.precipiceWidth = precipiceWidth

    def draw(self, screen):
        pygame.draw.rect(screen, colors.DIRTY_YELLOW,
                         [self.rect.x, self.rect.y, self.rect.width - 2, self.rect.height], 2)