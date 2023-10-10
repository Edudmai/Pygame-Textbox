"""PygameTextBox-Demo File Description"""

import pygame
from ..pygametextbox import TextBox

# Finals - Settings for the project
BG_COLOR = pygame.Color('tan')
FONT = pygame.font.SysFont('Comic Sans MS', 24)
FPS = 30
HEIGHT = FONT.get_linesize()-FONT.get_descent()
WIN = pygame.display.set_mode((300, HEIGHT+80))

# Variables
textbox = TextBox(pygame.Rect(10, 10, 280, HEIGHT), font=FONT)
clock = pygame.time.Clock()
running = True

# Set up
pygame.display.set_caption("pygametextbox Demo")
pygame.event.set_blocked(None)
pygame.event.set_allowed( (pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP) )
pygame.key.set_repeat(300, 100)

# Game loop
while running:

    # Event handling
    events = pygame.event.get()
    for event in events:
        match event.type:
          case pygame.QUIT: running = False

    textbox.update(events) # Pass events to the textbox.update method every frame
        
    # Draw to the window
    WIN.fill(BG_COLOR)
    textbox.drawTo(WIN)
    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
exit()