#!/bin/bash

# ==============================================================================
# HELLA COOL PROGRESS BAR
# ==============================================================================
# This script creates a smooth, animated progress bar in the terminal.
# It uses Unicode block characters to show fractional progress and 
# ANSI escape codes for 24-bit RGB color gradients.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Block Characters Setup
# ------------------------------------------------------------------------------
# Standard terminal characters take up full spaces. To create a "smooth" effect 
# instead of a choppy character-by-character jump, we use Unicode block elements.
# The array maps 0 to 8:
# 0: Empty space (" ")
# 1-7: Partial blocks from 1/8th width to 7/8th width ("▏", "▎", "▍", "▌", "▋", "▊", "▉")
# 8: Full block ("█")
blocks=(" " "▏" "▎" "▍" "▌" "▋" "▊" "▉" "█")

draw_progress_bar() {
    # --------------------------------------------------------------------------
    # 2. Input Parameters
    # --------------------------------------------------------------------------
    local percent=$1  # Current progress (0 to 100)
    local width=$2    # Total width of the progress bar in terminal columns
    
    # --------------------------------------------------------------------------
    # 3. Fractional Math in Bash
    # --------------------------------------------------------------------------
    # Native bash arithmetic ($(( ... ))) only supports integers (no decimals).
    # To determine the exact fractional block to draw, we multiply the total 
    # length by 8 (since we have 8 sub-block characters).
    # total_eighths: The absolute number of 1/8th blocks that need to be filled.
    local total_eighths=$(( percent * width * 8 / 100 ))
    
    # full_blocks: How many solid "█" characters we need.
    local full_blocks=$(( total_eighths / 8 ))
    
    # partial_idx: The remaining remainder (0 to 7) which maps to our partial blocks.
    local partial_idx=$(( total_eighths % 8 ))
    
    # --------------------------------------------------------------------------
    # 4. Building the Bar String
    # --------------------------------------------------------------------------
    local bar=""
    local i
    
    # Step A: Append all the solid full blocks
    for ((i=0; i<full_blocks; i++)); do
        bar="${bar}${blocks[8]}"
    done
    
    # Step B: If the bar isn't completely at 100%, append the partial block and padding
    if (( full_blocks < width )); then
        # Append the fractional block (e.g. "▌" if we are halfway through a character cell)
        bar="${bar}${blocks[$partial_idx]}"
        
        # Step C: Fill the rest of the available width with empty spaces
        for ((i=full_blocks+1; i<width; i++)); do
            bar="${bar} "
        done
    fi

    # --------------------------------------------------------------------------
    # 5. Color Gradient Calculation (Cyan to Green)
    # --------------------------------------------------------------------------
    # We use 24-bit TrueColor ANSI escape codes: \033[38;2;<R>;<G>;<B>m
    # To make it dynamic, we lock R=0 and G=255. 
    # As the percentage increases, we reduce the Blue channel from 255 down to 0.
    # 0%: Cyan (0, 255, 255) -> 100%: Green (0, 255, 0)
    local r=0
    local g=255
    local b=$(( 255 - (percent * 255 / 100) ))
    
    local COLOR="\033[38;2;${r};${g};${b}m"
    local RESET="\033[0m" # Resets the terminal color back to default

    # --------------------------------------------------------------------------
    # 6. Printing the Bar
    # --------------------------------------------------------------------------
    # \r (Carriage Return): Moves the cursor to the start of the current line 
    # WITHOUT moving down. This makes it overwrite the previous progress bar frame.
    printf "\r${COLOR}Progress: [%s] %3d%%${RESET}" "$bar" "$percent"
}

# ==============================================================================
# 7. Example Usage / Main Execution Loop
# ==============================================================================
width=40
total_steps=100

echo "Starting some hella cool task..."

# ------------------------------------------------------------------------------
# 8. Hide the Terminal Cursor
# ------------------------------------------------------------------------------
# tput civis hides the blinking cursor so it doesn't flicker during animation.
# The `|| echo -en "\033[?25l"` acts as a fallback for systems missing tput.
tput civis || echo -en "\033[?25l"

# ------------------------------------------------------------------------------
# 9. The Animation Loop
# ------------------------------------------------------------------------------
for ((i=0; i<=total_steps; i++)); do
    draw_progress_bar "$i" "$width"
    # sleep adds a small delay to simulate work and make the animation visible.
    sleep 0.04
done

# ------------------------------------------------------------------------------
# 10. Clean Up
# ------------------------------------------------------------------------------
# Always restore the cursor before the script exits!
tput cnorm || echo -en "\033[?25h"

# Print a newline (\n) so the next prompt doesn't overwrite the final 100% bar.
echo -e "\nTask completed successfully!"
