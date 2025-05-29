import pygame, sys
import random
import math
import time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# ─── CONSTANTS AND ASSETS ──────────────────────────────────────────────────────

SCREEN_WIDTH = 798
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brzi i besni')

# Load icons & images
logo = pygame.image.load('logo.jpeg')
pygame.display.set_icon(logo)

bg_img         = pygame.image.load('bg.png')
intro_img      = pygame.image.load('intro.png')
gameover_img   = pygame.image.load('gameover.png')
main_car_img   = pygame.image.load('car.png')
enemy_car1_img = pygame.image.load('car1.jpeg')
enemy_car2_img = pygame.image.load('car2.png')

# Fonts
IntroFont = pygame.font.Font("freesansbold.ttf", 38)
font_large = pygame.font.Font("freesansbold.ttf", 85)
font_small = pygame.font.Font("freesansbold.ttf", 25)

# Sounds
starting_music   = 'startingMusic.mp3'
background_music = 'BackgroundMusic.mp3'
crash_sound_file = 'car_crash.wav'

# Highscore file
HIGHSCORE_FILE = "highscore.txt"

# ─── LANES SETUP ────────────────────────────────────────────────────────────────
# We define exactly three lanes by their X‐coordinates (centers)
LANE_X = [178, 334, 490]
# Index 0 = left lane (x=178), 1 = middle lane (x=334), 2 = right lane (x=490)

# ─── INTRO SCREEN ───────────────────────────────────────────────────────────────

def intro_screen():
    pygame.mixer.music.load(starting_music)
    pygame.mixer.music.play(-1)
    click = False
    run = True

    # Create a PLAY button rectangle for hover/click detection
    play_button = pygame.Rect(265, 440, 300, 50)

    while run:
        screen.fill((0, 0, 0))
        screen.blit(intro_img, (0, 0))

        # Draw “PLAY” text
        play_text = IntroFont.render("PLAY", True, (255, 0, 0))
        screen.blit(play_text, (280, 450))

        # Draw a white border around the button, change to dark red on hover
        mx, my = pygame.mouse.get_pos()
        if play_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (155, 0, 0), play_button, 6)
        else:
            pygame.draw.rect(screen, (255, 255, 255), play_button, 6)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.collidepoint((mx, my)):
                    click = True

        if click:
            # Stop intro music and start countdown
            pygame.mixer.music.stop()
            countdown()
            return

        pygame.display.update()


# ─── COUNTDOWN ─────────────────────────────────────────────────────────────────

def countdown():
    pygame.mixer.music.load(background_music)
    # We won’t start background music until actual game loop
    
    # Pre‐render numbers once
    three_surf = font_large.render('3', True, (187, 30, 16))
    two_surf   = font_large.render('2', True, (255, 255, 0))
    one_surf   = font_large.render('1', True, (51, 165, 50))
    go_surf    = font_large.render('GO!!!', True, (0, 255, 0))

    # Show each on background for 1 second
    for surf in [three_surf, two_surf, one_surf, go_surf]:
        screen.blit(bg_img, (0, 0))
        # Center roughly in screen
        if surf == go_surf:
            screen.blit(surf, (300, 250))
        else:
            screen.blit(surf, (350, 250))
        pygame.display.update()
        time.sleep(1)

    # Now start the actual game
    gameloop()


# ─── GAME LOOP ─────────────────────────────────────────────────────────────────

