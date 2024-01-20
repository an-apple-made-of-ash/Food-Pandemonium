import pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window title
pygame.display.set_caption("My First Game")

# Game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw screen
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()

# Create player and background
player = pygame.Surface((50, 50))
player.fill((255, 0, 0))
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((0, 0, 255))

# Draw screen
screen.blit(background, (0, 0))
screen.blit(player, (WIDTH // 2 - 25, HEIGHT // 2 - 25))
pygame.display.flip()

# Player position
player_pos = [WIDTH // 2 - 25, HEIGHT // 2 - 25]

# Check for events
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

# Get pressed keys
keys = pygame.key.get_pressed()

# Update player position
if keys[pygame.K_UP]:
    player_pos[1] -= 5
if keys[pygame.K_DOWN]:
    player_pos[1] += 5
if keys[pygame.K_LEFT]:
    player_pos[0] -= 5
if keys[pygame.K_RIGHT]:
    player_pos[0] += 5

# Draw the player at the new position
screen.blit(player, player_pos)
pygame.display.flip()