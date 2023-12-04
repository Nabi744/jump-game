import pygame


def flip_image(image: pygame.Surface, verbose: str) -> pygame.Surface:
    if verbose.split("_")[-1] == "LEFT":
        return pygame.transform.flip(image, True, False)
    else:
        return image


def select_image(verbose: str) -> pygame.Surface:
    run_image = pygame.image.load("images/player/Idle_01.png").convert_alpha()
    charge_image = pygame.image.load("images/player/Jump_02.png").convert_alpha()
    jump_image = pygame.image.load("images/player/Jump_04.png").convert_alpha()
    stop_image = pygame.image.load("images/player/Dead_01.png").convert_alpha()

    state = verbose.split("_")[0]
    if state == "RUN":
        return flip_image(run_image, verbose=verbose)
    elif state == "CHARGE":
        return flip_image(charge_image, verbose=verbose)
    elif state == "JUMP":
        return flip_image(jump_image, verbose=verbose)
    elif state == "STOP":
        return flip_image(stop_image, verbose=verbose)