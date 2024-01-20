import pygame
import pytmx
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image_right = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Delivery-Right.png")
        self.image_left = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Delivery-Left.png")
        self.image = pygame.transform.scale(self.image_right, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.jump_power = 5
        self.gravity = 9.81
        self.is_jumping = False
        self.jump_count = 10

    def move(self, keys, obstacles):
        new_position = self.rect.copy()

        # Horizontal Movement
        if keys[pygame.K_a]:
            new_position.x -= self.speed
            self.image = pygame.transform.scale(self.image_left, (40, 40))
        if keys[pygame.K_d]:
            new_position.x += self.speed
            self.image = pygame.transform.scale(self.image_right, (40, 40))

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

class Thief(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, max_delay):
        super().__init__()
        # Load the image for the thief
        self.image = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Thief.png")
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.max_delay = max_delay
        self.delay_counter = 0
        self.random_direction_counter = 0
        self.random_direction_delay = random.randint(30, 60)  # Delay before changing direction

    def move(self, obstacles, map_width, map_height):
        # If the delay counter is greater than 0, decrease it and return
        if self.delay_counter > 0:
            self.delay_counter -= 1
            return

        # Temporary position to check for collisions
        new_position = self.rect.copy()

        # Randomly change direction after a delay
        self.random_direction_counter += 1
        if self.random_direction_counter >= self.random_direction_delay:
            self.random_direction_counter = 0
            direction = random.choice(['left', 'right', 'up', 'down', 'stay'])
        else:
            # Continue with the current direction
            direction = 'stay'

        if direction == 'left':
            new_position.x -= self.speed
        elif direction == 'right':
            new_position.x += self.speed
        elif direction == 'up':
            new_position.y -= self.speed
        elif direction == 'down':
            new_position.y += self.speed

        # Check for collisions with obstacles
        if any(new_position.colliderect(obstacle) for obstacle in obstacles):
            return  # Do not move if there's a collision with an obstacle

        # Check for collisions with map borders
        if new_position.left < 0:
            new_position.left = 0
        if new_position.right > map_width:
            new_position.right = map_width
        if new_position.top < 0:
            new_position.top = 0
        if new_position.bottom > map_height:
            new_position.bottom = map_height
            self.delay_counter = random.randint(10, self.max_delay)  # Reset delay when hitting the bottom

        # Update the position after checking collisions
        self.rect.topleft = new_position.topleft

        # Set a new delay counter
        self.delay_counter = random.randint(10, self.max_delay)



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

# ...


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
    tmx_data = load_pygame('/Users/felicia/Documents/GitHub/hmmmmm/Room 3/Rm3Mappls.tmx')
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")

    # Player setup
    player = Player(100, 100, 40, 40)  # Width and height set to 40 pixels

    # Thieves setup
    thieves = [Thief(random.randint(0, tmx_data.width * tmx_data.tilewidth),
                    random.randint(0, tmx_data.height * tmx_data.tileheight),
                    20, 20, 2, 60) for _ in range(3)]  # Adjust max_delay as needed

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
            # Add print statements for debugging
            thief.move(obstacles, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)
            screen.blit(thief.image, camera.apply(thief.rect))

        # Draw player on top of thieves
        screen.blit(player.image, camera.apply(player.rect))

        pygame.display.flip()
    pygame.quit()

if __name__ == '__main__':
    main()
