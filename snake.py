###
# Snake
###

### IMPORTS
import random
import pygame

### CONSTANTS
SNAKEBODYCOLOR = ( 20, 240,  20) # What color to draw the snake
SNAKEHEADCOLOR = (240, 255,  20) # Color of the snake's head
BORDERCOLOR =    ( 20, 240, 240) # Color of the screen border
APPLECOLOR =     (240,  20,  20) # What color to draw the apple
BGCOLOR =        (  0,   0,   0) # What color is the background

SIZE = 12                        # How big is each block?
APPLEPOINTS = 10                 # How many points per appls?
SCREENX = 50                     # How wide is the screen
SCREENY = 40                     # How tall is the screen

INITAPPLES = 3                   # How many apples to start with
APPLETIMER = 10                  # How many seconds before a new set of apples show up
SNAKEFADE = -3                   # How many segments to fade out

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

### Game Variables
snakeList = []                   # Where is the snake located
appleList = []                   # Where are all the apples
snakeDirection = DOWN            # Initial snake direction
score = 0                        # What's the current score?

### Init PyGame
pygame.init()

### FUNCTIONS
# Get a random point
def getRandomPoint(x, y):
    return (random.randint(2,x), random.randint(2,y))

# What is the next point in this direction?
def getNextPoint(point,direction):
    if direction == UP:
        return (point[0], point[1]-1)
    elif direction == DOWN:
        return (point[0], point[1]+1)
    elif direction == LEFT:
        return (point[0]-1, point[1])
    else:
        return (point[0]+1, point[1])

# Seed our initial apple load
# Returns a set of points
def initApples(numApples):
    appleList = []
    while numApples > 0:
        appleList.append(getRandomPoint(SCREENX-1,SCREENY-1))
        numApples -= 1
    return appleList

# Draw apples
def drawApples():
    global window
    for apple in appleList:
        appleRect = pygame.Rect(((apple[0]-1)*SIZE+1),
                                ((apple[1]-1)*SIZE+1),
                                SIZE-2, SIZE-2)
        pygame.draw.rect(window, APPLECOLOR, appleRect)

# Draw snake
def drawSnake():
    global window

    # First, draw the snake's head
    snakeHead = snakeList[0]
    snakeRect = pygame.Rect(((snakeHead[0]-1)*SIZE+1),
                            ((snakeHead[1]-1)*SIZE+1),
                            SIZE-2, SIZE-2)
    pygame.draw.rect(window, SNAKEHEADCOLOR, snakeRect)

    # Now, draw the body of the snake
    for snake in snakeList[1:SNAKEFADE]:
        snakeRect = pygame.Rect(((snake[0]-1)*SIZE+1),
                                ((snake[1]-1)*SIZE+1),
                                SIZE-2, SIZE-2)
        pygame.draw.rect(window, SNAKEBODYCOLOR, snakeRect)

    # Now fade out the last few segments
    colorFade = -180 // SNAKEFADE
    greenFade = SNAKEBODYCOLOR[1]-colorFade
    for snake in snakeList[SNAKEFADE:]:
        SNAKEFADECOLOR = (SNAKEBODYCOLOR[0],
                          greenFade,
                          SNAKEBODYCOLOR[2])
        snakeRect = pygame.Rect(((snake[0]-1)*SIZE+1),
                                ((snake[1]-1)*SIZE+1),
                                SIZE-2, SIZE-2)
        pygame.draw.rect(window, SNAKEFADECOLOR, snakeRect)
        greenFade -= colorFade
        

# Retuen a new direction in a clockwise motion
def clockwise(direction):
    if (direction == UP):
        return RIGHT
    if (direction == RIGHT):
        return DOWN
    if (direction == DOWN):
        return LEFT
    if (direction == LEFT):
        return UP

# Return a new direction in a counter clockwise motion
def counterclockwise(direction):
    if (direction == UP):
        return LEFT
    if (direction == RIGHT):
        return UP
    if (direction == DOWN):
        return RIGHT
    if (direction == LEFT):
        return DOWN
            
