import pygame
import random
from Explosion import Explosion
from pygame import mixer

# Sound
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
playerDamage = pygame.mixer.Sound("Assets/playerDamage.mp3")
playerDamage.set_volume(0.5)

# Cooldown
bossCooldown = 1500  # milliseconds
lastBossShot = pygame.time.get_ticks()

class BossFire(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Assets/bossAttack.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 30))  # wider attack
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, screenHeight, spaceshipGroup, spaceship, explosionGroup): # update method with collision detection (based on AlienFire)
        self.rect.y += 2 # faster than alien fire
        if self.rect.top > screenHeight:
            self.kill()
        # Collision with player
        if pygame.sprite.spritecollide(self, spaceshipGroup, False, pygame.sprite.collide_mask):
            self.kill()
            spaceship.healthRemaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosionGroup.add(explosion)
            playerDamage.play()

    def shoot(bossGroup, bossFireGroup): # boss shooting method
        global lastBossShot
        timeNow = pygame.time.get_ticks()
        if (timeNow - lastBossShot > bossCooldown 
            and len(bossFireGroup) < 5 
            and len(bossGroup) > 0):
            boss = bossGroup.sprites()[0]  # only one boss
            if boss.is_ready_to_shoot():   # only shoot when in position checking if boss has reached resting position
                bossFire = BossFire(boss.rect.centerx, boss.rect.bottom)
                bossFireGroup.add(bossFire)
                lastBossShot = timeNow
