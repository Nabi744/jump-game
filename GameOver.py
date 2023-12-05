import pygame, sys
from Colors import BLACK, BLUE, RED
from User import get_or_create_user

from fonts.Font import USERNAME_FONT

def game_over(screen, username: str):
    """
    Returns Game over status
    """
    font = USERNAME_FONT
    #The end
    game_over_text = font.render("The End!", True, BLUE)
    game_over_rect = game_over_text.get_rect(center=(700, 70))
    #exit
    exit_button = pygame.Rect((630,550), (100, 50))
    exit_text = font.render("Exit", True, RED)
    exit_rect = exit_text.get_rect(center=exit_button.center)
    # poem_sound=pygame.mixer.Sound("audio/poem.wav")
    # poem_sound.play()
    #poem
    poem_image=pygame.image.load("images/poem.jpg").convert_alpha()
    poem_image=pygame.transform.scale(poem_image,(450,600))

    #game over
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                get_or_create_user(username, 2100)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.collidepoint(event.pos):
                    get_or_create_user(username, 2100)
                    pygame.quit()
                    sys.exit()
        screen.fill(BLACK)
        screen.blit(poem_image,(175,0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()