##hi
import pygame
import pytmx
import random
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        self.img = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img,(30,30)) for img in self.img]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_power = 5
        self.gravity = 9.81
        self.speed = 2
        self.jump_power = 30
        self.gravity = 3
        self.jump = 1
        self.is_jumping = False

    def move(self, keys, obstacles):
        new_position = self.rect.copy()

        # Horizontal Movement
        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            new_position.x -= self.speed
            self.index = 2
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            new_position.x += self.speed
            self.index = 3

        self.image = self.images[self.index]

        # Check for collisions in the horizontal direction
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # Jumping
        if keys[pygame.K_SPACE] and self.jump == 1: 
            self.jump -= 1
            if self.jump < 0: 
                self.jump = 0
            self.is_jumping = True
            new_position.y -= self.jump_power
            self.is_jumping = False 

        if not self.is_jumping: 
            new_position.y += self.gravity
        
        if any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.jump = 1

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

class Thief(pygame.sprite.Sprite):
    def __init__(self, image_path, initial_position):
        self.img = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 20
        self.jump_power = 50
        self.gravity = 9.81
        self.is_jumping = False
        self.jump_count = 10

    def move(self, obstacles):
        new_position = self.rect.copy()

        # Horizontal Movement
        check = random.randint(0, 60)
        if check > 30:
            move = random.choice(['stay', 'left', 'right', 'jump'])
        else:
            move = 'stay'

        if move == 'right':
            new_position.x += self.speed
        elif move == 'left':
            new_position.x -= self.speed
        elif move == 'jump':
            self.is_jumping = True

        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # Check if the thief has reached the bottom of the map
        if new_position.y > pygame.display.get_surface().get_height():
            # Respawn at a random point (not a tile ledge)
            respawn_x = random.randint(0, pygame.display.get_surface().get_width())
            respawn_y = 0

            # Adjust the respawn position to avoid obstacles
            while any(pygame.Rect(respawn_x, respawn_y, self.rect.width, self.rect.height).colliderect(obstacle) for obstacle in obstacles):
                respawn_x = random.randint(0, pygame.display.get_surface().get_width())
                respawn_y = 0

            new_position.x = respawn_x
            new_position.y = respawn_y

        if self.is_jumping == True:
            new_position.y -= self.jump_power
            lr = random.randint(1, 2)
            if lr == 1:
                new_position.x += self.speed
            else:
                new_position.x -= self.speed
            self.is_jumping = False

        if not self.is_jumping:
            new_position.y += self.gravity

        # Apply gravity
        if not self.is_jumping:
            new_position.y += self.gravity

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft


class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target_rect):
        return target_rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + self.width // 2
        y = -target.rect.y + self.height // 2

        # Limit camera scroll to map boundaries
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.map_width - self.width), x)  # right
        y = max(-(self.map_height - self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.map_width, self.map_height)

def load_pygame(filename):
    tmx_data = pytmx.util_pygame.load_pygame(filename)
    return tmx_data

def draw_map(surface, tmx_data, camera):
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    surface.blit(tile, camera.apply(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight, tmx_data.tilewidth, tmx_data.tileheight)))

def get_collision_objects(tmx_data, layer_name):
    obstacles = []
    layer = tmx_data.get_layer_by_name("Tile Layer 1")
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles
# ...

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    path = os.path.join(os.path.dirname(__file__), 'Rm3Mappls.tmx')
    tmx_data = load_pygame(path)
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

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

    # Thieves setup
    thieves = []
    thief_path = os.path.join(asset_path, "Thief.png")
    #coords = []
    thief1 = Thief(thief_path, (200,200))
    thief2 = Thief(thief_path, (800,560))
    thief3 = Thief(thief_path, (1346,1000))
    thieves.append(thief1)
    thieves.append(thief2)
    thieves.append(thief3)

    camera = Camera(screen_width, screen_height, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)  # Limit to 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player.move(keys, obstacles)

        camera.update(player)

        screen.fill((0, 0, 0))  # Clear screen
        draw_map(screen, tmx_data, camera)

        # Move and draw thieves
        for thief in thieves:
            thief.move(obstacles)
            screen.blit(thief.image, camera.apply(thief.rect))

        # Draw player on top of thieves
        screen.blit(player.image, camera.apply(player.rect))

        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
