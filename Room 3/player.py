import pygame
from spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction = .35, -.12
        self.image = Spritesheet('spritesheet.png').parse_sprite('chick.png')
        self.rect = self.image.get_rect()
        self.position, self.velocity = pygame.math.Vector2(0,0), pygame.math.Vector2(0,0)
        self.acceleration = pygame.math.Vector2(0,self.gravity)

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles)

    def horizontal_movement(self,dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= .3
        elif self.RIGHT_KEY:
            self.acceleration.x += .3
        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self,dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)
        return hits

    def checkCollisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:  # Hit tile moving right
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # Hit tile moving left
                self.position.x = tile.rect.right
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:  # Hit tile from the top
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:  # Hit tile from the bottom
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y

# Inside your player.py module:

class Deliveryman(Player):
    def __init__(self):
        super().__init__()
        # Add any additional attributes specific to the Deliveryman class

    def catch_thief(self, thief):
        if self.rect.colliderect(thief.rect):
            self.thieves_captured += 1
            thief.disappear()

    def update(self, dt, tiles):
        super().update(dt, tiles)
        # Add any additional update logic for the Deliveryman class, if needed


class Thief(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('thief_spritesheet.png').parse_sprite('thief.png')  # Adjust filenames as needed
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        # Add any additional attributes for the Thief class

    def random_spawn(self, tiles):
        # Implement logic to randomly spawn the thief on valid tiles
        pass

    def disappear(self):
        # Implement logic to make the thief disappear when caught
        pass

    def update(self, dt):
        # Add any update logic for the Thief class
        pass

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


# Inside your player.py module:

class Thief(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('thief_spritesheet.png').parse_sprite('thief.png')  # Adjust filenames as needed
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.is_spawned = False
        self.speed = 2  # Adjust the speed as needed

    def random_spawn(self, tiles):
        if not self.is_spawned:
            valid_spawn_tiles = [tile for tile in tiles if tile.is_walkable()]
            if valid_spawn_tiles:
                spawn_tile = random.choice(valid_spawn_tiles)
                self.position.x = spawn_tile.rect.x
                self.position.y = spawn_tile.rect.y
                self.rect.topleft = self.position
                self.is_spawned = True

    def disappear(self):
        self.is_spawned = False
        # Implement any additional logic needed when the thief disappears

    def update(self, dt):
        if self.is_spawned:
            # Example: Move the thief horizontally (you can modify this based on your game's logic)
            self.position.x += self.speed * dt
            self.rect.topleft = self.position

            # Implement any additional logic for the thief's behavior, animation, etc.
            # Example: Change direction when reaching the screen boundary
            if self.position.x < 0 or self.position.x > SCREEN_WIDTH:
                self.speed *= -1  # Reverse the direction

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))



