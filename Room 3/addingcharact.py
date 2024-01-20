import pygame
import pytmx
import os 

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_paths): #image_paths should be a list
        super().__init__()
        self.images = [pygame.image.load(path) for path in image_paths]
        self.resized = [pygame.transform.scale(img, (width, height)) for img in self.images]
        self.index = 0
        self.image = self.resized[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.jump_power = 10
        self.gravity = 1
        self.is_jumping = False
        self.jump_count = 10

    def move(self, keys, obstacles):
        new_position = self.rect.copy()

        # Horizontal Movement
        if keys[pygame.K_a] or keys[pygame.K_RIGHT]:
            new_position.x -= self.speed
            self.image = self.resized[2]
        if keys[pygame.K_d] or keys[pygame.K_LEFT]:
            new_position.x += self.speed
            self.image = self.resized[3]
        

        # Check for collisions in the horizontal direction
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # Jumping
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True

        if self.is_jumping:
            new_position.y -= self.jump_power
            self.jump_count -= 1

            if self.jump_count <= 0:
                self.is_jumping = False
                self.jump_count = 10

        # Apply gravity
        if not self.is_jumping:
            new_position.y += self.gravity

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft


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
    layer = tmx_data.get_layer_by_name("Tile Layer 1")
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    path = os.path.join(os.path.dirname(__file__),'Rm3Mappls.tmx')
    tmx_data = load_pygame(path)
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

    # Player setup
    assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
    paths = ["Delivery-Front.png","Delivery-Back.png","Delivery-Left.png","Delivery-Right.png"]
    sprites = []
    for path in paths: 
        sprite_path = os.path.join(assets_path, path)
        sprites.append(sprite_path)
    player = Player(100, 100, 40, 40, sprites)  # Width and height set to 40 pixels

    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(60)  # Limit to 60 frames per second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player.move(keys, obstacles)

        screen.fill((0, 0, 0))  # Clear screen
        draw_map(screen, tmx_data)
        screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
