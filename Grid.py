import csv
import pygame
import time
from Block import Block
from typing import Optional
import math

from images.map.BlockProcessor import scaled_image

BRICK = "BRICK"
EMPTY = "EMPTY"


class Grid:
    """This class is for the background grid."""

    def __init__(
        self, grid_size: tuple[int, int], block_size: int, stage: Optional[int]
    ):
        self.grid_size = grid_size
        self.block_size = block_size
        self.grid_list = []
        self.create_grid_list()
        self.grid = self.get_grid(stage)
        from Vine import VineGroup

        self.vine_group_list = [VineGroup() for i in range(30)]

    def get_grid(self, stage: Optional[int]):
        """
        This method creates the grid by reading the appropriate csv file for a map. What file to choose depends on the player stage.
        """
        if not stage or stage >= 30:#30스테이지 이상은 없음
            stage = 0
        return self.grid_list[stage]

    def create_grid_list(self):
        """
        This reads the whole csv file and updates the grid list.
        """
        BRICK_IMAGE = scaled_image("BRICK")
        EMPTY_IMAGE = scaled_image("EMPTY")
        start_time = time.time()
        with open("images/map/map_all.csv", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            row_cnt, col_cnt = 0, 0
            grid = []
            for row in csv_reader:
                new_row = []
                for value in row:
                    new_row.append(
                        Block("BRICK", BRICK_IMAGE, row_cnt, col_cnt)
                        if int(value) == 1
                        else Block("EMPTY", EMPTY_IMAGE, row_cnt, col_cnt)
                    )
                    col_cnt += 1
                grid.append(new_row)
                row_cnt += 1
                col_cnt = 0
                if row_cnt == 12:
                    self.grid_list.append(grid)
                    grid = []
                    row_cnt = 0
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    start_time = end_time

    def draw_grid(self, screen: pygame.Surface):
        """
        This method draws the grid on the screen.
        :param screen:
        :return:
        """
        for grid_row in self.grid:
            for block in grid_row:
                screen.blit(block.image, block.rect.topleft)

    def movable_left(self, player:pygame.sprite) -> bool:
        """
        This method returns a value whether the player can move left.
        """
        #모든 Block에 대해
        for grid_row in self.grid:
            for block in grid_row:
                #Brick만 충돌 판별
                if block.type=="BRICK":
                    #충돌 감지
                    if (player.rect.x < block.rect.right < player.rect.x+player.rect.width
                        and (block.rect.top<player.rect.y<block.rect.bottom
                             or block.rect.top<player.rect.y+player.rect.height < block.rect.bottom
                             or player.rect.y<block.rect.top<player.rect.y+player.rect.height
                             or player.rect.y<block.rect.bottom<player.rect.y+player.rect.height)
                        and round(-block.rect.right+player.rect.x,4)>=math.floor(math.sin(player.angle)*player.speed)
                        # and math.sin(player.angle)<0
                    ):
                        player.rect.x=block.rect.right
                        return False
        #좌측 끝
        if player.rect.x<0:
            player.rect.x=0
            return False
        return True

    def movable_right(self, player:pygame.sprite) -> bool:
        """
        This method returns a value whether the player can move right.
        """
        #모든 Block에 대해
        for grid_row in self.grid:
            for block in grid_row:
                #Brick만 충돌 판별
                if block.type=="BRICK":
                    #충돌 감지
                    if (player.rect.x+player.rect.width> block.rect.left > player.rect.x
                        and (block.rect.top<player.rect.y<block.rect.bottom
                             or block.rect.top<player.rect.y+player.rect.height < block.rect.bottom
                             or player.rect.y<block.rect.top<player.rect.y+player.rect.height
                             or player.rect.y<block.rect.bottom<player.rect.y+player.rect.height)
                        and round(player.rect.x+player.rect.width-block.rect.left,4)<=math.ceil(math.sin(player.angle)*player.speed)
                        # and math.sin(player.angle)>=0
                    ):
                        player.rect.x=block.rect.left-player.rect.width
                        return False
        #우측 끝
        if player.rect.x+player.rect.width>16*self.block_size:
            player.rect.x=16*self.block_size-player.rect.width
            return False
        return True

    def movable_down(self, player:pygame.sprite) -> bool:
        """
        This method returns a value whether the player can move down.
        """
        #모든 Block에 대해
        for grid_row in self.grid:
            for block in grid_row:
                #Brick만 충돌 판별
                if block.type=="BRICK":
                    #충돌 감지
                    if (player.rect.y < block.rect.top <= player.rect.y+player.rect.height
                        and (block.rect.left<=player.rect.x<=block.rect.right
                             or block.rect.left<player.rect.x+player.rect.width<block.rect.right
                             or player.rect.x<block.rect.left<player.rect.x+player.rect.width
                             or player.rect.x<block.rect.right<player.rect.x+player.rect.width)
                        and round(player.rect.y+player.rect.height-block.rect.top,4)<=math.ceil(-math.cos(player.angle)*player.speed)
                        # and math.cos(player.angle)<=0
                    ):
                        player.rect.y=block.rect.top-player.rect.height
                        return False
        return True

    def movable_up(self, player:pygame.sprite) -> bool:
        """
        This method returns a value whether the player can move up.
        """
        #모든 Block에 대해
        for grid_row in self.grid:
            for block in grid_row:
                #Brick만 충돌 판별
                if block.type=="BRICK":
                    #충돌 감지
                    if (player.rect.y+player.rect.height > block.rect.bottom > player.rect.y
                        and (block.rect.left<player.rect.x<block.rect.right
                             or block.rect.left<player.rect.x+player.rect.width < block.rect.right
                             or player.rect.x<block.rect.left<player.rect.x+player.rect.width
                             or player.rect.x<block.rect.right<player.rect.x+player.rect.width)
                        and math.cos(player.angle)>0
                    ):
                        player.rect.y=block.rect.bottom
                        return False
        return True