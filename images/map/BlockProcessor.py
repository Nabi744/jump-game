import pygame


def original_image(type: str) -> pygame.Surface:
    return pygame.image.load(f"images/map/{type}.png").convert_alpha()

def scaled_image(type: str) -> pygame.Surface:
    return pygame.transform.scale(original_image(type), (50, 50))