def gameloop():
    # Play background music
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.play(-1)

    # Crash sound
    crash_sound = pygame.mixer.Sound(crash_sound_file)

    # Initialize score and highscore
    score_value = 0
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            highscore_value = int(f.read().strip())
        except:
            highscore_value = 0

    # Helper to show current score
    def show_score(x, y):
        score_surf = font_small.render("SCORE: " + str(score_value), True, (255, 0, 0))
        screen.blit(score_surf, (x, y))

    # Helper to show high score
    def show_highscore(x, y):
        hiscore_surf = font_small.render("HISCORE: " + str(highscore_value), True, (255, 0, 0))
        screen.blit(hiscore_surf, (x, y))

    # GAME OVER sub‐loop
    def game_over_screen():
        nonlocal score_value, highscore_value
        # Stop music and play crash
        pygame.mixer.music.stop()
        crash_sound.play()
        time.sleep(1)

        run_go = True
        while run_go:
            screen.blit(gameover_img, (0, 0))
            # Flicker score/hiscore
            show_score(330, 400)
            show_highscore(330, 450)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart entire game (go back to countdown, then gameloop)
                        run_go = False
                        countdown()
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # ── INITIAL POSITIONS ────────────────────────────────────────────

    # Main car starts in the middle lane (index 1)
    main_lane = 1
    maincarX = LANE_X[main_lane]
    maincarY = 495  # fixed Y near bottom

    # Two enemies: each is [lane_index, Y_position, image]
    enemy1_lane = random.randint(0, 2)
    enemy1X = LANE_X[enemy1_lane]
    enemy1Y = -100  # start off-screen
    enemy1_speed = 7

    enemy2_lane = random.randint(0, 2)
    enemy2X = LANE_X[enemy2_lane]
    enemy2Y = -200  # start off-screen (staggered)
    enemy2_speed = 9  # slightly faster for variety

    run = True
    while run:
        # ── EVENT HANDLING ───────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move left one lane (clamped)
                    main_lane = max(0, main_lane - 1)
                    maincarX = LANE_X[main_lane]
                if event.key == pygame.K_RIGHT:
                    # Move right one lane (clamped)
                    main_lane = min(2, main_lane + 1)
                    maincarX = LANE_X[main_lane]
                # No UP/DOWN movement any more

        # ── UPDATE ENEMY POSITIONS ─────────────────────────────────
        enemy1Y += enemy1_speed
        enemy2Y += enemy2_speed

        # ── CHECK IF ENEMIES PASSED BOTTOM → SCORE + RESPAWN ─────────
        if enemy1Y > SCREEN_HEIGHT:
            score_value += 1
            # Respawn off-screen with new random lane
            enemy1_lane = random.randint(0, 2)
            enemy1X = LANE_X[enemy1_lane]
            enemy1Y = -100

        if enemy2Y > SCREEN_HEIGHT:
            score_value += 1
            enemy2_lane = random.randint(0, 2)
            enemy2X = LANE_X[enemy2_lane]
            enemy2Y = -200

        # Update highscore if beaten
        if score_value > highscore_value:
            highscore_value = score_value

        # ── DRAW EVERYTHING ────────────────────────────────────────
        screen.fill((0, 0, 0))
        screen.blit(bg_img, (0, 0))

        # Draw main car
        screen.blit(main_car_img, (maincarX, maincarY))

        # Draw enemies
        screen.blit(enemy_car1_img, (enemy1X, enemy1Y))
        screen.blit(enemy_car2_img, (enemy2X, enemy2Y))

        # Draw scores
        show_score(570, 20)
        show_highscore(10, 20)

        pygame.display.update()

        # ── CHECK COLLISIONS ───────────────────────────────────────
        # Use Rect collisions (simpler than distance)
        main_rect = pygame.Rect(maincarX, maincarY,
                                main_car_img.get_width(),
                                main_car_img.get_height())

        enemy1_rect = pygame.Rect(enemy1X, enemy1Y,
                                  enemy_car1_img.get_width(),
                                  enemy_car1_img.get_height())
        enemy2_rect = pygame.Rect(enemy2X, enemy2Y,
                                  enemy_car2_img.get_width(),
                                  enemy_car2_img.get_height())

        if main_rect.colliderect(enemy1_rect) or main_rect.colliderect(enemy2_rect):
            # Stop movement and go to game over
            run = False

        # ── CAP FPS FOR SMOOTH PLAY ─────────────────────────────────
        pygame.time.Clock().tick(60)

        # If we detected collision, break the loop
        if not run:
            # Save highscore back to file
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(highscore_value))
            # Show Game Over screen
            game_over_screen()
            return  # After game_over returns, we don’t continue this loop

    # Outside while-run (should never get here normally)
    pygame.quit()
    sys.exit()


# ─── ENTRY POINT ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Make sure highscore file exists
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            int(f.read().strip())
    except:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write("0")

    intro_screen()
