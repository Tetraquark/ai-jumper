# Colors constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 204, 255)
VIOLET = (149, 95, 220)
DIRTY_YELLOW = (226, 155, 40)

colorsList = [(250, 235, 215), (0, 255, 255), (127, 255, 212),
              (255, 102, 204), (165, 42, 42), (220, 20, 60),
              (182, 249, 95), (219, 163, 32), (255, 140, 0)]

def countIndexShift(index, maxIndex):
    i = index
    if i > maxIndex:
        divider = index / maxIndex
        #if index % maxIndex == 0:
        #    divider -= 1
        i = index - divider * maxIndex
    return i

def getColor(index):
    global colorsList
    colorIndex = countIndexShift(index, len(colorsList) - 1)
    return colorsList[colorIndex]