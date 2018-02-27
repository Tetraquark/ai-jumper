import pygame

import colors
import geneticmlp as gmlp

JUMP_Y_SPEED = -8

class Jumper(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color, populationNumber, shift_speed, death_y, maxTravelLen, screen_height, gmlpBrain = None):
        super(Jumper, self).__init__()

        self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.color = color

        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0

        self.death_y = death_y
        self.shift_speed = shift_speed

        self.gmlpBrain = gmlp.GeneticMLP(2,6,1)
        self.gmlpBrain.reset()
        if gmlpBrain is not None:
            self.gmlpBrain.weights = gmlpBrain
        self.isDead = False
        self.len_walked = 0
        self.maxTravelLen = maxTravelLen
        self.populationNumber = populationNumber
        self.screen_height = screen_height

        self.myFitness = 0

    def update(self):
        # Calc gravity
        self.calc_gravity()

        self.rect.x += 2
        platforms_hit_list = pygame.sprite.spritecollide(self, self.world.platforms_sprite_list, False)
        self.rect.x -= 2

        if len(platforms_hit_list) > 0:
            self.change_x = -1 * self.shift_speed

        # Move right/left
        self.rect.x += self.change_x

        # Move up/down
        self.rect.y += self.change_y
        platforms_hit_list = pygame.sprite.spritecollide(self, self.world.platforms_sprite_list, False)
        for platform in platforms_hit_list:

            if self.change_y > 0:
                self.rect.bottom = platform.rect.top
            elif self.change_y < 0:
                self.rect.top = platform.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

        if not self.isDead:
            self.len_walked += self.shift_speed

            if self.rect.y >= self.death_y:
                self.image.fill(colors.BLACK)
                self.isDead = True
                self.countFitness()

            # Take decision about jump
            if len(platforms_hit_list) > 0:
                platform = platforms_hit_list[0]
                platform_surface_len = platform.rect.x + platform.rect.width - self.rect.x

                precipice_len = platform.precipiceWidth

                # Asks the jumper brain
                decision = self.gmlpBrain.propagate_forward([float(precipice_len),
                                                             float(platform_surface_len)])
                if decision[0] > 0.6:
                    self.jump()

    def draw(self, screen):
        borderWidth = 2
        pygame.draw.rect(screen, colors.BLACK, [self.rect.x - borderWidth, self.rect.y - borderWidth,
                                                self.rect.width + borderWidth, self.rect.height + borderWidth], borderWidth)
        pygame.draw.rect(screen, self.color, self.rect)

    def calc_gravity(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        # Check if object is on the ground
        if self.rect.y >= self.screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = self.screen_height - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.world.platforms_sprite_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screen_height:
            self.change_y = JUMP_Y_SPEED

    def setWorld(self, world):
        self.world = world

    def setColor(self, color):
        self.image.fill(color)

    def resetJumper(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.myFitness = 0
        self.isDead = False
        self.len_walked = 0
        self.change_x = 0

    def countFitness(self):
        self.myFitness = self.len_walked #self.maxTravelLen - self.len_walked