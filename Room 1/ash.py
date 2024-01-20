import pygame
import os
pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 32, 32)  # Example player rect
speed = 5
radius = 50

run = True
while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    new_position = player.copy()
    if keys[pygame.K_LEFT]:
        new_position.x -= speed
    if keys[pygame.K_RIGHT]:
        new_position.x += speed
    if keys[pygame.K_UP]:
        new_position.y -= speed
    if keys[pygame.K_DOWN]:
        new_position.y += speed

    player = new_position

    # draw the scene
    window.fill((0, 0, 0))
    
    
    pygame.draw.circle(window, (255, 255, 255), new_position.center, radius)
    pygame.draw.rect(window, (0,255,0), player)

    pygame.display.update()

    # draw transparent circle and update display
    # window.blit(cover_surf, clip_rect)
    pygame.display.flip()

pygame.quit()
exit()