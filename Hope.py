import pygame

from Colors import GREEN, WHITE
from Grid import Grid
from Player import Player


def color_shimmer_generator(
    a: tuple[int, int, int], increasing: bool
) -> (tuple[int, int, int], bool):
    """
    Generates a color shimmering effect when the hope gauge bar is full.
    It gradually switches from green to yellow, based on the increasing
    bool argument.
    """
    if increasing:
        b = (a[0] + 1, a[1], a[2])
        if b[0] == 255:
            return (b, False)
        else:
            return (b, True)
    else:
        b = (a[0] - 1, a[1], a[2])
        if b[0] == 0:
            return (b, True)
        else:
            return (b, False)


class Hope:
    """
    This class represents the hope gauge and its design features.
    """
    def __init__(self, screen_width, screen_height):
        self.value = 0
        self.max_value = 100
        self.width = screen_width - 20
        self.height = 20
        self.increasing = True
        self.rect = pygame.Rect(10, 10, self.width, self.height)
        self.hope_rect = pygame.Rect(10, 10, 0, self.height)
        self.color = GREEN
        self.last_incremented_time = pygame.time.get_ticks()

    def increment(self):
        """
        The hope gauge should increment every 0.5 seconds. To implement this, 
        we use the milliseconds time method via the pygame module and compare it
        with the last incremented time. If the gauge is full, we need not increment.
        """

        current_time = pygame.time.get_ticks()
        if current_time - self.last_incremented_time < 40:
            return

        if self.value < self.max_value:
            self.value += 1
            self.last_incremented_time = current_time
            self.hope_rect = pygame.Rect(
                10, 10, round(self.width * (self.value / 100)), self.height
            )
        else:
            color = color_shimmer_generator(self.color, self.increasing)
            self.color = color[0]
            self.increasing = color[1]

    def use_hope(self, keys, vine_group: pygame.sprite.Group, player: Player, grid: Grid) -> bool:
        """
        This is for the hope skill. If the hope gauge is full and the SPACE_BAR is 
        pressed, we grow the vine up to the top and then let the player climb it.
        """
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if self.value != self.max_value:
                return False
            self.last_incremented_time = current_time
            self.value = 0
            vine_group.make_vine_to_top(player)
            return True

    def draw_hope_gauge(self, screen):
        pygame.draw.rect(screen, self.color, self.hope_rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
