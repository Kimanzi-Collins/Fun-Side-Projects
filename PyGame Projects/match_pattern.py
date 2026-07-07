import pygame
import random
import sys
import os

# ---------------------------------------------------------
# 1. INITIALIZATION & SETUP
# ---------------------------------------------------------
# Initialize all imported pygame modules
pygame.init()

# Set up the display window
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Match The Pattern")

# Clock object to help control the game's framerate
clock = pygame.time.Clock()
FPS = 60

# ---------------------------------------------------------
# 2. DEFINING COLORS AND FONTS
# ---------------------------------------------------------
# Normal button colors (Made much darker to make clicks distinguishable)
RED = (100, 0, 0)
GREEN = (0, 100, 0)
BLUE = (0, 0, 100)
YELLOW = (100, 100, 0)

# Bright colors for when a button is "flashing" or active
BRIGHT_RED = (255, 50, 50)
BRIGHT_GREEN = (50, 255, 50)
BRIGHT_BLUE = (50, 50, 255)
BRIGHT_YELLOW = (255, 255, 50)

WHITE = (255, 255, 255)
BLACK = (15, 15, 15)

# Initialize fonts for drawing text
font = pygame.font.SysFont("Arial", 36, bold=True)
large_font = pygame.font.SysFont("Arial", 72, bold=True)

# ---------------------------------------------------------
# 3. SETTING UP THE BUTTONS
# ---------------------------------------------------------
# We define a 2x2 grid for our four buttons. 
pad = 20          # Spacing between buttons and screen edges
top_margin = 70   # Space at the top of the screen for the score

# Calculate width and height of each button dynamically
btn_w = (WIDTH - 3 * pad) // 2
btn_h = (HEIGHT - top_margin - 2 * pad) // 2

# Create pygame.Rect objects for each color button
# Rectangles define (x, y, width, height)
buttons = {
    "red": pygame.Rect(pad, top_margin, btn_w, btn_h),
    "green": pygame.Rect(2 * pad + btn_w, top_margin, btn_w, btn_h),
    "blue": pygame.Rect(pad, top_margin + pad + btn_h, btn_w, btn_h),
    "yellow": pygame.Rect(2 * pad + btn_w, top_margin + pad + btn_h, btn_w, btn_h)
}

# Dictionaries to easily map string names to their respective colors
normal_colors = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW}
bright_colors = {"red": BRIGHT_RED, "green": BRIGHT_GREEN, "blue": BRIGHT_BLUE, "yellow": BRIGHT_YELLOW}


