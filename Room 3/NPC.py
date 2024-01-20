import pygame
import sys

pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Object settings
object_color = (255, 0, 0)
object_width, object_height = 50, 50
object_rect = pygame.Rect((screen_width - object_width) // 2, (screen_height - object_height) // 2, object_width, object_height)

# NPC settings
npc_icon = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Man.png")
npc_rect = npc_icon.get_rect()
npc_rect.x = screen_width - npc_rect.width - 20  # Adjust the x-coordinate to place it at the side
npc_rect.y = screen_height // 2 - npc_rect.height // 2

# Speech bubble settings
speech_bubble = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Portal.png")  # Replace with your speech bubble image
speech_bubble_rect = speech_bubble.get_rect()
speech_bubble_rect.x = npc_rect.x - speech_bubble_rect.width - 10
speech_bubble_rect.y = npc_rect.y - 10

# Time settings
visibility_duration = 3000  # in milliseconds (3 seconds)
start_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time

    # Check if the object should still be visible
    if elapsed_time < visibility_duration:
        screen.fill((255, 255, 255))  # Clear the screen
        pygame.draw.rect(screen, object_color, object_rect)  # Draw the object
        screen.blit(npc_icon, npc_rect)  # Draw the NPC with the icon
        screen.blit(speech_bubble, speech_bubble_rect)  # Draw the speech bubble
    else:
        # Object has been visible for the specified duration
        screen.fill((0, 0, 0))  # Clear the screen

    pygame.display.flip()
    clock.tick(60)
