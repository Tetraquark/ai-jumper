import random

import pygame

import colors
import jumper as jp
import platform as pl

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TEXT_FONT = "Arial"
FONT_SIZE = 15

class World():
    def __init__(self, shiftSpeed):
        self.platforms_sprite_list = pygame.sprite.Group()
        self.active_sprite_list = pygame.sprite.Group()
        self.shiftSpeed = shiftSpeed
        self.platforms_list = []

    def appendJumper(self, jumperObj):
        jumperObj.setWorld(self)
        self.active_sprite_list.add(jumperObj)

    def appendPlatform(self, platform):
        if(len(self.platforms_list) == 0):
            self.platforms_list.append(platform)
            self.platforms_sprite_list.add(platform)
        else:
            lastPlatform = self.platforms_list[len(self.platforms_list) - 1]
            platform.rect.x = lastPlatform.rect.x + lastPlatform.rect.width + lastPlatform.precipiceWidth
            self.platforms_list.append(platform)
            self.platforms_sprite_list.add(platform)

    def update(self):
        self.active_sprite_list.update()
        self.platforms_sprite_list.update()

        for platform in self.platforms_list:
            platform.rect.x -= self.shiftSpeed

    def draw(self, screen, font):
        self.active_sprite_list.draw(screen)
        for jumper in self.active_sprite_list:
            label = font.render(str(jumper.maxTravelLen - jumper.len_walked), 1, colors.BLACK)
            screen.blit(label, (jumper.rect.x, jumper.rect.y))
            label2 = font.render(str(jumper.populationNumber), 1, colors.BLACK)
            screen.blit(label2, (jumper.rect.x, jumper.rect.y + 20))

        self.platforms_sprite_list.draw(screen)

