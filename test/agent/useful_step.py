from base_agent import*
import pygame
import sys
import numpy as np
from pygamewrapper import PyGameWrapper
from reversi_board import ReversiBoard
import utils

class useful_step(PyGameWrapper):
    def __init__(self, width=600, height=600):
        self.side_length = min(width, height)
        self.top_left = (0,0)
        self.board = ReversiBoard(self.side_length, self.top_left)
        actions = self._init_action_set()
        super().__init__(width, height, actions=actions)

        self.last_label = '1A'
        self.cur_player = -1
        self.prev_action_time = 0
    def _init_action_set(self): 
        actions = {}
        for i, row in enumerate(self.board.rows):
            for j , col in enumerate(self.board.cols):
                x = 0.1 * self.side_length + 0.8 * (j+0.5) / len(self.board.cols) * self.side_length
                y = 0.1 * self.side_length + 0.8 * (i+0.5) / len(self.board.rows) * self.side_length
                actions[row+col] = utils.element_wise_addition(self.top_left, (x, y))
        return actions

    def pos2label(self, pos):
        pos = tuple([p - tl for p, tl in zip(pos, self.top_left)])
        if (pos[0] < 0 or pos[0] > self.side_length or
            pos[1] < 0 or pos[1] > self.side_length):
            raise utils.ValueOutOfRange()

        return self.board.pos2label(pos)

    def _is_available(self, label, flip=False):
        status = self.get_game_state()
        if status[self.board.enum[label]]==2:
            print(status[self.board.enum[label]] )
        if status[self.board.enum[label]] == 2 and flip == False:
            return True

        if status[self.board.enum[label]] == 0 or status[self.board.enum[label]] == 2:
            return self._check_around(label, flip=flip)

        return False

    def _check_around(self, label, flip):
        is_avail = False
        status = self.get_game_state()
        row = int(self.board.enum[label] // len(self.board.cols))
        col = int(self.board.enum[label] % len(self.board.cols))
        for i in range(-1, 2):
            if row+i < 0 or row+i >= len(self.board.rows): continue

            for j in range(-1, 2):
                if col+j < 0 or col+j >= len(self.board.cols): continue

                label = self.board.rows[row+i] + self.board.cols[col+j]
                if status[self.board.enum[label]] == -1 * self.cur_player:
                    if self._check_direction(row, col, i, j, flip=flip):
                        is_avail = True
                    
        return is_avail

    def _check_direction(self, row, col, dx, dy, flip):
        is_avail = False
        status = self.get_game_state()
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < len(self.board.rows) and 0 <= col+y[-1] < len(self.board.cols):
            label = self.board.rows[row+x[-1]] + self.board.cols[col+y[-1]]
            if status[self.board.enum[label]] == 0:
                break
            if status[self.board.enum[label]] == self.cur_player:
                if flip:
                    for r, c in zip(x, y):
                        self.board.update(self.board.rows[row+r]+self.board.cols[col+c], self.cur_player)
                    is_avail = True
                    break
                else:
                    return True

            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return is_avail

    def _get_available_actions(self):
        avail = []
        for row in self.board.rows:
            for col in self.board.cols:
                if self._is_available(row+col):
                    avail.append(row+col)  
        return avail

    def get_game_state(self):
        return self.board.status

    def get_actions(self):
        return self.actions

if __name__=='__main__':
    game=useful_step()
    print(game.get_game_state())






    



# print(MyAgent().enum) 