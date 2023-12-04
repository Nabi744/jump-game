import pygame
import time

def flip_image(image: pygame.Surface, verbose: str) -> pygame.Surface:
    if verbose.split("_")[-1] == "LEFT":
        return pygame.transform.flip(image, True, False)
    else:
        return image


def select_image(image_state) -> pygame.Surface:
    image_0_0 = pygame.image.load("images/player/Basic 0.png").convert_alpha()#stop_left
    image_0_1 = pygame.image.load("images/player/Basic 1.png").convert_alpha()#stop_right
    image_0_2 = pygame.image.load("images/player/Basic 2.png").convert_alpha()#stop_stop
    image_1_0_1 = pygame.image.load("images/player/Walk 1.png").convert_alpha()#walk_left1
    image_1_0_2 = pygame.image.load("images/player/Walk 2.png").convert_alpha()#walk_left2
    # image_1_1_1 = pygame.image.load("images/player/Walk 1.png").convert_alpha()#walk_right1
    # image_1_1_2 = pygame.image.load("images/player/Walk 2.png").convert_alpha()#walk_right2
    image_2_0 = pygame.image.load("images/player/Jump 0.png").convert_alpha()#jump_left
    image_2_1 = pygame.image.load("images/player/Jump 1.png").convert_alpha()#jump_right
    image_2_2 = pygame.image.load("images/player/Jump 2.png").convert_alpha()#jump_stop
    image_3_0 = pygame.image.load("images/player/Charge 0.png").convert_alpha()#charge_left
    image_3_1 = pygame.image.load("images/player/Charge 1.png").convert_alpha()#charge_right
    image_3_2 = pygame.image.load("images/player/Charge 2.png").convert_alpha()#charge_stop
    image_4_0 = pygame.image.load("images/player/Climb 0.png").convert_alpha()#climb1
    image_4_1 = pygame.image.load("images/player/Climb 1.png").convert_alpha()#climb2

    if image_state[0]==1:
        if time.time() % 0.5 > 0.25:
            return flip_image(eval(f"image_1_{image_state[1]}_1"))
        else:
            return flip_image(eval(f"image_1_{image_state[1]}_2"))
    elif image_stage[0]==4:
        if time.time() % 0.25 > 0.125:
            return flip_image(eval(f"image_4_{0}"))
        else:
            return flip_image(eval(f"image_4_{1}"))
    else:
        return flip_image(eval(f"image_{image_state[0]}_{image_state[1]}"))