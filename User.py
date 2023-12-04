import pickle
import pygame
import sys

from Colors import WHITE, BLACK
from fonts.Font import USERNAME_FONT

class User:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.points = 0


def load_users():
    """
    Loads users or makes one if `None`
    """
    try:
        with open("users_data.pkl", "rb") as file:
            users = pickle.load(file)
    except FileNotFoundError:
        users = {}
    return users


def save_users(users):
    """
    Overwrites the pickled data of users
    """
    with open("users_data.pkl", "wb") as file:
        pickle.dump(users, file)

def get_or_create_user(name: str) -> User:
    """
    This acts as a user manager, getting or creating a user via a name.
    """
    users = load_users()
    current_user = users.get(name, User(name))
    return current_user


def get_or_create_user(name: str, points=None) -> User:
    """
    This acts as a user manager, getting or creating a user via a name.
    """
    users = load_users()
    current_user = users.get(name, User(name))
    if points is not None:
        if current_user.points is None:
            current_user.points = points
        else:
            current_user.points = max(current_user.points, points)
    users[name] = current_user
    save_users(users=users)
    return current_user


def input_username(screen):
    """
    Inputs the username and links it to the user.
    """
    font = USERNAME_FONT
    input_box = pygame.Rect(300, 250, 200, 32)
    color_inactive = pygame.Color("lightskyblue3")
    color_active = pygame.Color("dodgerblue2")
    color = color_inactive
    active = False
    text = ""

    label_text = font.render("Enter your name:", True, WHITE)
    label_rect = label_text.get_rect(topleft=(input_box.x, input_box.y - 40))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill(BLACK)

        screen.blit(label_text, label_rect)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()