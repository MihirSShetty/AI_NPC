# Import the pygame module
import pygame

import pygame_gui
import sys

from model import *

import time

import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_TAB
)

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

TEXT_COLOR = (50, 50, 50)  # Dark grey for output box
BOX_COLOR = (139, 69, 19)  # White text

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player.png").convert()

        new_width = 100  # Desired width
        new_height = 150  # Desired height
        self.surf = pygame.transform.scale(self.surf, (new_width, new_height))

        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

   # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#AI npc class
class Leah(pygame.sprite.Sprite):
    def __init__(self):
        super(Leah, self).__init__()
        self.surf = pygame.image.load("images/leah_body.png").convert()

        self.name = "Leah"

        new_width = 50  # Desired width
        new_height = 100  # Desired height
        self.surf = pygame.transform.scale(self.surf, (new_width, new_height))

        self.surf.set_colorkey((255,255,255), RLEACCEL)
 
        self.rect = self.surf.get_rect(center = (800, 400))
        self.speed = 50

        self.rect = self.surf.get_rect(center=(800, 400))
        self.speed = 1

        self.starting_position = (800, 400)  # Leah's starting position
        self.well_position = (800, 200)  # Target well position
        self.is_leading = False  # Whether Leah is currently moving
        self.moving_up = True  # Direction of movement (up/down)

    def lead(self):
        """Starts or continues Leah's movement to the well and back."""
        if not self.is_leading:
            # Begin the movement if not already moving
            self.is_leading = True
            self.moving_up = True  # Start by moving up

        # Perform the movement if Leah is leading
        if self.is_leading:
            if self.moving_up:
                # Move up toward the well
                if self.rect.top > self.well_position[1]:
                    self.rect.move_ip(0, -self.speed)
                else:
                    # Reached the well, start moving down
                    self.moving_up = False
            else:
                # Move down back to the starting position
                if self.rect.top < self.starting_position[1]:
                    self.rect.move_ip(0, self.speed)
                else:
                    # Reached the starting position, stop leading
                    self.is_leading = False
                    print("Leah has returned to the starting position.")

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def talk(self, player):
        # Define thresholds for proximity
        horizontal_threshold = 50  # Adjust as needed
        vertical_threshold = 50    # Allow some vertical leeway

        # Check horizontal and vertical alignment
        if abs(player.rect.right - self.rect.left) < horizontal_threshold and \
        abs(player.rect.centery - self.rect.centery) < vertical_threshold:
            print("Talking started with player")
            get_input(self.name)
        else:
            print("Too far")

class John(pygame.sprite.Sprite):
    def __init__(self):
        super(John, self).__init__()
        self.surf = pygame.image.load("images/john_body.png").convert()

        self.name = "John"

        new_width = 50  # Desired width
        new_height = 100  # Desired height
        self.surf = pygame.transform.scale(self.surf, (new_width, new_height))

        self.surf.set_colorkey((255,255,255), RLEACCEL)
 
        self.rect = self.surf.get_rect(center = (200, 400))
        self.speed = 1

        self.going_right = True

    def talk_to_others(self):
        memory_list = dict_mem_list[self.name]
        for gossip in gossip_list:
            memory_list.append({"role": "user", "content": gossip})

    # Move the sprite based on speed
    def walk(self):
        if self.going_right and self.rect.right < 600:
            self.rect.move_ip(self.speed, 0)

        # Reached the right boundary
        elif self.going_right and self.rect.right >= 600:
            print("Talking to Leah")
            self.talk_to_others()
            self.going_right = False  # Switch direction to left

        # Moving left
        elif not self.going_right and self.rect.left > 200:
            self.rect.move_ip(-self.speed, 0)

        # Reached the left boundary
        elif not self.going_right and self.rect.left <= 200:
            self.going_right = True  # Switch direction to right
    
    # Remove the sprite when it passes the left edge of the screen
    def talk(self, player):
        # Define thresholds for proximity
        horizontal_threshold = 50  # Adjust as needed
        vertical_threshold = 50    # Allow some vertical leeway

        # Check horizontal and vertical alignment
        if abs(player.rect.right - self.rect.left) < horizontal_threshold and \
        abs(player.rect.centery - self.rect.centery) < vertical_threshold:
            print("Talking started with player")
            get_input(self.name)
        else:
            print("Too far")
        

pygame.init()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#create a custom even
TALK = pygame.USEREVENT + 1

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

# text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=manager,
#                                                object_id='#main_text_entry')

# Create a text input box at the bottom of the screen
input_rect = pygame.Rect(150, SCREEN_HEIGHT - 80, SCREEN_WIDTH - 200, 100)  # Positioned near the bottom
text_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=input_rect,
    manager=manager,
    object_id='#main_text_entry'
)

#clock for controlling speed
clock = pygame.time.Clock()

#for bid dialogues to prevent running off
def wrap_text(text, font, max_width):
    """
    Splits text into multiple lines that fit within max_width.
    """
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # Add the last line
    return lines

def show_output(output, char_image):
    print("show output called")

    output_rect = pygame.Rect(150, SCREEN_HEIGHT - 200, SCREEN_WIDTH - 150, 200)
    image_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, 150, 200)  # Space for the image

    font = pygame.font.SysFont(None, 24)
    max_width = output_rect.width - 20  # Add padding for the text
    lines = wrap_text(output, font, max_width)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_TAB:
                    return main_loop()

        pygame.draw.rect(screen, BOX_COLOR, output_rect)  # Output box background
        pygame.draw.rect(screen, TEXT_COLOR, output_rect, 2)  # Output box border

        # Render and display text line by line
        y_offset = output_rect.y + 10
        for line in lines:
            rendered_text = font.render(line, True, "black")
            screen.blit(rendered_text, (output_rect.x + 10, y_offset))
            y_offset += font.get_height() + 5  # Adjust for line spacing

        leah_image = pygame.image.load(char_image).convert()
        screen.blit(leah_image, (image_rect.x, image_rect.y))

        pygame.display.update()
        clock.tick(60)

def get_input(npc_name):
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                event.ui_object_id == '#main_text_entry'):
                leah_response, emotion, lead = on_submit(event.text, npc_name)

                if lead:
                    leah.is_leading = True
                    return main_loop()

                print(leah_response)
                print(emotion)

                show_output(leah_response, emotion)
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return main_loop()
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)

        manager.draw_ui(screen)

        pygame.display.update()

player = Player()
leah = Leah()
john = John()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(leah)
all_sprites.add(john)

### Image of Well
well_img = pygame.image.load("images/well.jpg").convert()
well_img = pygame.transform.scale(well_img, (200, 250))
well_img.set_colorkey((255,255,255), RLEACCEL)
well_rect = well_img.get_rect(center = (500, 200))

def main_loop():
    # Variable to keep the main loop running
    running = True

    # Main loop
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                #logic for what to when start talking
                if event.key == K_TAB:
                    leah.talk(player)
                    john.talk(player)
                    
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        john.walk()

        if leah.is_leading:
            leah.lead()

    # Fill the screen with black

        screen.fill((60, 179, 113))

        # Draw the player on the screen
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        screen.blit(well_img, well_rect)

        # Update the display
        pygame.display.flip()

        # ensures fps at constant rate and slowed
        clock.tick(30)

main_loop()
