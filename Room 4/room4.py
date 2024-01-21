import os
import pygame
from pygame.locals import *
from tiles import *
from collide import *
import subprocess
import sys

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
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_position.x -= self.speed
            self.index = 3
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_position.x += self.speed
            self.index = 2

        self.image = self.images[self.index]

        # Check for collisions 
        # Check for collisions with "Teleport" layer
        teleport_collisions = [obstacle for obstacle in obstacles if obstacle.layer_name == "Teleport"]
        if not any(new_position.colliderect(obstacle) for obstacle in teleport_collisions):
            self.rect.topleft = new_position.topleft
        else:
            pygame.quit()
            script_path = "teleport.py"
            subprocess.run(['python3', script_path])
            running = False 
        

        

pygame.init() 

map = TileMap('teleportationRoom_Border.csv', "Dark Brick1.png")
screen = pygame.display.set_mode([800,600])
canvas = pygame.Surface([800,1200])
path = os.path.join(os.path.dirname(__file__),'teleportationRoom.tmx')
tmx_data = load_pygame(path)
obstacles = get_collision_objects(tmx_data, "Border")
portals = get_collision_objects(tmx_data,"Teleport")

pygame.display.set_caption("Room 4")

#Path to Assets
asset_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
imgs = [] 
paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
sprites = []
for path in paths: 
    sprite_path = os.path.join(asset_path, path)
    sprites.append(sprite_path)
# Player setup
player = Player(100, 100, sprites)  # Width and height set to 40 pixels

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