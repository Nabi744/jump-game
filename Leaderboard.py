import pygame
import sys

from Colors import BLACK, WHITE
from User import *
from fonts.Font import LEADERBOARD_FONT


def get_sorted_users() -> list[User]:
    """
    This retrieves the users from pickled data and returns it in a form of a sorted list
    """
    users = load_users()
    return sorted(users.values(), key = lambda user : user.points, reverse=True)

def display_leaderboard(screen: pygame.Surface) -> None:
    """
    Based on the sorted list returned by `get_sorted_users`, the top 5 are displayed on the leaderboard.
    """
    font = LEADERBOARD_FONT
    screen.fill(BLACK)
    users_list = get_sorted_users()
    text_y = 50

    for i, user in enumerate(users_list[:10], start = 1):
        text = f"{i}. {user.name}: {user.points} points"
        rendered_text = font.render(text, True, WHITE)
        screen.blit(rendered_text, (50, text_y))
        text_y += 40
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.flip()
