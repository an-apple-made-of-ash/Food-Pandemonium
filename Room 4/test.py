# Importing pygame module 
import pygame 
from pygame.locals import *
  
# initiate pygame and give permission 
# to use pygame's functionality. 
pygame.init() 
  
# create the display surface object 
# of specific dimension. 
window = pygame.display.set_mode((800, 600)) 
  
# Add caption in the window 
pygame.display.set_caption('Player Movement') 
  
# Add player sprite 
image = pygame.image.load('C:/Users/ashle/Documents/ash/hmmmmm/Assets/DeliveryMan.png') 
  
  
# Store the initial 
# coordinates of the player in 
# two variables i.e. x and y. 
x = 100
y = 100
  
# Create a variable to store the 
# velocity of player's movement 
velocity = 12
  
# Creating an Infinite loop 
run = True
while run: 
  
    # Filling the background with 
    # white color 
    window.fill((255, 255, 255)) 
  
    # Display the player sprite at x 
    # and y coordinates 
    window.blit(image, (x, y)) 
  
    # iterate over the list of Event objects 
    # that was returned by pygame.event.get() 
    # method. 
    for event in pygame.event.get(): 
  
        # Closing the window and program if the 
        # type of the event is QUIT 
        if event.type == pygame.QUIT: 
            run = False
            pygame.quit() 
            quit() 
  
        # Checking event key if the type 
        # of the event is KEYDOWN i.e. 
        # keyboard button is pressed 
        if event.type == pygame.KEYDOWN: 
  
            # Decreasing the x coordinate 
            # if the button pressed is 
            # Left arrow key 
            if event.key == pygame.K_LEFT: 
                x -= velocity 
  
            # Increasing the x coordinate 
            # if the button pressed is 
            # Right arrow key 
            if event.key == pygame.K_RIGHT: 
                x += velocity 
  
            # Decreasing the y coordinate 
            # if the button pressed is 
            # Up arrow key 
            if event.key == pygame.K_UP: 
                y -= velocity 
  
            # Increasing the y coordinate 
            # if the button pressed is 
            # Down arrow key 
            if event.key == pygame.K_DOWN: 
                y += velocity 
  
        # Draws the surface object to the screen. 
        pygame.display.update()