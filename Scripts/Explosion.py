import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,size):
        super().__init__()
        # Load explosion image
        self.images = []
        for num in range(1,9): # assuming 8 frames named exp1.png to exp8.png makes 3 sizes
            img = pygame.image.load(f"Assets/exp{num}.png").convert_alpha()
            if size == 1:
                img = pygame.transform.scale(img, (30, 30))
            if size == 2:
                img = pygame.transform.scale(img, (60, 60))
            if size == 3:
                img = pygame.transform.scale(img, (180, 180))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self): # update method for animation
        explosionSpeed = 3
        self.counter += 1        
        if self.counter >= explosionSpeed and self.index < len(self.images)-1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]            
        if self.index >= len(self.images)-1 and self.counter >= explosionSpeed: # kill after animation
            self.kill()