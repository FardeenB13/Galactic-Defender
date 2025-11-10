import pygame
from Explosion import Explosion
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
enemyExplodes=pygame.mixer.Sound("Assets/enemyExplosion.mp3")
enemyExplodes.set_volume(0.5)

class Missle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Correct image load
        self.image = pygame.image.load("Assets/missle.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (10, 10))    
        self.rect = self.image.get_rect(center=(x, y))

    def update(self,alienGroup,explosionGroup,bossGroup): # update method with collision detection
        self.rect.y -= 2  # move upward
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alienGroup, True): # Check collision with aliens
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery,2)
            explosionGroup.add(explosion)
            enemyExplodes.play()
        
        hits = pygame.sprite.spritecollide(self, bossGroup, False, pygame.sprite.collide_mask) # Precise collision with boss using mask
        if hits:
            for boss in hits:   # Loop through all bosses hit
                boss.take_damage(1, explosionGroup)  # Reduce boss health
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)
            enemyExplodes.play()