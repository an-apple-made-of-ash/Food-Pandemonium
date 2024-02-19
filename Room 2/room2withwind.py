import os
import pygame
from pygame.locals import *
from tiles import *
from collide import *
import random
import pytmx
import random
import os
import openai
import time
import tiktoken 
import threading
import itertools

# Set your company's ChatGPT API key and URL here
company_api_key = 
company_api_url = 

# Ensure the company's ChatGPT API key is used directly
openai.api_key = company_api_key

def insult(model):
    insults = []
    prompt = "Pretend you are an annoyed resident. Give me one very rude sentence expressing annoyance towards the delivery man for being slow. Give me a new novel response each time"

    openai.api_type = 
    openai.api_version = 
    openai.api_base = 
    openai.api_key = 

    if model == 'gpt-4':
        azure_oai_model = 
    else:
        azure_oai_model = 

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


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position):
        super().__init__()
        self.imag = [pygame.image.load(path) for path in image_paths]
        self.images = [pygame.transform.scale(img, (38, 38)) for img in self.imag]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 2

    def move(self, obstacles):
        new_position = self.rect.copy()
        keys = pygame.key.get_pressed()
        # Horizontal Movement
        if keys[K_a] or keys[K_LEFT]:
            if westW == False:
                new_position.x -= self.speed
                self.index = 2
            else:
                self.index = 2
        if keys[K_d] or keys[K_RIGHT]:
            if eastW == False:
                new_position.x += self.speed
                self.index = 3
            else:
                self.index = 3
        if keys[K_w] or keys[K_UP]:
            if northW == False:
                new_position.y -= self.speed
                self.index = 1
            else:
                self.index = 1
        if keys[K_s] or keys[K_DOWN]:
            if southW == False: 
                new_position.y += self.speed
                self.index = 0
            else:
                self.index = 0
        self.image = self.images[self.index]

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

# Wind Class
class Wind(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_position, direction):
        super().__init__()
        # Select a random path from the list
        image_path = random.choice(image_paths)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        self.speed = 5
        self.direction = direction
    def update(self):
        if self.direction == "North":
            self.rect.y -= self.speed
        elif self.direction == "South":
            self.rect.y += self.speed
        elif self.direction == "West":
            self.rect.x -= self.speed
        elif self.direction == "East":
            self.rect.x += self.speed
            
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
        self.text = ["So slow","Im going to be old.","0/5 speed", "bad service"]

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
        index = random.randint(0,len(self.text)-1)
        print(self.text[index])
        text_surface = font.render(self.text[index], True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.speech_bubble_rect.center
        screen.blit(text_surface, text_rect)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.appear_time > self.display_time:
            self.kill()

pygame.init()



width = 800
height = 600
screen = pygame.display.set_mode([width, height])
path = os.path.join(os.path.dirname(__file__), 'Room 2.tmx')
tmx_data = load_pygame(path)
obstacles = get_collision_objects(tmx_data, "Tile Layer 2")

pygame.display.set_caption("Room 2")
assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets")
paths = ["Delivery-Front.png", "Delivery-Back.png", "Delivery-Left.png", "Delivery-Right.png"]
sprites = [os.path.join(assets_path, path) for path in paths]
imgs = ["Boy.png", "Man.png", "ManCap.png", "Woman.png"]
npc_sprites = []
for path in imgs:
        img_path = os.path.join(assets_path, path)
        npc_sprites.append(img_path)

player = Player(sprites, (60, 525))
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
camera = Camera(width, height, tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight)

clock = pygame.time.Clock()
move = True
running = True
last_weather_change = 0
delay_between_calls = 1000
eastW = False
westW = False
northW = False
southW = False

rain_path = "Assets\Rain Filter.png"
rain_filter = pygame.image.load(rain_path)
npc_group = pygame.sprite.Group()

wind_paths = ["Assets\Wind.png"]

winds = []  # List to hold instances of Wind class
npc_visible = False
while running:
    spawn_time = pygame.time.get_ticks()
    clock.tick(60)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if move:
        player.move(obstacles)
        if current_time - last_weather_change > 5000:  # Change weather every 10 seconds
            weather = random.randint(1, 2)
            eastW = False 
            westW = False
            northW = False 
            southW = False
            player.speed = 1

            if weather == 1:
                wind_direction = random.choice(["North", "South", "East", "West"])
                print(wind_direction + " wind is blowing!")
                if wind_direction == "North":
                    northW = True 
                elif wind_direction == "South":
                    southW = True 
                elif wind_direction == "West":
                    westW = True 
                elif wind_direction == "East": 
                    eastW = True

            elif weather == 2:
                player.speed = 20
                print("It's Raining")

            
            last_weather_change = current_time 
            pygame.time.delay(delay_between_calls) 

    all_sprites.update()
    camera.update(player)

    screen.fill((40, 40, 50))
    draw_map(screen, tmx_data, camera)

    if (player.rect.x + player.rect.width) >= 1560 and (player.rect.y + player.rect.height) >= 560:
        font = pygame.font.Font('freesansbold.ttf', 24)
        text = font.render('Dash may have braved the weather but more awaits him...', True, (0, 200, 0))
        textRect = text.get_rect()
        textRect.center = (400, 300)
        screen.fill((255, 255, 255))

        screen.blit(text, textRect)
        move = False

    if current_time - spawn_time >= 5000:
        if npc_visible == False:
            npc = NPC(npc_sprites, lambda: insult('gpt-4'))
            npc_group.add(npc)
            npc_visible = True
            spawn_time = current_time

    if npc_visible and current_time - spawn_time >= 4800:
        npc.kill()
        npc_visible = False

    npc_group.draw(screen)  # Draw NPCs after other elements
    screen.blit(player.image, camera.apply(player.rect))

    for npc in npc_group:
        npc.show_speech_bubble(screen)

    pygame.display.update()
    
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    pygame.display.flip()
    pygame.display.update()

pygame.quit()