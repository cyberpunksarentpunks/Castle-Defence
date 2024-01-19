import sys
#from class_character import *
#from pygame import locals

# The game playing screen should have a gate's health indicator, a current wave/round that is coming
# 
import pygame
from pygame import locals
import math
from math import sqrt, pow

class Menu:
    def __init__(self, screen, button_x, button_y, button_width, button_height, button_color, text, text_color, action):
        self.screen = screen
        self.button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        self.button_color = button_color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self):
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def check_click(self, pos):
        if self.button_rect.collidepoint(pos):
            self.action()
            


# Defining the image and starting position of a character.
# Then for enemy and allies is x,y_change to set their moving direction.
# Creating their stats for health, damage, what a player will get if they shot them and cost of allies to summon.
# The state of character mode which they currently are in.(Moving, attacking, death or just standing for a player).
#### Characters should change their animations depending on their character state !
class Character:
    
    def __init__(self, image, x_cor, y_cor, x_change, y_change, health, damage, reward, cost, state):
        self.img = image
        self.x = x_cor
        self.y = y_cor
        self.x_change = x_change
        self.y_change = y_change
        self.hp = health
        self.dmg = damage
        self.reward = reward
        self.cost = cost
        self.state = state
        
    
    # draws the character image on specified position into screen
    # Maybe the use for making an individual pngs into animations should be here. I don't know.
    def draw_character(self):
        screen.blit(self.img, (self.x, self.y))

    
    def move(self, direction):
        if direction == 'left':
            self.x -= self.x_change
        elif direction == 'right':
            self.x += self.x_change
        elif direction == 'up':
            self.y -= self.y_change
        elif direction == 'down':
            self.y += self.y_change
    
    # player controls
    def handle_controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move('left')
        if keys[pygame.K_RIGHT]:
            self.move('right')
        if keys[pygame.K_UP]:
            self.move('up')
        if keys[pygame.K_DOWN]:
            self.move('down')
        
    
    # collision detection between character and any given object 
    def is_collision(self, characterX,characterY, objectX, objectY, target_distance):
        distance = math.sqrt(math.pow(characterX - objectX,2) + (math.pow(characterY - objectY, 2)))
        if distance < target_distance:
            return True
        else:
            return False
    
     
    # summoning ally will happen if a player has enough funds.
    # ! note- if he hasn't, there will be summoners icons somewhere on the top and the icons will be faded
    # 
    def summon_ally(self):
        pass


# Class for creating the Vault    
class Vault:
    
    def __init__(self, image, posX, posY, health):
        self.img = image
        self.x = posX
        self.y = posY
        self.hp = health
    
    # draw the vault into the screen    
    def draw_vault(self):
        screen.blit(self.img, (self.x, self.y))
        
# used on a button in menu to quit the game        
def quit_game():
    pygame.quit()
    sys.exit()

# MENU LOOP    
def main_menu():
    menu_buttons = [
        Menu(screen, 100, 200, 200, 50, (0, 255, 0), "Play", (0, 0, 0), game_loop),
        Menu(screen, 100, 300, 200, 50, (255, 0, 0), "Quit", (0, 0, 0), quit_game)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in menu_buttons:
                        button.check_click(pygame.mouse.get_pos())

        screen.fill((255, 255, 255))
        for button in menu_buttons:
            button.draw()

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 840, 460
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Menu")        

# initialize the pygame
pygame.init()

# creating the screen and size of it
WIDTH = 840
HEIGHT = 460
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Loading characters/objects images and resizing them
player_image_origin = pygame.image.load('img/test_npc.png')
vault_image_origin = pygame.image.load('img/test_gate.png')
enemy_image_origin = pygame.image.load('img/test_npc2.png')

resized_vault = pygame.transform.scale(vault_image_origin, (200, 200))
resized_player = pygame.transform.scale(player_image_origin, (70, 70))
resized_npc = pygame.transform.scale(enemy_image_origin, (70, 70))

# character creations
player = Character(image=resized_player, x_cor=150, y_cor=180, x_change=1, y_change=1, health=None, damage=2,reward=None, cost=None, state="still")
enemy = Character(image=resized_npc, x_cor=700, y_cor=380, x_change=0, y_change=0, health=3, damage=5, reward=10, cost=None, state="still")

# objects creations
vault = Vault(image=resized_vault, posX=0, posY=250, health=100)

# Game loop - is played after pressing the play button in the menu
def game_loop():
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player controls
        player.handle_controls()
        
        # Clear the screen
        screen.fill((255, 255, 255))
        
        # Draw the player character and whole scene
        player.draw_character()
        vault.draw_vault()
        enemy.draw_character()
        
        
        # Update the display
        pygame.display.flip()

    pygame.quit()


main_menu()
game_loop()