def run(generationSize, bestJumpersNum, mutantsJumpersNum, maxTravelLen, maxGenerationNum):
    """
    Runs the simulation of the genetic algorithm to select the best jumpers with MLP neural network.

    :param generationSize: number of jumpers in generation (int)
    :param bestJumpersNum: number of the best (elite) generation jumpers (int)
    :param mutantsJumpersNum: number of jumper-mutants in generation (int)
    :param maxTravelLen: maximum travel length for jumper
    :param maxGenerationNum: number of genetic algorithm iterations
    :return:
    """

    if bestJumpersNum + mutantsJumpersNum > generationSize:
        bestJumpersNum = generationSize / 2
        mutantsJumpersNum = generationSize / 2

    pygame.init()
    textsFont = pygame.font.SysFont(TEXT_FONT, FONT_SIZE)

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('AI-Jumper')
    current_fps = 128
    _fps_step = 32
    MAX_FPS = 1024
    MIN_FPS = 32

    # World parameters
    death_height = SCREEN_HEIGHT - 100
    shift_speed = 3 # Objects movement speed
    jumper_start_x = 25
    jumper_start_y = SCREEN_HEIGHT - 200

    # Init world
    world = World(shift_speed)
    jumpersGenerationList = []
    
    # First random population
    for j in range(generationSize):
        aiJumper = jp.Jumper(jumper_start_x + random.choice(range(-20,20)), jumper_start_y, 40, 60, colors.getColor(j),
                             0, shift_speed, death_height, maxTravelLen, SCREEN_HEIGHT)
        jumpersGenerationList.append(aiJumper)
        world.appendJumper(aiJumper)

    # Append platforms to new world
    maxTravelLenTmp = maxTravelLen
    maxTravelLenTmp += pl.PLATFORM_LEN_MAX + pl.PRECIPICE_LEN_MAX
    platformsNumber = 0
    while maxTravelLenTmp > 0:
        platformLen = random.choice(range(pl.PLATFORM_LEN_MIN, pl.PLATFORM_LEN_MAX))
        platformPrecipiceWidth = random.choice(range(pl.PRECIPICE_LEN_MIN, pl.PRECIPICE_LEN_MAX))
        maxTravelLenTmp -= platformLen + platformPrecipiceWidth
        world.appendPlatform(pl.Platform(platformLen, 100, SCREEN_HEIGHT - 100, platformPrecipiceWidth))
        platformsNumber += 1

    generationCounter = 0
    isBestFounded = False
    # Start genetic algorithm (simulation)
    print 'Start simulation: maximum length of travel = ' + str(maxTravelLen)
    while generationCounter < maxGenerationNum:
        print 'Generation N: ' + str(generationCounter)

        clock = pygame.time.Clock()
        isRunning = True
        while isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                    generationCounter = maxGenerationNum

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_fps -= _fps_step
                    if event.key == pygame.K_RIGHT:
                        current_fps += _fps_step

            if current_fps > MAX_FPS:
                current_fps = MAX_FPS
            elif current_fps < MIN_FPS:
                current_fps = MIN_FPS

            if isRunning:
                #Update world
                world.update()

                #Draw world
                screen.fill(colors.WHITE)
                world.draw(screen, textsFont)

                label = textsFont.render('RED - Jumper-mutants from the last generation.', 1, colors.RED)
                screen.blit(label, (10, 10))
                label = textsFont.render('BLUE - best Jumpers from the last generation.', 1, colors.BLUE)
                screen.blit(label, (10, 30))
                label = textsFont.render('OTHER COLORS - new Jumpers.', 1, (0,191,255))
                screen.blit(label, (10, 50))
                label = textsFont.render('FPS rate: ' + str(current_fps), 1, colors.BLACK)
                screen.blit(label, (SCREEN_WIDTH - 140, 10))
                label = textsFont.render('Generation # ' + str(generationCounter), 1, colors.BLACK)
                screen.blit(label, (SCREEN_WIDTH - 140, 30))

                # Check jumpers walk result
                aliveJumpersList = [jumper for jumper in jumpersGenerationList if not jumper.isDead]
                if len(aliveJumpersList) > 0:
                    for jumper in aliveJumpersList:
                        if jumper.len_walked >= maxTravelLen:
                            jumper.countFitness()
                            isRunning = False
                            isBestFounded = True
                            bestJumper = jumper

                # If all jumpers are dead
                else:
                    isRunning = False

                clock.tick(current_fps)
                pygame.display.flip()

        # Population estimation
        # sort population by travel length
        jumpersGenerationList = sorted(jumpersGenerationList, key=lambda jumper: jumper.len_walked, reverse=False)

        print 'The best length of travel: ' + str(jumpersGenerationList[generationSize - 1].len_walked)
        print 'The worst length of travel : ' + str(jumpersGenerationList[0].len_walked)
        print '+---------------------------------+'

        if not isBestFounded:
            # Reset world
            world = World(shift_speed)

            resetJumpersNum = len(jumpersGenerationList) - bestJumpersNum - mutantsJumpersNum
            firstEliteJumperIndex = len(jumpersGenerationList) - bestJumpersNum

            # Create new Jumpers with random neural network weights
            for i in range(0, resetJumpersNum):
                jumpersGenerationList[i] = jp.Jumper(jumper_start_x + random.choice(range(-20,20)), jumper_start_y, 40, 60,
                                                     colors.getColor(i), generationCounter + 1, shift_speed, death_height,
                                                     maxTravelLen, SCREEN_HEIGHT)
                world.appendJumper(jumpersGenerationList[i])

            # Create mutants population in new generation
            for i in range(resetJumpersNum, firstEliteJumperIndex):
                randomEliteJumper = jumpersGenerationList[random.randint(firstEliteJumperIndex, len(jumpersGenerationList) - 1)]
                # Cross the jumpers brains
                jumpersGenerationList[i].gmlpBrain.cross(randomEliteJumper.gmlpBrain.weights)
                jumpersGenerationList[i].gmlpBrain.mutate()
                jumpersGenerationList[i].resetJumper(jumper_start_x, jumper_start_y)
                jumpersGenerationList[i].setColor(colors.RED)
                world.appendJumper(jumpersGenerationList[i])

            # Save best Jumpers of last generation in new generation
            for i in range(firstEliteJumperIndex, len(jumpersGenerationList) - 1):
                jumpersGenerationList[i].resetJumper(jumper_start_x, jumper_start_y)
                jumpersGenerationList[i].setColor(colors.BLUE)
                world.appendJumper(jumpersGenerationList[i])

            # Append platforms to new world
            for i in range(platformsNumber):
                world.appendPlatform(
                    pl.Platform(random.choice(range(pl.PLATFORM_LEN_MIN, pl.PLATFORM_LEN_MAX)), 100, SCREEN_HEIGHT - 100,
                             random.choice(range(pl.PRECIPICE_LEN_MIN, pl.PRECIPICE_LEN_MAX))))

            generationCounter += 1
        else:
            print ' '
            print '==================================================='
            print 'The best jumper comes from generation: ' + str(bestJumper.populationNumber)
            print 'The Jumper weights:'
            print bestJumper.gmlpBrain.weights
            generationCounter = maxGenerationNum

    if not isBestFounded:
        print ' '
        print '==================================================='
        print 'No jumper has reached maximum travel length.'

    pygame.quit()

if __name__ == "__main__":
    run()