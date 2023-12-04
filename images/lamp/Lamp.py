import pygame
def get_lamp_by_stage(stage: int, size: int) -> pygame.Surface:
    """
    This gets `stage` as a parameter and outputs the corresponding surface for the
    lamp of that stage. As `stage` increases, the corresponding lamp should have brighter
    luminosity.
    """
    file_path_to_lamp = f"images/lamp/lamp_{stage}.png"
    image_of_lamp = pygame.image.load(file_path_to_lamp).convert_alpha()
    return pygame.transform.scale(image_of_lamp, (size, size),)
