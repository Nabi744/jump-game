import pygame
import sys
# Initialize Pygame
pygame.init()



from fonts.Font import LEADERBOARD_FONT

from Colors import BLACK, BLUE, WHITE
from GameOver import game_over
from Grid import Grid
from Hope import Hope
from Leaderboard import display_leaderboard
from Player import Player
from User import get_or_create_user, input_username
from Vine import VineGroup

class Game():
    def __init__(self):
        # Set up display
        screen_width: int = 800
        screen_height: int = 600
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Jack & Ivy")


        # Set up font
        # FIXME: Modify fonts


        # FIXME: Fix the audio to desired.
        pygame.mixer.music.load("audio/About Our Journey.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)


        # Set Username and display leaderboard
        username = input_username(screen=screen)
        user = get_or_create_user(name=username)
        display_leaderboard(screen=screen)

        # Initialize clock
        clock = pygame.time.Clock()

        # Create needed instances
        player = Player(screen_width, screen_height)
        player.player_stage = user.points // 100 if user.points > 0 else 0
        hope_gauge = Hope(screen_width=screen_width, screen_height=screen_height)

        # Create Grid
        grid_size = (screen_height // player.size, screen_width // player.size)
        block_size = player.size
        background = Grid(
            grid_size=grid_size,
            block_size=block_size,
            stage=user.points // 100 if user.points > 0 else 0,
        )
        if player.player_stage!=30:
            vine_group = background.vine_group_list[player.player_stage]
        else:
            game_over(screen,username=username)

        # Vine should be created after 5 seconds
        elapsed_time_after_stage = pygame.time.get_ticks()
        current_stage = 0

        # Exit Button
        exit_button = pygame.Rect(12.5, 10, 100, 50)
        return_button = pygame.Rect(40, 100, 100, 50)
        exit_text = LEADERBOARD_FONT.render("EXIT", True, BLUE)
        return_text = LEADERBOARD_FONT.render("RETURN", True, BLUE)
        exit_text_rect = exit_text.get_rect(center=exit_button.center)
        return_text_rect = return_text.get_rect(center=return_button.center)
        exit_status = False
        run=True
        while run:
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    get_or_create_user(username, (player.player_stage + 1) * 100)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if exit_button.collidepoint(event.pos):
                        get_or_create_user(username, (player.player_stage + 1) * 100)
                        pygame.quit()
                        sys.exit()
                    if return_button.collidepoint(event.pos):
                        exit_status = False
            # Get key states
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                print("ESCAPE PRESSED")
                exit_status = True

            if exit_status:
                screen.fill(BLACK)
                pygame.draw.rect(screen, BLACK, exit_button)
                pygame.draw.rect(screen, BLACK, return_button)
                screen.blit(exit_text, exit_text_rect)
                screen.blit(return_text, return_text_rect)
                pygame.display.flip()
                continue

            # Move player
            player.update(screen_height, grid=background, vine_group=vine_group, keys=keys)
            if player.player_stage == 30:
                game_over(screen, username)

            hope_gauge.increment()
            hope_used = hope_gauge.use_hope(
                keys, vine_group=vine_group, player=player, grid=background
            )

            # Initialize screen by first filling it with white
            screen.fill(WHITE)

            # Draw Grid
            background.draw_grid(screen=screen)

            if current_stage != player.player_stage:
                current_stage = player.player_stage
                elapsed_time_after_stage = pygame.time.get_ticks()


            vine_group = background.vine_group_list[player.player_stage]
            current_time = pygame.time.get_ticks()
            vine_group.insert_vine(player.rect.x, player.rect.y, player.size, screen_height)
            vine_group.update()
            if current_time - elapsed_time_after_stage >= 1200:
                if player.player_stage>=1:
                    background.vine_group_list[player.player_stage-1].vine_active=True
            vine_group.draw(screen)

            # Draw Player and Lamp
            player.draw_player_and_lamp(screen=screen)

            # Draw hope gauge
            hope_gauge.draw_hope_gauge(screen=screen)

            pygame.display.flip()

            # Cap the frame rate
            clock.tick(240)


if __name__ == "__main__":
    game = Game()