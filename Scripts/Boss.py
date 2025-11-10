import pygame
from pygame import mixer
from Explosion import Explosion

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
bossDead=mixer.Sound("Assets/deathExplosion.mp3")
bossDead.set_volume(0.5)

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health=30):
        super().__init__()
        # Load image
        self.image = pygame.image.load("Assets/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))  # Bigger boss
        self.rect = self.image.get_rect(center=(x, y))
        self.move_counter = 0
        self.move_direction = 1

        # Health
        self.healthStart = health
        self.healthRemaining = health  # use only this for tracking

        # Movement
        self.speed = 2
        self.resting_y = 200  # stop a little higher than center

    def update(self): # update method with movement (based on Alien)
        if self.rect.top < self.resting_y: # Move down to resting position
            self.rect.y += self.speed
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75: # Change direction per frame
            self.move_direction *= -1 
            self.move_counter *= self.move_direction
    

    def take_damage(self, amount, explosionGroup):
        """Reduce boss health by given amount."""
        self.healthRemaining -= amount
        if self.healthRemaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery,3)
            explosionGroup.add(explosion)
            mixer.Sound.play(bossDead)
            mixer.music.stop()   # instantly cuts the boss music
            self.kill()  # Remove boss from game

    def draw_health_bar(self, screen, screenWidth):
        """Draw health bar in HUD style (top-right corner)"""
        bar_width, bar_height = 200, 20
        bar_x = screenWidth - bar_width - 20  # 20px from right
        bar_y = 20  # top margin

        # Background (red)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # (green based on remaining health)
        if self.healthRemaining > 0:
            health_width = int(bar_width * (self.healthRemaining / self.healthStart))
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))

        # Border (gold)
        pygame.draw.rect(screen, (255, 215, 0), (bar_x, bar_y, bar_width, bar_height), 3)

    def is_ready_to_shoot(self):
        # Only shoot if boss has reached resting position
        return self.rect.top >= self.resting_y
