import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set window size (e.g., 480x800 for a phone)
screen_width = 480
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Clicker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (112, 128, 144)
DARK_GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)
GOLD = (255, 215, 0)
BUTTON_COLOR = (255, 223, 186)
BUTTON_SHADOW = (205, 173, 149)
BACKGROUND_COLOR = (30, 30, 30)

# Font
font = pygame.font.SysFont(None, 55)

# Score
score = 0

# Energy
energy = 1500
max_energy = 1500
energy_recharge_rate = 1  # Energy replenishment rate per second
last_recharge_time = time.time()

# Button size and position
button_radius = 100
button_center = (screen_width // 2, screen_height // 2)
button_rect = pygame.Rect(button_center[0] - button_radius, button_center[1] - button_radius, button_radius * 2,
                          button_radius * 2)

# Button state flag
is_pressed = False

# Upgrade button size and position
upgrade_button_width = 200
upgrade_button_height = 50
upgrade_button_x = screen_width // 2 - upgrade_button_width // 2
upgrade_button_y = screen_height - 100
upgrade_button_rect = pygame.Rect(upgrade_button_x, upgrade_button_y, upgrade_button_width, upgrade_button_height)

# Upgrade status flag
upgrade_purchased = False
upgrade_cost = 100  # Initial upgrade cost
upgrade_multiplier = 1  # Initial multiplier for score per click after upgrade


# Function to draw text on screen
def draw_text(text, font, color, surface, center_x, center_y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(center_x, center_y))
    surface.blit(textobj, textrect)


# Main game loop
running = True
while running:
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and energy >= upgrade_multiplier:
                distance = ((event.pos[0] - button_center[0]) ** 2 + (event.pos[1] - button_center[1]) ** 2) ** 0.5
                if distance <= button_radius:
                    score += upgrade_multiplier
                    energy -= upgrade_multiplier
                    is_pressed = True
            if upgrade_button_rect.collidepoint(event.pos) and score >= upgrade_cost:
                score -= upgrade_cost
                upgrade_multiplier += 1  # Increase score per click after upgrade
                upgrade_cost = 500  # Increase upgrade cost for the next upgrade
                is_pressed = False
        if event.type == pygame.MOUSEBUTTONUP:
            if is_pressed:
                is_pressed = False

    # Replenish energy
    if current_time - last_recharge_time >= 1:
        energy = min(energy + energy_recharge_rate, max_energy)
        last_recharge_time = current_time

    # Fill screen with dark color
    screen.fill(BACKGROUND_COLOR)

    # Display button
    pygame.draw.circle(screen, BUTTON_SHADOW, button_center, button_radius + 5)  # Shadow
    pygame.draw.circle(screen, BUTTON_COLOR, button_center, button_radius)  # Button

    # Display energy
    draw_text(f'Energy: {energy}/{max_energy}', font, WHITE, screen, screen_width // 2, 80)

    # Display score (below energy)
    draw_text(f'$ {score}', font, WHITE, screen, screen_width // 2, 140)

    # Display upgrade button
    pygame.draw.rect(screen, GOLD, upgrade_button_rect)
    draw_text(f"Upgrade (Cost: {upgrade_cost})", font, BLACK, screen, upgrade_button_x + upgrade_button_width // 2,
              upgrade_button_y + upgrade_button_height // 2)

    # Update screen
    pygame.display.flip()

    # Set frame rate
    pygame.time.Clock().tick(60)
