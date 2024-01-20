import pygame
from tiles import *
from spritesheet import Spritesheet
# from player import Deliveryman
# from thief import Thief  # Assuming you have a Thief class defined

# Set up pygame
pygame.init()

# Set up the window and game loop
DISPLAY_W, DISPLAY_H = 800, 600
canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 60

# Load spritesheet and create deliveryman
spritesheet = Spritesheet('/Users/felicia/Documents/GitHub/hmmmmm/Room 3/R3Spritesheet.png')
# deliveryman = Deliveryman()
deliveryman = None  # Replace with your actual code to create Deliveryman instance

# Load the level
map = TileMap('Room3Map.csv', spritesheet)
# deliveryman.position.x, deliveryman.position.y = map.start_x, map.start_y

# Initialize thieves
#thieves_list = [Thief() for _ in range(5)]
#for thief in thieves_list:
    #thief.random_spawn(map.tiles)

# Game loop
while running:
    dt = clock.tick(60) * 0.001 * TARGET_FPS

    # Check player input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         deliveryman.LEFT_KEY = True
        #     elif event.key == pygame.K_RIGHT:
        #         deliveryman.RIGHT_KEY = True
        #     elif event.key == pygame.K_SPACE:
        #         deliveryman.jump()
        #
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_LEFT:
        #         deliveryman.LEFT_KEY = False
        #     elif event.key == pygame.K_RIGHT:
        #         deliveryman.RIGHT_KEY = False

    # Update deliveryman and check for catching thieves
    # deliveryman.update(dt, map.tiles)
    #for thief in thieves_list:
        #thief.update(dt)
        # deliveryman.catch_thief(thief)

    # Check victory condition
    # if deliveryman.thieves_captured == 5:
    #     print("Congratulations! You caught all the thieves. Victory!")

    # Update window and display
    canvas.fill((0, 255, 0))
    map.draw_map(canvas)
    # deliveryman.draw(canvas)

    # Draw and update thieves
    #for thief in thieves_list:
        #thief.draw(canvas)

    window.blit(canvas, (0, 0))
    pygame.display.update()

# Quit pygame when the game loop exits
pygame.quit()
