import pygame
import random

# Define grid size
rows = 4
cols = 7

class Aliens(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        # Load image
        self.image = pygame.image.load("Assets/alien" + str(random.randint(1,6)) + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = 1  # 1 for right, -1 for left
        
    def update(self): # update method with movement
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
    
def create_aliens(alienGroup): #  Create a grid of aliens
        for row in range(rows):
            for col in range(cols):
                alien = Aliens(100 + col * 100, 100 + row * 70)
                alienGroup.add(alien)
