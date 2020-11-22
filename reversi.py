import pygame
import sys
import numpy as np
from pygamewrapper import PyGameWrapper
from reversi_board import ReversiBoard
import utils

class Reversi(PyGameWrapper):
    """
        game_state:
            -1: dark side
            0: no piece
            1: light side
    """
    BG_COLOR = (255, 255, 255)
    def __init__(self, width=600, height=600, bg_color=BG_COLOR):
        screen_dim = (width, height)
        self.side_length = min(width, height)
        if width >= height:
            self.top_left = (0.5 * (width - height), 0)
        else:
            self.top_left = (0, 0.5 * (height - width))
        self.board = ReversiBoard(self.side_length, self.top_left)

        actions = self.board.enum
        super().__init__(width, height, actions=actions)

        self.bg_color = bg_color
        self.last_label = '1A'
        self.cur_player = -1

    def _handle_player_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                try:
                    if self.get_game_state()[self.board.enum[self.last_label]] == 2:
                        self.board.update(self.last_label, 0)
                    label = self.pos2label(event.pos)
                    if self._is_available(label):
                        self.last_label = label
                        self.board.update(label, 2)

                except utils.ValueOutOfRange:
                    pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    label = self.pos2label(event.pos)
                    if self._is_available(label):
                        self._flip(label)
                        if len(self.get_available_actions()) > 0:
                            self.cur_player *= -1

                except utils.ValueOutOfRange:
                    pass

    def pos2label(self, pos):
        pos = tuple([p - tl for p, tl in zip(pos, self.top_left)])

        if (pos[0] < 0 or pos[0] > self.side_length or
            pos[1] < 0 or pos[1] > self.side_length):
            raise utils.ValueOutOfRange()

        return self.board.pos2label(pos)

    def _flip(self, label):
        status = self.get_game_state()
        self.board.update(label, self.cur_player)
        row = int(self.board.enum[label] // len(self.board.rows))
        col = int(self.board.enum[label] % len(self.board.rows))
        for i in range(-1, 2):
            if row+i < 0 or row+i >= len(self.board.rows): continue

            for j in range(-1, 2):
                if col+j < 0 or col+j >= len(self.board.cols): continue

                label = self.board.rows[row+i] + self.board.cols[col+j]
                if status[self.board.enum[label]] == -1 * self.cur_player:
                    x, y = [i], [j]
                    while 0 <= row+x[-1] < len(self.board.rows) and 0 <= col+y[-1] < len(self.board.cols):
                        label = self.board.rows[row+x[-1]] + self.board.cols[col+y[-1]]
                        if status[self.board.enum[label]] == self.cur_player:
                            for r, c in zip(x, y):
                                self.board.update(self.board.rows[row+r]+self.board.cols[col+c], self.cur_player)
                            break

                        x.append(x[-1] + i)
                        y.append(y[-1] + j)



    def get_available_actions(self):
        avail = []
        for row in self.board.rows:
            for col in self.board.cols:
                if self._is_available(row+col):
                    avail.append(row+col)
                
        return avail

    def _is_available(self, label):
        status = self.get_game_state()
        block = self.board.enum[label]
        row = int(block // len(self.board.rows))
        col = int(block % len(self.board.rows))
        if status[block] == 2:
            return True
        if status[block] == 0:
            for i in range(-1, 2):
                if row+i < 0 or row+i >= len(self.board.rows): continue

                for j in range(-1, 2):
                    if col+j < 0 or col+j >= len(self.board.cols): continue

                    label = self.board.rows[row+i] + self.board.cols[col+j]
                    if status[self.board.enum[label]] == -1 * self.cur_player:
                        x, y = i, j
                        while (row+x >= 0 and row+x < len(self.board.rows) and
                               col+y >= 0 and col+y < len(self.board.cols)):
                            label = self.board.rows[row+x] + self.board.cols[col+y]
                            if status[self.board.enum[label]] == self.cur_player:
                                return True

                            x, y = utils.element_wise_addition((x, y), (i, j))

        return False

    def get_game_state(self):
        return self.board.status

    def get_actions(self):
        return self.actions

    def init(self):
        init_status = [('4D', 1), ('4E', -1), ('5D', -1), ('5E', 1)]
        for s in init_status:
            self.board.update(*s)

        self.screen.fill(self.bg_color)
        self.board.draw_board(self.screen)
        self.board.draw_pieces(self.screen)

    def game_over(self):
        if len(self.get_available_actions()) > 0:
            return True
        return False

    def step(self, dt):
        self._handle_player_events()
        self.board.draw_board(self.screen)
        self.board.draw_pieces(self.screen)

if __name__ == '__main__':
    pygame.init()
    game = Reversi(width=800, height=600)
    game.screen = pygame.display.set_mode(game.get_screen_dims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(30)
        game.step(dt)
        pygame.display.update()