import pygame
import random
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        original_image = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/Woman.png")
        self.image = pygame.transform.scale(original_image, (80, 120))
        self.rect = self.image.get_rect()

        corner = random.choice(["top_left", "top_right", "bottom_left", "bottom_right"])

        if corner == "top_left":
            self.rect.topleft = (0, 0)
        elif corner == "top_right":
            self.rect.topright = (SCREEN_WIDTH-60, 0)
        elif corner == "bottom_left":
            self.rect.bottomleft = (0, SCREEN_HEIGHT)
        elif corner == "bottom_right":
            self.rect.bottomright = (SCREEN_WIDTH-60, SCREEN_HEIGHT)

        # Load speech bubble image
        self.speech_bubble = pygame.image.load("/Users/felicia/Documents/GitHub/hmmmmm/Assets/SpeechBubble.png")
        self.speech_bubble = pygame.transform.scale(self.speech_bubble, (150, 100))
        self.speech_bubble_rect = self.speech_bubble.get_rect()

        # Text to be displayed in the speech bubble
        self.text = "Hello, I'm an NPC!"

        # Set the position of the speech bubble based on the corner
        self.set_speech_bubble_position(corner)

    def set_speech_bubble_position(self, corner):
        if corner == "top_left":
            self.speech_bubble_rect.midbottom = (150, 0)
        elif corner == "top_right":
            self.speech_bubble_rect.midbottom = (SCREEN_WIDTH-210, 0)
        elif corner == "bottom_left":
            self.speech_bubble_rect.midtop = (0, SCREEN_HEIGHT-150)
        elif corner == "bottom_right":
            self.speech_bubble_rect.midtop = (SCREEN_WIDTH-60, SCREEN_HEIGHT)

    def show_speech_bubble(self, screen):
        # Render speech bubble
        screen.blit(self.speech_bubble, self.speech_bubble_rect)

        # Render text
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = self.speech_bubble_rect.center
        screen.blit(text_surface, text_rect)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Your Game Title")

npc_group = pygame.sprite.Group()

clock = pygame.time.Clock()

spawn_time = pygame.time.get_ticks()
npc_visible = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()

    if current_time - spawn_time >= 5000:
        if not npc_visible:
            npc = NPC()
            npc_group.add(npc)
            npc_visible = True
            spawn_time = current_time

    if npc_visible and current_time - spawn_time >= 2000:
        npc.kill()
        npc_visible = False

    screen.fill((255, 255, 255))
    npc_group.draw(screen)

    # Show speech bubble for each visible NPC
    for npc in npc_group:
        npc.show_speech_bubble(screen)

    pygame.display.flip()
    clock.tick(60)
