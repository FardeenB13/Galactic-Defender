import pygame, sys
from pygame.locals import *
from Spaceship import Spaceship
from Aliens import create_aliens
from AlienFire import AlienFire
from Boss import Boss
from BossFire import BossFire
from pygame import mixer
from Button import Button

pygame.init()
# Sound
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

clock = pygame.time.Clock()
fps = 60
screenWidth = 800
screen_height = 600

screen = pygame.display.set_mode((screenWidth, screen_height))
pygame.display.set_caption("Galactic Defender")

background = pygame.image.load("Assets/background.png")
def draw_background():
    screen.blit(background, (0,0))

font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
font50 = pygame.font.SysFont('Constantia', 50)

WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
SILVER = (192, 192, 192)

def drawText(text, font, color, x, y):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))
    

def main_game_loop():   
    # Game variables
    countDown= 3
    lastCount = pygame.time.get_ticks()
    boss_spawned = False
    gameOver = 0
    game_won = False
    spaceshipGroup = pygame.sprite.Group()
    spaceship = Spaceship(screenWidth // 2, screen_height - 100, 3)
    spaceshipGroup.add(spaceship)
    missleGroup = pygame.sprite.Group()
    alienGroup = pygame.sprite.Group()
    alienFireGroup = pygame.sprite.Group()
    bossGroup = pygame.sprite.Group()
    bossFireGroup = pygame.sprite.Group()
    boss_spawned = False
    explosionGroup = pygame.sprite.Group()
    create_aliens(alienGroup)

    run = True
    while run:
        clock.tick(fps)    
        draw_background()  #  draw background first
            
        if countDown == 0:
            # Check for win condition
            if boss_spawned and len(bossGroup) == 0 and not game_won:
                gameOver = 1  # Player won    
            
            if gameOver == 0:
            # --- Draw everything in the correct order ---
                spaceship.update(missleGroup)
                missleGroup.update(alienGroup,explosionGroup,bossGroup)
                alienGroup.update()
                AlienFire.shoot(alienGroup, alienFireGroup)
                alienFireGroup.update(screen_height, spaceshipGroup, spaceship, explosionGroup)
                bossFireGroup.update(screen_height, spaceshipGroup, spaceship, explosionGroup)
                bossFireGroup.draw(screen)
            else: # Game over screen (win or lose)
                if gameOver == 1 and not game_won:
                    drawText('YOU WIN!', font50, GOLD, (screenWidth / 2 - 110), (screen_height /2 + 60))
                if gameOver == -1:
                    drawText('GAME OVER!', font50, GOLD, (screenWidth / 2 - 110), (screen_height /2 + 60))
                            
        explosionGroup.update()
        if countDown > 0: # Countdown before game starts
            drawText('GET READY!', font40, GOLD, (screenWidth / 2 - 110), (screen_height /2 + 60))
            drawText(str(countDown), font50, GOLD, (screenWidth / 2 - 10), (screen_height /2 + 110))
            countTimer = pygame.time.get_ticks()
            if countTimer - lastCount > 1000:
                countDown -= 1
                lastCount = countTimer
            
            # --- Spawn Boss when aliens are gone ---
        if len(alienGroup) == 0 and not boss_spawned:
            boss = Boss(screenWidth // 2, -100, health=30)
            bossGroup.add(boss)
            boss_spawned = True   
            
            mixer.music.load("Assets/bossMusic.mp3")
            mixer.music.set_volume(0.5)
            mixer.music.play(-1)  # play arrival sound once
            
        # --- Boss logic ---
        if boss_spawned:
            bossGroup.update()
            bossGroup.draw(screen)

            # Boss shooting (only if boss reached resting position)
            for boss in bossGroup:
                if boss.is_ready_to_shoot():
                    BossFire.shoot(bossGroup, bossFireGroup)

            # Draw boss health bar
            for boss in bossGroup:
                boss.draw_health_bar(screen, screenWidth)
        
        for event in pygame.event.get(): # event handling
            if event.type == QUIT:
                run = False           
        
        #  --- Draw all sprite groups ---
        spaceshipGroup.draw(screen)     
        alienGroup.draw(screen)
        missleGroup.draw(screen)
        alienFireGroup.draw(screen)
        explosionGroup.draw(screen)
        gameOver= spaceship.draw_health_bar(screen,screen_height,explosionGroup,gameOver)  
        pygame.display.flip()            # flip once per frame
        

# ---------------- MENU SCREEN ----------------
def main_menu():
    # Start menu music
    mixer.music.load("Assets/menuMusic.mp3")   
    mixer.music.set_volume(0.5)
    mixer.music.play(-1)  # loop forever

    # Title font 
    title_font = pygame.font.SysFont('Constantia', 70)  
    title_text = title_font.render("GALACTIC DEFENDER", True, GOLD)
    title_rect = title_text.get_rect(center=(400, 120))  # center at top of screen

    while True:
        draw_background()  
        screen.blit(title_text, title_rect)  # draw title

        mouse_pos = pygame.mouse.get_pos()

        # Buttons
        play_button = Button(None, (400, 250), "PLAY", font50, GOLD, SILVER)
        controls_button = Button(None, (400, 350), "CONTROLS", font50, GOLD, SILVER)
        quit_button = Button(None, (400, 450), "QUIT", font50, GOLD, SILVER)

        for button in [play_button, controls_button, quit_button]:
            button.changeColor(mouse_pos)
            button.update(screen)

        for event in pygame.event.get(): # event handling for menu
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if play_button.checkForInput(mouse_pos):
                    mixer.music.stop()   # stop menu music when game starts
                    main_game_loop()
                    # restart menu music when returning to menu
                    mixer.music.load("Assets/menuMusic.mp3")
                    mixer.music.set_volume(0.5)
                    mixer.music.play(-1)
                if controls_button.checkForInput(mouse_pos):
                    controls_screen()
                if quit_button.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# ---------------- CONTROLS SCREEN ----------------
def controls_screen():
    while True:
        draw_background()
        mouse_pos = pygame.mouse.get_pos()

        window_width, window_height = screen.get_size()

        # Instructions split into multiple lines
        instructions = [
            "SPACE = Shoot",
            "A or <- = Move Left",
            "D or -> = Move Right"
        ]

        # Calculate total height of all lines
        line_height = font50.get_height()
        total_height = len(instructions) * line_height + (len(instructions) - 1) * 10  # 10 px spacing

        # Starting y position so block is vertically centered
        start_y = (window_height - total_height) // 2

        # Render each line centered
        for i, line in enumerate(instructions):
            text_surface = font50.render(line, True, GOLD)
            text_rect = text_surface.get_rect(center=(window_width // 2, start_y + i * (line_height + 10)))
            screen.blit(text_surface, text_rect)

        # Back button
        back_button = Button(None, (window_width // 2, window_height - 100), "BACK", font50, GOLD, SILVER)
        back_button.changeColor(mouse_pos)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and back_button.checkForInput(mouse_pos):
                return  # back to menu

        pygame.display.update()

# ---------------- START ----------------
main_menu()