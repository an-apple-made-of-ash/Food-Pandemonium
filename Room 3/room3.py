import pygame
import pytmx
import random
import os
<<<<<<< Updated upstream
import itertools
import threading
=======
import openai
import time
import tiktoken 
import threading
import itertools

# Set your company's ChatGPT API key and URL here
company_api_key = "981bdca6dae44b78a930541b4577f696"
company_api_url = "https://dso-ie-openai.openai.azure.com/"

# Ensure the company's ChatGPT API key is used directly
openai.api_key = company_api_key

def insult(model):
    insults = []
    prompt = "Pretend you are an annoyed resident. Give me one very rude sentence expressing annoyance towards the delivery man for being slow. Give me a new novel response each time"

    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_base = "https://dso-ie-openai.openai.azure.com/"
    openai.api_key = "981bdca6dae44b78a930541b4577f696"

    if model == 'gpt-4':
        azure_oai_model = "dsogpt4" 
    else:
        azure_oai_model = "dsochatgpt35"

    response = openai.ChatCompletion.create(
        engine=azure_oai_model,
        temperature=0,
        max_tokens=256,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": prompt}
        ]
    )

    text = str(response.choices[0].message.content)
    print(text)
    #insults.append(text)


>>>>>>> Stashed changes

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_paths):
        self.img = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img,(30,30)) for img in self.img]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.gravity = 9.81
        self.speed = 2
        self.jump_power = 33
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
        super().__init__()
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
            if new_position.y + new_position.height >= 1160:
                new_position.y = 41

        # Collision detection
        if not any(new_position.colliderect(obstacle) for obstacle in obstacles):
            self.rect.topleft = new_position.topleft

    def collide(self,player): 
        if self.rect.colliderect(player.rect):
            print("Collision detected")
            self.kill()

    #def update(self, obstacles, player):
        #self.move(obstacles)
        #self.collide(player)

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

class NPC(pygame.sprite.Sprite):
    def __init__(self,img_list, insult_func):
        super(NPC, self).__init__()
        original_image = pygame.image.load(random.choice(img_list))
        self.image = pygame.transform.scale(original_image, (120, 180))
        self.rect = self.image.get_rect()
        screen_width = 800
        screen_height = 600

        corner = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])

        if corner == "top_left":
            self.rect.topleft = (0, 0)
        elif corner == "top_right":
            self.rect.topright = (screen_width-130, 0)
        elif corner == "bottom_left":
            self.rect.bottomleft = (0, screen_height)
        elif corner == "bottom_right":
            self.rect.bottomright = (screen_width-130, screen_height)

        # Load speech bubble image
        self.speech_bubble = pygame.image.load("Assets/SpeechBubble.png")
        self.speech_bubble = pygame.transform.scale(self.speech_bubble, (150, 100))
        self.speech_bubble_rect = self.speech_bubble.get_rect()

        # Text to be displayed in the speech bubble
        self.text = insult_func()

        # Set the position of the speech bubble based on the corner
        self.set_speech_bubble_position(corner)


    def set_speech_bubble_position(self, corner):
        screen_width = 800
        screen_height = 600
        if corner == "top_left":
            self.speech_bubble_rect.midbottom = (160, 100)
        elif corner == "top_right":
            self.speech_bubble_rect.midbottom = (screen_width-88, 95)
        elif corner == "bottom_left":
            self.speech_bubble_rect.midtop = (160, screen_height-180)
        elif corner == "bottom_right":
            self.speech_bubble_rect.midtop = (screen_width-88, screen_height-180)

    def show_speech_bubble(self, screen):
        # Render speech bubble
        screen.blit(self.speech_bubble, self.speech_bubble_rect)

        # Render text
        font = pygame.font.SysFont("comicsansms", 14)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.speech_bubble_rect.center
        screen.blit(text_surface, text_rect)


class Advertisement(pygame.sprite.Sprite):
    def __init__(self, ad_image_paths):
        super(Advertisement, self).__init__()
        self.image_paths = ad_image_paths
        self.image_index = itertools.cycle(range(len(ad_image_paths)))
        self.image = pygame.image.load(ad_image_paths[next(self.image_index)])
        self.rect = self.image.get_rect()
        self.visible = False
        self.display_start_time = 0

    def show(self, screen, current_time):
        if self.visible:
            screen.blit(self.image, self.rect)
            if current_time - self.display_start_time >= 2000:
                self.visible = False

    def update(self, current_time):
        if current_time - self.display_start_time >= 7000:
            self.visible = True
            self.display_start_time = current_time
            self.image = pygame.image.load(self.image_paths[next(self.image_index)])



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
<<<<<<< Updated upstream
class Advertisement(pygame.sprite.Sprite):
    def __init__(self, ad_image_paths):
        super(Advertisement, self).__init__()
        self.image_paths = ad_image_paths
        self.image_index = itertools.cycle(range(len(ad_image_paths)))
        self.image = pygame.image.load(ad_image_paths[next(self.image_index)])
        self.rect = self.image.get_rect()
        self.visible = False
        self.display_start_time = 0

    def show(self, screen, current_time):
        if self.visible:
            screen.blit(self.image, self.rect)
            pygame.time.delay(1500)
            if current_time - self.display_start_time >= 3000:
                self.visible = False


    def update(self, current_time):
        if current_time - self.display_start_time >= 10000:
            self.visible = True
            self.display_start_time = current_time
            self.image = pygame.image.load(self.image_paths[next(self.image_index)])

