import pygame
import pytmx
import subprocess
from random import shuffle
from tiles import *
from collide import *


passwords = {1: 'hyefxt', 2: 'rwvnxz', 3: 'ctwldx', 4: 'lbimco', 5: 'mactuy', 6: 'fydaea'}
order = [1, 2, 3, 4, 5, 6]
shuffle(order)


def pop_message(window, message):
    font = pygame.font.SysFont("comicsansms", 14)
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    window.blit(text_surface, text_rect)


def load_pygame(filename):
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    return tmx_data


def draw_map(surface, tmx_data):
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

    def move(self, keys, border, treasure1, treasure2, treasure3, treasure4, treasure5, treasure6, portal, window):
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
        if not any(new_position.colliderect(obstacle) for obstacle in border):
            self.rect.topleft = new_position.topleft
        
        if any(new_position.colliderect(obstacle) for obstacle in treasure1):
            message = str(order[0]) + ": " + passwords[order[0]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in treasure2):
            message = str(order[1]) + ": " + passwords[order[1]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in treasure3):
            message = str(order[2]) + ": " + passwords[order[2]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in treasure4):
            message = str(order[3]) + ": " +  passwords[order[3]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in treasure5):
            message = str(order[4]) + ": " + passwords[order[4]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in treasure6):
            message = str(order[5]) + ": " + passwords[order[5]]
            pop_message(window, message)
            pygame.time.wait(3000)

        if any(new_position.colliderect(obstacle) for obstacle in portal):
            pygame.quit()
            subprocess.run(['python', 'room4.py'])


map = TileMap('teleportationRoom_Border.csv', "Dark Brick1.png")
screen = pygame.display.set_mode([800,600])
canvas = pygame.Surface([800,1200])
path = os.path.join(os.path.dirname(__file__),'treasure_chest_map.tmx')
tmx_data = load_pygame(path)
border = get_collision_objects(tmx_data, "Border")
portals = get_collision_objects(tmx_data,"Teleport")
treasure1 = get_collision_objects(tmx_data,"Treasure Chest 1")
treasure2 = get_collision_objects(tmx_data,"Treasure Chest 2")
treasure3 = get_collision_objects(tmx_data,"Treasure Chest 3")
treasure4 = get_collision_objects(tmx_data,"Treasure Chest 4")
treasure5 = get_collision_objects(tmx_data,"Treasure Chest 5")
treasure6 = get_collision_objects(tmx_data,"Treasure Chest 6")

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
    player.move(pygame.key.get_pressed(), border, treasure1, treasure2, treasure3, treasure4, treasure5, treasure6, portals, screen)

    canvas.fill((80, 80, 80))
    map.draw_map(canvas)
    
    # Draw sprites on top of the map
    all_sprites.draw(canvas)
    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    pygame.display.update()



pygame.quit()