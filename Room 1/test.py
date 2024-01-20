import os
import pygame
from pygame.locals import *
from tiles import *
from collide import *

#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position):
        super(Player,self).__init__()
        self.images = [pygame.image.load(path) for path in image_paths]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

    def update(self): 
        new_pos = self.rect.copy()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.index=2
            self.rect.x -= 1

        if keys[K_RIGHT] or keys[K_d]:
            self.index=3
            self.rect.x += 1

        if keys[K_UP] or keys[K_w]:
            self.index=1
            self.rect.y -= 1

        if keys[K_DOWN] or keys[K_s]:
            self.index=0
            self.rect.y += 1

        self.image = self.images[self.index]


pygame.init() 

map = TileMap('room1_walls_test.tmx')
screen = pygame.display.set_mode([800,600])
canvas = pygame.Surface([800,1200])
path = os.path.join(os.path.dirname(__file__),'room1_walls_test.tmx')
tmx_data = load_pygame(path)
obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

pygame.display.set_caption("Room 1")

#For Sprites 
assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
sprites = []
for path in paths: 
    sprite_path = os.path.join(assets_path, path)
    sprites.append(sprite_path)

player = Player(sprites,(50,50))

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

    all_sprites.update()

    canvas.fill((80, 80, 80))
    map.draw_map(canvas)
    
    # Draw sprites on top of the map
    all_sprites.draw(canvas)

    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    pygame.display.update()

    #Rain -> Either increase framerate or increase change in movement 
    #Strong Winds -> Constantly Push back 



pygame.quit()