# Handle keyboard input
def processInput(key, direction):
    global running
    newDirection = direction
    if key == pygame.K_l:
        if direction == UP or direction == DOWN:
            newDirection = RIGHT
    elif key == pygame.K_j:
        if direction == UP or direction == DOWN:
            newDirection = LEFT
    elif key == pygame.K_i:
        if direction == RIGHT or direction == LEFT:
            newDirection = UP
    elif key == pygame.K_k:
        if direction == RIGHT or direction == LEFT:
            newDirection = DOWN
    elif key == pygame.K_RIGHT or key == pygame.K_PERIOD:
        newDirection = clockwise(direction)
    elif key == pygame.K_LEFT or key == pygame.K_COMMA:
        newDirection = counterclockwise(direction)

    elif key == pygame.K_q:
        running = False
        
    return newDirection

# Add a new head segment, removing the tail if 
def addSnakeSegment(direction, expandSnake):
    global snakeList

    snakeList.insert(0, getNextPoint(snakeList[0], direction))
    if not expandSnake:
        del snakeList[-1]

# Check if the snake hit something
# If it hit an apple, remove the apple and increase the score
# If it hit itself or ran off the screen, quit the game
def checkSnakeHit():
    global snakeList, points, running, speed, expandSnake
    snakeHead = snakeList[0]

    # First check for an apple hit
    if snakeHead in appleList:
        appleList.remove(snakeHead)
        points += APPLEPOINTS

        # Add a new apple to the screen, and make it visible
        newApple = getRandomPoint(SCREENX-1, SCREENY-1)
        while (newApple in appleList) or (newApple in snakeList):
            newApple = getRandomPoint(SCREENX-1, SCREENY-1)
        appleList.append(newApple)

        # Make the snake longer, and speed things up
        expandSnake = 3
        speed = 5 + points//50

    # Now check if we hit our own body
    # Need to ignore the actual head, so look from the 2nd element on    
    if snakeHead in snakeList[1:]:
        running = False
        print("Ouroboros not permitted!")

    # Now check for a wall hit
    if snakeHead[0]<=0 or snakeHead[0]>=SCREENX or snakeHead[1]<=0 or snakeHead[1]>=SCREENY:
        running = False
        print("Off screen!")

# Draw the screen properly
def drawScreen():
    global window

    # Draw a border rectangle to enclose the screen
    outerBorder = pygame.Rect(0, 0, SCREENX*SIZE, SCREENY*SIZE)
    innerBorder = pygame.Rect(SIZE, SIZE, (SCREENX-2)*SIZE, (SCREENY-2)*SIZE)

    pygame.draw.rect(window, BORDERCOLOR, outerBorder)
    pygame.draw.rect(window, BGCOLOR, innerBorder)

    # Draw the apples and the current form of the snake
    drawApples()
    drawSnake()


### Main Flow
# Setup PyGame board
pygame.init()
window = pygame.display.set_mode(((SCREENX*SIZE), (SCREENY*SIZE)))
pygame.display.set_caption("Snake Byte!")

window.fill(BGCOLOR)

# Init basic game parameters
appleList += initApples(INITAPPLES)
snakeList = [(28, 14),
             (27, 14),
             (26, 14),
             (25, 14),
             (25, 13),
             (25, 12),
             (25, 11),
             (25, 10)]
snakeDirection = RIGHT
points = 0
speed = 5

running = True
expandSnake = 0
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snakeDirection = processInput(event.key, snakeDirection)

    # Add a new segment to the snake
    addSnakeSegment(snakeDirection, expandSnake>0)
    if expandSnake>0:
        expandSnake-=1

    # Check if the snake hit something
    checkSnakeHit()

    # Refresh the screen
    drawScreen();
    pygame.display.flip()
    clock.tick(speed)

print("Points: {}".format(points))
