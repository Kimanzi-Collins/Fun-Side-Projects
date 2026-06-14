import pygame
import sys

# 1. Initialize the library
pygame.init()

# 2. Setup the display window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame")

# 3. Setup game variables (State)
clock = pygame.time.Clock()
FPS = 60

# Let's define our player object's starting state
player_x = 400
player_y = 300
player_size = 50
player_speed = 5

# 4. The Main Game Loop
running = True
while running:
    
    # --- PHASE 1: EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Triggers when the 'X' button is clicked
            running = False

    # --- PHASE 2: UPDATE STATE ---
    # Check for sustained key presses
    keys = pygame.key.get_pressed()
    
    # Update coordinate math based on input
    if keys[pygame.K_LEFT]:
            player_x -= player_speed
    if keys[pygame.K_RIGHT]:
            player_x += player_speed
    if keys[pygame.K_UP]:
            player_y -= player_speed
    if keys[pygame.K_DOWN]:
            player_y += player_speed

    # --- PHASE 3: RENDER (DRAW) ---
    # Wipe the previous frame clean with a solid background color (RGB)
    screen.fill((0, 0, 0)) # Black background

    # Draw the player: surface, color (RGB), [X, Y, Width, Height]
    pygame.draw.rect(screen, (0, 128, 255), [player_x, player_y, player_size, player_size])

    # Push the newly drawn frame to the actual display
    pygame.display.flip()

    # --- PHASE 4: TIMING ---
    # Cap the framerate to ensure the game runs at the same speed on all hardware
    clock.tick(FPS)

# Cleanly exit the program when the loop breaks
pygame.quit()
sys.exit()