# ---------------------------------------------------------
# 4. HELPER FUNCTIONS
# ---------------------------------------------------------
def draw_buttons(lit_button=None, score=0, high_score=0):
    """
    Clears the screen and draws the four colored buttons.
    If 'lit_button' is provided, that specific button is drawn with its bright color.
    """
    screen.fill(BLACK)
    
    # Draw the current score and high score at the top center
    score_text = font.render(f"Score: {score}  |  High Score: {high_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, top_margin // 2))
    screen.blit(score_text, score_rect)
    
    # Draw each button
    for color_name, rect in buttons.items():
        if lit_button == color_name:
            color = bright_colors[color_name]
        else:
            color = normal_colors[color_name]
        
        # draw.rect takes (surface, color, rect_object, border_radius)
        pygame.draw.rect(screen, color, rect, border_radius=20)
        
        # Draw a bright white outline to make the "lit" state extremely distinct
        if lit_button == color_name:
            pygame.draw.rect(screen, WHITE, rect, width=5, border_radius=20)

def draw_text_centered(text, text_font, color, y_offset=0):
    """Utility function to quickly draw centered text on the screen."""
    text_surface = text_font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

def flash_sequence(sequence, score, high_score):
    """
    Flashes the sequence of colors for the player to memorize.
    It loops through the list of colors and lights them up one by one.
    """
    # DIFFICULTY SCALING: 
    # Flash duration gets shorter as score goes up.
    # Base is 500ms, decreases by 25ms per point, minimum of 150ms.
    flash_duration = max(150, 500 - (score * 25))
    pause_duration = max(50, 250 - (score * 15))
    
    for color_name in sequence:
        draw_buttons(color_name, score, high_score) # Draw with the button lit up
        pygame.display.flip()           # Update the screen
        pygame.time.delay(flash_duration)          # Dynamic pause based on score
        
        draw_buttons(None, score, high_score)       # Draw with all buttons normal
        pygame.display.flip()
        pygame.time.delay(pause_duration)          # Dynamic pause between flashes

# ---------------------------------------------------------
# 5. MAIN GAME LOOP
# ---------------------------------------------------------
def main():
    # Load High Score from file
    high_score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")
    high_score = 0
    if os.path.exists(high_score_file):
        try:
            with open(high_score_file, "r") as f:
                high_score = int(f.read().strip())
        except ValueError:
            pass # If the file is corrupted, just keep high_score as 0

    # Game variables
    sequence = []      # The pattern the computer generates
    player_input = []  # The pattern the player has clicked so far
    score = 0
    
    # States: START (title screen), WATCH (computer flashes pattern), 
    # PLAY (waiting for player input), GAME_OVER (player messed up)
    state = "START" 
    
    running = True
    while running:
        # Event loop: handles inputs like mouse clicks and closing the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "START":
                    # Transition from title screen to the first pattern
                    state = "WATCH"
                    
                elif state == "GAME_OVER":
                    # Reset all variables to start a fresh game
                    sequence = []
                    score = 0
                    state = "WATCH"
                    
                elif state == "PLAY":
                    # Get the (x, y) coordinates of where the mouse clicked
                    mouse_pos = event.pos
                    clicked_button = None
                    
                    # Check if the mouse click collided with any of our button rectangles
                    for color_name, rect in buttons.items():
                        if rect.collidepoint(mouse_pos):
                            clicked_button = color_name
                            break
                    
                    # If the player actually clicked a button
                    if clicked_button:
                        # Flash the button they clicked briefly
                        draw_buttons(clicked_button, score, high_score)
                        pygame.display.flip()
                        
                        # Click speed is also scaled to the difficulty
                        click_flash_duration = max(100, 200 - (score * 10))
                        pygame.time.delay(click_flash_duration)
                        
                        draw_buttons(None, score, high_score)
                        pygame.display.flip()
                        
                        # Add their click to their input sequence
                        player_input.append(clicked_button)
                        
                        # Check if their click was correct
                        current_index = len(player_input) - 1
                        if player_input[current_index] != sequence[current_index]:
                            # They clicked the wrong button!
                            state = "GAME_OVER"
                            
                            # Save High Score if beaten
                            if score > high_score:
                                high_score = score
                                try:
                                    with open(high_score_file, "w") as f:
                                        f.write(str(high_score))
                                except Exception as e:
                                    print(f"Failed to save high score: {e}")
                                    
                        elif len(player_input) == len(sequence):
                            # They successfully matched the entire sequence!
                            score += 1
                            state = "WATCH"          # Switch back to the computer's turn
                            pygame.time.delay(1000)  # Pause for 1 second before next round

        # --- Game State Logic & Rendering ---
        
        if state == "START":
            screen.fill(BLACK)
            draw_text_centered("Match The Pattern!", large_font, WHITE, -50)
            draw_text_centered("Click anywhere to start", font, WHITE, 50)
            pygame.display.flip()
            
        elif state == "WATCH":
            # Computer's turn: clear player's past inputs
            player_input = []
            
            # Add a new random color to the sequence
            sequence.append(random.choice(list(buttons.keys())))
            
            # Draw standard buttons, pause briefly, then flash the new sequence
            draw_buttons(None, score, high_score)
            pygame.display.flip()
            pygame.time.delay(500) 
            
            flash_sequence(sequence, score, high_score)
            
            # Switch to player's turn
            state = "PLAY"
            
        elif state == "PLAY":
            # Just keep drawing the standard buttons while we wait for player clicks
            draw_buttons(None, score, high_score)
            pygame.display.flip()
            
        elif state == "GAME_OVER":
            screen.fill(BLACK)
            draw_text_centered("GAME OVER", large_font, RED, -50)
            draw_text_centered(f"Final Score: {score}", font, WHITE, 20)
            
            if score >= high_score and score > 0:
                draw_text_centered("NEW HIGH SCORE!", font, BRIGHT_YELLOW, 60)
                draw_text_centered("Click anywhere to restart", font, WHITE, 110)
            else:
                draw_text_centered("Click anywhere to restart", font, WHITE, 80)
            pygame.display.flip()

        # Limit framerate
        clock.tick(FPS)

    # Quit properly when the loop ends
    pygame.quit()
    sys.exit()

# Run the main function when the file is executed
if __name__ == "__main__":
    main()
