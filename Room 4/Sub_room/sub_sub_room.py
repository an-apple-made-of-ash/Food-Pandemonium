import os
import pygame
from pygame.locals import *
import subprocess
import sys

import pygame, csv, os 

class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        image_path = os.path.join(os.path.dirname(__file__), image_path)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, tile_img): 
        self.tile_size = 20
        self.start_x, self.start_y = 0,0
        self.tiles = self.load_tiles(filename, tile_img)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0,0,0))
        self.load_map()

    def draw_map(self,surface):
        surface.blit(self.map_surface, (0,0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(os.path.dirname(__file__),(filename))) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map
    
    def load_tiles(self, filename, tile_img):
        tiles = []
        map = self.read_csv(filename) 
        x, y = 0,0
        for row in map: 
            x=0
            for tile in row: 
                if tile == "-1": #Blank
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == "0":
                    tiles.append(Tile(tile_img, x * self.tile_size, y*self.tile_size))
                
                x+=1

            y+=1
        
        self.map_w, self.map_h = x*self.tile_size, y*self.tile_size
        return tiles
    
import pygame
import pytmx
import os

def load_pygame(filename):
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    return tmx_data

def draw_map(surface, tmx_data, tileset):
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

def get_collision_objects(tmx_data, layer_name):
    obstacles = []
    layer = tmx_data.get_layer_by_name(layer_name)
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles


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
        else:
            pygame.quit()
            subprocess.run(['python', 'Room 4\\teleport.py']) 