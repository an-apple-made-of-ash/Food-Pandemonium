import os
import pygame
from pygame.locals import *
from tiles import *
from collide import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        super().__init__()
        self.img = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img,(30,30)) for img in self.img]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def move(self, keys, obstacles):
        new_position = self.rect.copy()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_position.y -= self.speed
            self.index = 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_position.y += self.speed
            self.index = 0
        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            new_position.x += self.speed
            self.index = 3
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            new_position.x -= self.speed
            self.index = 2

        self.image = self.images[self.index]

        # Check for collisions 
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # clear screen and set clipping region
        screen.fill(0)    
        clip_rect = pygame.Rect(new_position.x-radius+12, new_position.y-radius+12, radius*2, radius*2)
        screen.set_clip(clip_rect)

        # draw the scene
        ts, w, h, c1, c2 = 50, *screen.get_size(), (255, 255, 255), (255, 0, 0)
        tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
        for rect, color in tiles:
            pygame.draw.rect(screen, color, rect)
        
        pygame.draw.rect(screen, (0,255,0), player)
        # pygame.display.update()

        # draw transparent circle and update display
        screen.blit(cover_surf, clip_rect)

        


pygame.init() 

map = TileMap('room1_walls.csv')
screen = pygame.display.set_mode([800,600])
canvas = pygame.Surface([800,1200])
path = os.path.join(os.path.dirname(__file__),'room1_walls_test.tmx')
tmx_data = load_pygame(path)
obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

radius = 50
cover_surf = pygame.Surface((radius*2, radius*2))
cover_surf.fill(0)
cover_surf.set_colorkey((255, 255, 255))
pygame.draw.circle(cover_surf, (255, 255, 255), (radius, radius), radius)

pygame.display.set_caption("Room 1")

#Path to Assets
asset_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
imgs = [] 
paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
sprites = []
for path in paths: 
    sprite_path = os.path.join(asset_path, path)
    sprites.append(sprite_path)
# Player setup
player = Player(100, 300, sprites)  # Width and height set to 40 pixels

#Create sprite group and add player to it 
all_sprites = pygame.sprite.Group() 
all_sprites.add(player)

clock = pygame.time.Clock()

running = True 
while running: 
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False 

    #all_sprites.update()
    player.move(pygame.key.get_pressed(), obstacles)

    canvas.fill((80, 80, 80))
    map.draw_map(canvas)
    
    # Draw sprites on top of the map
    all_sprites.draw(canvas)

   
    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    pygame.display.update()



pygame.quit()

#Code for HARD MODE
#if keys[K_DOWN] or keys[K_s]:
    #self.index=0
    #if not any(self.rect.colliderect(obstacle) for obstacle in obstacles):
        #self.rect.y += 5
    #else:
        #self.rect.y += 0