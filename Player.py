import pygame
import math
import random
import time
from Colors import BLUE

from Grid import Grid
from fonts.Font import FLOOR_FONT
from images.lamp.Lamp import get_lamp_by_stage
from images.player.PlayerImage import select_image


def verbose_keys(keys) -> str:
    """
    Interprets the keys data to a verbose string
    """
    if keys[pygame.K_UP]:
        return "UP"
    if keys[pygame.K_LEFT]:
        return "LEFT"
    if keys[pygame.K_RIGHT]:
        return "RIGHT"
    return "DEFAULT"

def vec_add(angle1, length1, angle2, length2):
    """
    This function adds two vectors and returns the angle and length of the resultant vector.
    :param angle1:
    :param length1:
    :param angle2:
    :param length2:
    :return angle, length
    """
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    angle = math.pi/2 - math.atan2(y, x)
    length = math.hypot(x, y)
    return angle, length

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        '''
        initialize player
        :param screen_width:
        :param screen_height:
        '''
        super().__init__()
        original_image = select_image((0,0))
        self.image = pygame.transform.scale(
            original_image,
            (30, 40),
        )
        self.rect = self.image.get_rect()
        self.rect.x = 51
        self.rect.y = 500
        self.rect.width = 30
        self.rect.height = 40
        self.speed = 0
        self.angle = 0
        self.move_speed = 2.4/3.6
        self.max_speed = 15/4
        self.gravity = 1/10
        self.player_stage = 0
        self.lamp = Lamp(self)
        self.state = "STOP"
        #action:{0:stop,1:walk,2:jump,3:charge,4:climb,5:collide}
        #direction:{0:left,1:right,2:stop}
        self.image_state=(0,0) #action, direction
        self.jump_strength = 0
        self.control=False

    def update(self,screen_height,grid,vine_group,keys):
        """
        This updates the player's position and state.
        :param screen_height:
        :param grid:
        :param vine_group:
        :param keys:
        :return:
        """
        if self.control:#if can move
            self.move_by_key(keys)
        else:#if not on vine nor collision_down
            self.apply_gravity()
        self.motion()
        self.collision(grid,vine_group)
        self.adjust()
        self.check_level(screen_height, grid, vine_group)

    def collision(self,grid:Grid,vine_group:pygame.sprite.Group):
        self.control=False
        self.collide_left=False
        self.collide_right=False
        self.collide_up=False
        self.collide_down=False
        #vine collision
        if not vine_group.vine_active:
            self.collide_vine=None
        else:
            self.collide_vine=pygame.sprite.spritecollideany(self, vine_group)

        if self.collide_vine:
            self.control=True
            self.convert_state_to_run()
            self.rect.y=self.collide_vine.rect.y-self.rect.height
            if self.image_state[0]!=3 and self.image_state[0]!=2:
                self.speed=0
                self.angle=0
            bush_sound = pygame.mixer.Sound("audio/bush.mp3")
            bush_sound.set_volume(0.9)
            bush_sound.play()
            return
        #grid collision
        if not grid.movable_left(self):
            self.collide_left=True
        elif not grid.movable_right(self):
            self.collide_right=True
        elif not grid.movable_up(self):
            self.collide_up=True
        elif not grid.movable_down(self):
            self.collide_down=True
            self.control=True
    def motion(self):#move
        if self.speed>self.max_speed:
            self.speed=self.max_speed
        self.rect.x += self.speed * math.sin(self.angle)
        self.rect.y -= self.speed * math.cos(self.angle)

    def adjust(self):
        #collide adjust + collide sound
        if not self.control:
            if self.collide_up:
                self.angle=math.pi-self.angle
                # self.speed*=0.35
                #collide sound
                p = random.random()
                if p < 0.15:#15% chances of um
                    collide_sound = pygame.mixer.Sound("audio/um.mp3")
                else:#85% chances of oof
                    collide_sound = pygame.mixer.Sound("audio/oof.mp3")
                collide_sound.play()
            if self.collide_left or self.collide_right:
                # self.speed*=0.5
                self.angle*=-1
                #collide sound
                p = random.random()
                if p < 0.15:#15% chances of um
                    collide_sound = pygame.mixer.Sound("audio/um.mp3")
                else:#85% chances of oof
                    collide_sound = pygame.mixer.Sound("audio/oof.mp3")
                collide_sound.play()
        if self.collide_down:
            self.speed=0

    def introduce_new_stage(self, grid: Grid, vine_group: pygame.sprite.Group):
        """
        This introduces a new stage, where the grid should be updated, the lamp should be
        incremented, and the vine group should be emptied.
        """
        self.player_stage += 1
        grid.grid = grid.grid_list[self.player_stage]
        self.lamp.increment()
        self.rect.y = 600 - self.rect.height

    def fall_to_previous_stage(self, grid: Grid):
        """
        Falls to the previous stage
        """
        self.player_stage -= 1
        grid.grid = grid.grid_list[self.player_stage]
        self.lamp.decrement()
        self.rect.y = -self.rect.height

    def check_level(self,screen_height, grid: Grid, vine_group: pygame.sprite.Group):
        #check fall
        if self.rect.y+self.rect.height>screen_height and math.cos(self.angle)<= 0 and self.player_stage>0:
            self.fall_to_previous_stage(grid=grid)
            return
        #check next
        if (math.cos(self.angle)>=0 and self.rect.y <= 0 and  self.player_stage<19):
            self.introduce_new_stage(grid=grid, vine_group=vine_group)
            return
        #check ending
        elif math.cos(self.angle)>=0 and self.rect.y <= 0 and  self.player_stage==19:
            self.player_stage+=1
            return

    def move_left(self):
        """
        This is for moving left.
        """
        self.angle=-math.pi/2
        self.speed=self.move_speed

    def move_right(self):
        """
        This is for moving right.
        """
        self.angle=math.pi/2
        self.speed=self.move_speed

    def jump_left(self):
        """
        This is for jumping left.
        """
        self.speed=(self.move_speed**2+(self.jump_strength/9)**2)**0.5
        self.angle=-(math.atan(self.move_speed/(self.jump_strength/9)))

    def jump_right(self):
        """
        This is for jumping right.
        """
        self.speed=(self.move_speed**2+(self.jump_strength/9)**2)**0.5
        self.angle=(math.atan(self.move_speed/(self.jump_strength/9)))

    def jump_stop(self):
        """
        This is for jumping straight up.
        """
        self.angle=0
        self.speed=self.jump_strength/9

    def apply_gravity(self):
        """
        This applies gravity. Note that the form of gravitational motion is discrete.
        """
        self.angle,self.speed=vec_add(self.angle, self.speed,math.pi,0.27*self.gravity)

    def convert_state_to_run(self) -> None:
        # You cannot change state when charging otherwise than jumping.
        if self.state.startswith("CHARGE"):
            return
        self.state = "RUN_" + self.state.split("_")[-1]

    def move_by_key(self,keys):
        # You cannot handle keys while jumping
        if not self.state.startswith("JUMP"):
            input_result: str = verbose_keys(keys=keys)
            #Jump stream + image state change
            if input_result.startswith("UP"):
                #jump direction
                if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                    self.state = "CHARGE_LEFT"
                    self.image_state=(3,0)
                elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                    self.state = "CHARGE_RIGHT"
                    self.image_state=(3,1)
                else:
                    self.state = "CHARGE_" + self.state.split("_")[-1]
                    if self.state == "CHARGE_LEFT":
                        self.image_state=(3,0)
                    elif self.state == "CHARGE_RIGHT":
                        self.image_state=(3,1)
                    else:
                        self.image_state=(3,2)
                self.jump_strength += 0.4
                #max jump_strength
                if self.jump_strength > 30:
                    self.state = "JUMP_" + self.state.split("_")[-1]
                    jump_sound = pygame.mixer.Sound("audio/jump.mp3")
                    jump_sound.play()
                    jump_sound.set_volume(0.2)
                    if self.state == "JUMP_LEFT":
                        self.jump_left()
                        self.image_state=(2,0)
                        self.state = "STOP"
                        self.jump_strength = 0
                    elif self.state == "JUMP_RIGHT":
                        self.jump_right()
                        self.image_state=(2,1)
                        self.state = "STOP"
                        self.jump_strength = 0
                    elif self.state == "JUMP_STOP":
                        self.jump_stop()
                        self.image_state=(2,2)
                        self.state = "STOP"
                        self.jump_strength = 0
            elif (input_result == "DEFAULT" or input_result == "CHARGE_"+self.state) and self.state.startswith("CHARGE"):
                # We need to jump here
                self.state = "JUMP_" + self.state.split("_")[-1]
                jump_sound = pygame.mixer.Sound("audio/jump.mp3")
                jump_sound.play()
                jump_sound.set_volume(0.2)
                if self.state == "JUMP_LEFT":
                    self.jump_left()
                    self.jump_strength = 0
                    self.state = "STOP"
                    self.image_state=(2,0)
                elif self.state == "JUMP_RIGHT":
                    self.jump_right()
                    self.jump_strength = 0
                    self.state = "STOP"
                    self.image_state=(2,1)
                elif self.state == "JUMP_STOP":
                    self.jump_stop()
                    self.jump_strength = 0
                    self.state = "STOP"
                    self.image_state=(2,2)
            elif input_result == "LEFT":
                if self.state.startswith("CHARGE"):
                    self.jump_left()
                    self.jump_strength=0
                    self.state = "STOP"
                    self.image_state=(2,0)
                else:
                    self.state = "RUN_LEFT"
                    self.move_left()
                    self.image_state=(1,0)
            elif input_result == "RIGHT":
                if self.state.startswith("CHARGE"):
                    self.jump_right()
                    self.jump_strength=0
                    self.state = "STOP"
                    self.image_state=(2,1)
                else:
                    self.state = "RUN_RIGHT"
                    self.move_right()
                    self.image_state = (1,1)
            else:
                self.state = "STOP"
                self.image_state = (0, 0)

        # Update image
        self.image = pygame.transform.scale(
            select_image(self.image_state),
            (30, 40),
        )


    def draw_player_and_lamp(self, screen=pygame.Surface):
        """
        This draws the player and the lamp.
        :param screen:
        :return:
        """
        def draw_player_stage(self: Player):
            player_font = FLOOR_FONT
            player_stage_text = "Stage " + str(self.player_stage + 1)
            rendered_text = player_font.render(player_stage_text, True, BLUE)
            screen.blit(rendered_text, (50, 50))

        self.lamp.update_lamp_position(self)
        screen.blit(self.image, self.rect.topleft)
        screen.blit(self.lamp.image, self.lamp.rect.topleft)
        draw_player_stage(self)


class Lamp(pygame.sprite.Sprite):
    def __init__(self, player: Player):
        """
        This initializes the lamp.
        """
        super().__init__()
        self.size = 30
        self.image = get_lamp_by_stage(0, self.size)
        self.rect = self.image.get_rect()
        self.brightness = 0
        self.rect.x = player.rect.x + 5
        self.rect.y = player.rect.y + 5

    def increment(self):
        """
        This increments the lamp brightness.
        """
        if self.brightness < 6:  # Maximum brightness is 6
            self.brightness += 1
        self.image = get_lamp_by_stage(self.brightness, self.size)

    def decrement(self):
        """
        This decrements the lamp brightness.
        """
        if self.brightness > 0:
            self.brightness -= 1
        self.image = get_lamp_by_stage(self.brightness, self.size)

    def update_lamp_position(self, player: Player):
        """
        This updates the lamp position.
        """
        self.rect.x = player.rect.x + 5
        self.rect.y = player.rect.y + 5
