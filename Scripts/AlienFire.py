import pygame
import random
from Explosion import Explosion
from pygame import mixer

alienCooldown = 1000  # milliseconds
lastAlienShot = pygame.time.get_ticks()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
playerDamage=pygame.mixer.Sound("Assets/playerDamage.mp3")
playerDamage.set_volume(0.5)


class AlienFire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Correct image load
        self.image = pygame.image.load("Assets/greengoo.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (25, 25))    
        self.rect = self.image.get_rect(center=(x, y))

    def update(self,screenHeight,spaceshipGroup, spaceship,explosionGroup): # update method with collision detection
        self.rect.y += 1  # move upward
        if self.rect.top > screenHeight:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceshipGroup, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.healthRemaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery,1)
            explosionGroup.add(explosion)
            playerDamage.play()
        
            
    def shoot(alienGroup, alienFireGroup): # alien shooting method
        global lastAlienShot
        alienCooldown = 1000
        timeNow = pygame.time.get_ticks()

        if timeNow - lastAlienShot > alienCooldown and len(alienFireGroup) < 5 and len(alienGroup) > 0: # limit to 5 shots on screen
            attackingAlien = random.choice(alienGroup.sprites()) # choose random alien to shoot
            alienFire = AlienFire(attackingAlien.rect.centerx, attackingAlien.rect.bottom) # shoot from bottom center of alien
            alienFireGroup.add(alienFire)
            lastAlienShot = timeNow # update last shot time