import pygame
from Missle import Missle
from Explosion import Explosion
from pygame import mixer

# Sound
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
playerShoots=pygame.mixer.Sound("Assets/missleFire.mp3")
playerShoots.set_volume(0.5)
playerDead=mixer.Sound("Assets/deathExplosion.mp3")
playerDead.set_volume(0.5)


RED = (255, 0, 0)
GOLD = (255, 215, 0)  
GREEN = (0, 255, 0)

class Spaceship(pygame.sprite.Sprite): # Spaceship class
    def __init__(self, x, y, health):
        super().__init__()        
        # Load image
        self.image = pygame.image.load("Assets/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(x, y))
        self.healthStart = health
        self.healthRemaining = health
        self.lastShot = pygame.time.get_ticks()

    def update(self,missleGroup): # update method with movement and shooting
        self.mask = pygame.mask.from_surface(self.image)
        """Handle movement only"""
        speed = 5
        cooldown = 500  # milliseconds
        time_now = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.rect.x -= speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < 800:
            self.rect.x += speed
        if keys[pygame.K_SPACE] and time_now - self.lastShot > cooldown:
            playerShoots.play()
            missle = Missle(self.rect.centerx, self.rect.top)
            missleGroup.add(missle)
            self.lastShot = time_now

    def draw_health_bar(self, screen, screenHeight, explosionGroup,gameOver): # draw health bar and checks for game over (bottom-left corner)
        bar_x, bar_y = 20, screenHeight - 40  # 20px from left, 40px from bottom
        bar_width, bar_height = 300, 20
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        if self.healthRemaining > 0:
            health_width = int(bar_width * (self.healthRemaining / self.healthStart))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        elif self.healthRemaining <= 0 and self.alive():
            explosion = Explosion(self.rect.centerx, self.rect.centery,3)
            explosionGroup.add(explosion)
            playerDead.play()
            mixer.music.stop()   # instantly cuts the music
            self.kill()
            gameOver = -1  # Player lost
        pygame.draw.rect(screen, GOLD, (bar_x, bar_y, bar_width, bar_height), 3)  # Gold border
        return gameOver
