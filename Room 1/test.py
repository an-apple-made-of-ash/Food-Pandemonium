import pygame
import pytmx

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
    layer = tmx_data.get_layer_by_name('Tile Layer 1')
    for x, y, tile in layer.tiles():
        if tile:  # If the tile is not empty
            obstacles.append(pygame.Rect(x * tmx_data.tilewidth, y * tmx_data.tileheight,
                                         tmx_data.tilewidth, tmx_data.tileheight))
    return obstacles

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    tmx_data = load_pygame('/Users/joonh/Desktop/hmmmmm/Room 1/room1_walls_test.tmx')
    obstacles = get_collision_objects(tmx_data, 'Tile Layer 1')

    # Player setup
    player = pygame.Rect(100, 300, 32, 32)  # Example player rect
    speed = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            player = new_position

        screen.fill((0, 0, 0))  # Clear screen
        draw_map(screen, tmx_data)  
        pygame.draw.rect(screen, (255, 0, 0), player)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
