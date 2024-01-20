import pygame
import pytmx

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        original_image = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Delivery-Right.png")
        self.image = pygame.transform.scale(original_image, (width, height))
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
        if keys[pygame.K_a]:
            new_position.x -= self.speed
        if keys[pygame.K_d]:
            new_position.x += self.speed

        # Check for collisions in the horizontal direction
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

        # Jumping
        if keys[pygame.K_SPACE] and self.jump == 1: 
            self.jump -= 1
            
        

        if any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.jump -= 1
            if self.jump < 0: 
                self.jump = 0
            self.is_jumping = True
            new_position.y -= self.jump_power
            self.is_jumping = False 

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
    tmx_data = load_pygame('/Users/felicia/Documents/GitHub/hmmmmm/Room 3/Rm3Mappls.tmx')
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

    # Player setup
    player = Player(100, 100, 40, 40)  # Width and height set to 40 pixels

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
