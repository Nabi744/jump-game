import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, type: str, image: pygame.Surface, row: int, col: int):
        super().__init__()
        self.type = type
        self.size = 50
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = col * self.size
        self.rect.y = row * self.size