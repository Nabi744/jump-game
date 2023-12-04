import pygame, sys
from Colors import BLACK, BLUE, RED
from User import get_or_create_user

from fonts.Font import USERNAME_FONT

def game_over(screen, username: str):
    """
    Returns Game over status
    """

    font = USERNAME_FONT
    game_over_text = font.render("You Broke All The Stages!!", True, BLUE)
    game_over_rect = game_over_text.get_rect(center=(400, 210))
    exit_button = pygame.Rect(0, 400, 800, 50)
    exit_text = font.render("Exit", True, RED)
    exit_rect = exit_text.get_rect(center=exit_button.center)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                get_or_create_user(username, 3000)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.collidepoint(event.pos):
                    get_or_create_user(username, 3000)
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()