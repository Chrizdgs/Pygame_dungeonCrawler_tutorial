import pygame
import math
import constants


class Character():
    def __init__(self, x, y, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.action = 0  #0: idle, 1: run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40)  # Character size 40x40
        self.rect.center = (x, y)

    def move(self, dx, dy):
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True

        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        #control diagonal speed
        if dx != 0 and dy != 0:
            dx *= (math.sqrt(2)/2) # approximately 0.7071
            dy *= (math.sqrt(2)/2) # approximately 0.7071

        self.rect.x += dx
        self.rect.y += dy
        
    def update(self):
        #check what action the player is performing
        if self.running == True:
            self.update_action(1) #1: run
        else:
            self.update_action(0) #0: idle

        animation_cooldown = 70
        #handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0:  # Only draw rectangle for player character
            surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))  # Draw character image
        else:    
            surface.blit(flipped_image, self.rect)  # Draw character image
        pygame.draw.rect(surface, constants.RED, self.rect, 1)  # Draw character as a blue rectangles