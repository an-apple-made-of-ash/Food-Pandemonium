import pygame
import os
pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

radius = 50
cover_surf = pygame.Surface((radius*2, radius*2))
cover_surf.fill(0)
cover_surf.set_colorkey((255, 255, 255))
pygame.draw.circle(cover_surf, (255, 255, 255), (radius, radius), radius)

# Player setup
player = pygame.Rect(100, 100, 32, 32)  # Example player rect
speed = 1

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

    # clip_center = pygame.mouse.get_pos()

    # clear screen and set clipping region
    window.fill(0)    
    clip_rect = pygame.Rect((new_position.x)/1.5, (new_position.y)/1.5, radius*2, radius*2)
    window.set_clip(clip_rect)

    # draw the scene
    ts, w, h, c1, c2 = 50, *window.get_size(), (255, 255, 255), (255, 0, 0)
    tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
    for rect, color in tiles:
        pygame.draw.rect(window, color, rect)
    
    pygame.draw.rect(window, (0,255,0), player)
    # pygame.display.update()

    # draw transparent circle and update display
    window.blit(cover_surf, clip_rect)
    pygame.display.flip()

pygame.quit()
exit()