def update_ads(ads):
    while True:
        current_time = pygame.time.get_ticks()
        ads.update(current_time)
        pygame.time.delay(100)  # Adjust delay as needed


=======
# ...
# ...
>>>>>>> Stashed changes
def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    # Load background image
    background_image_path = os.path.join(os.path.dirname(__file__), "/Users/felicia/Documents/GitHub/hmmmmm/Assets/PaneBG.png")
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    path = os.path.join(os.path.dirname(__file__), 'Rm3Mappls.tmx')
    tmx_data = load_pygame(path)
    obstacles = get_collision_objects(tmx_data, "Tile Layer 1")
    spawn_time = pygame.time.get_ticks()
    npc_visible = False

    # Path to Assets
    asset_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
    imgs = ["Boy.png", "Man.png", "ManCap.png", "Woman.png"]
    paths = ["Delivery-Front.png", "Delivery-Back.png", "Delivery-Left.png", "Delivery-Right.png"]
<<<<<<< Updated upstream
    ads = ["Ad4.png","Ad2.png","Ad3.png"]
=======
>>>>>>> Stashed changes
    sprites = []
    ad_paths = []
    npc_sprites = []
    for path in paths:
        sprite_path = os.path.join(asset_path, path)
        sprites.append(sprite_path)

    for path in imgs:
        img_path = os.path.join(asset_path, path)
        npc_sprites.append(img_path)

<<<<<<< Updated upstream
    for path in ads:
        img_path = os.path.join(asset_path, path)
        ad_paths.append(img_path)

    ads = Advertisement(ad_paths)

=======
>>>>>>> Stashed changes
    # Player setup
    player = Player(100, 100, sprites)  # Width and height set to 40 pixels

    # Thieves setup
    thieves = []
    thief_path = os.path.join(asset_path, "Thief.png")
    thief1 = Thief(thief_path, (200, 200))
    thief2 = Thief(thief_path, (800, 560))
    thief3 = Thief(thief_path, (900, 700))
    thief4 = Thief(thief_path, (900, 700))
    thief5 = Thief(thief_path, (600, 600))
    thief6 = Thief(thief_path, (700, 400))
    thieves.extend([thief1, thief2, thief3, thief4, thief5, thief6])

    camera = Camera(screen_width, screen_height, tmx_data.width * tmx_data.tilewidth,
                    tmx_data.height * tmx_data.tileheight)
    npc_group = pygame.sprite.Group()

<<<<<<< Updated upstream
    # Advertisement
=======
    ad_paths = ["Ad1.png", "Ad2.png", "Ad3.png"]
    ads = Advertisement(ad_paths)

>>>>>>> Stashed changes
    advertisement_thread = threading.Thread(target=update_ads, args=(ads,))
    advertisement_thread.daemon = True
    advertisement_thread.start()

    running = True
    clock = pygame.time.Clock()

    # Adjust the frame rate here (e.g., 30 frames per second)
    target_fps = 30

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        player.move(keys, obstacles)
        camera.update(player)

        # Draw the background image
        screen.blit(background_image, (0, 0))

        draw_map(screen, tmx_data, camera)

        # Move and draw thieves
        for thief in thieves:
            thief.move(obstacles)
            screen.blit(thief.image, camera.apply(thief.rect))
            if thief.rect.colliderect(player.rect):
                print("collision")
                thieves.remove(thief)

        if len(thieves) == 0:
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render('Ok. So Dash got this round...', True, (0, 200, 0))
            text_rect = text.get_rect()
            text_rect.center = (400, 300)
            screen.fill((255, 255, 255))
            player.new_position = (800, 600)
            screen.blit(text, text_rect)

        ads.show(screen, current_time)  # Display advertisements

        npc_group.draw(screen)  # Draw NPCs after other elements
        screen.blit(player.image, camera.apply(player.rect))

        for npc in npc_group:
            npc.show_speech_bubble(screen)

        pygame.display.update()

        # Limit the frame rate
        clock.tick(target_fps)

    pygame.quit()

if __name__ == '__main__':
    main()
