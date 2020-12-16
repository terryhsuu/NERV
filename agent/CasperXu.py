from random import *
import pygame
import sys
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION

class BaseAgent():
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):

        self.color = color
        self.rows_n = rows_n
        self.cols_n = cols_n
        self.block_len = 0.8 * min(height, width)/cols_n
        self.col_offset = (width - height)/2 + 0.1 * min(height, width) + 0.5 * self.block_len
        self.row_offset = 0.1 * min(height, width) + 0.5 * self.block_len
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.side_length = min(width, height)
        self.top_left = (0,0)
        self.actions = self._init_action_set()
        self.status = {i:0 for i in range(64)}
        self.cur_player = -1
        self.enum = {}
        count =0
        for i in self.rows:
            for j in self.cols:
                self.enum[i+j] = count
                count+=1
        self.rev_enum = {y:x for x,y in self.enum.items()}
        

    def step(self, reward, obs):
        """
        Parameters
        ----------
        reward : dict
            current_score - previous_score
            
            key: -1(black), 1(white)
            value: numbers
            
        obs    :  dict 
            board status

            key: int 0 ~ 63
            value: [-1, 0 ,1]
                    -1 : black
                     0 : empty
                     1 : white

        Returns
        -------
        tuple:
            (x, y) represents position, where (0, 0) mean top left. 
                x: go right
                y: go down
        event_type:
            non human agent uses pygame.USEREVENT
        """

        raise NotImplementError("You didn't finish your step function. Please override step function of BaseAgent!")
    

class MyAgent(BaseAgent):        
    def _init_action_set(self): 
        actions = {}
        for i, row in enumerate(self.rows):
            for j , col in enumerate(self.cols):
                x = 0.1 * self.side_length + 0.8 * (j+0.5) / len(self.cols) * self.side_length
                y = 0.1 * self.side_length + 0.8 * (i+0.5) / len(self.rows) * self.side_length
                actions[row+col] = tuple([sum(i) for i in zip(self.top_left, (x, y))])
        return actions
    
    def _is_available(self, label):
        status = self.get_game_state()
        if status[self.enum[label]] != 0  : return False 
        if self._check_around(label): return True
        return False

    def _check_around(self, label):
        is_avail = False
        status = self.get_game_state()
        row = int(self.enum[label] // 8)
        col = int(self.enum[label] % 8)
        for i in range(-1, 2):
            if row+i < 0 or row+i >= 8: continue
            for j in range(-1, 2):
                if col+j < 0 or col+j >= 8: continue
                label = self.rows[row+i] + self.cols[col+j]
                if status[self.enum[label]] == -1 * self.cur_player: #周圍有沒有白棋
                    if self._check_direction(row, col, i, j):
                        is_avail = True
        return is_avail

    def _check_direction(self, row, col, dx, dy): 
        status = self.get_game_state()
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < 8 and 0 <= col+y[-1] < 8:
            label = self.rows[row+x[-1]] + self.cols[col+y[-1]]
            if status[self.enum[label]] == 0:
                break
            if status[self.enum[label]] == self.cur_player:
                return True

            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return False

    def _get_available_actions(self):
        avail = []
        for row in self.rows:
            for col in self.cols:
                if self._is_available(row+col):
                    avail.append(row+col)  
        return avail

    def get_game_state(self):
        return self.status

    def how_close_to_edge(self,label):
        edge = {0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,23,31,39,47,55,57,58,59,60,61,62,63}
        degree = 63
        for i in edge:
            if degree > abs(self.enum[label]-i):
                degree = abs(self.enum[label]-i)
                if degree == 0: break
        return degree #int

    def check_again(self,x, y, dx, dy):
        status = self.get_game_state()
        while 0 <= x+dx <8 and 0 <= y+dy < 8:
            label = self.rows[x+dx] + self.cols[y+dy]
            if status[self.enum[label]] == 0:
                return True
            elif status[self.enum[label]] == self.cur_player:
                x += dx
                y += dy
            else:
                return False                 
    
    def check_if_safe(self, label:str):
        status = self.get_game_state()
        row = int(self.enum[label] // 8)
        col = int(self.enum[label] % 8)
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                x,y = row+dx, col+dy
                while 0 <= x < 8 and 0 <= y < 8:
                    label_2 = self.rows[x] + self.cols[y]
                    if status[self.enum[label_2]] == 0:
                        break
                    elif status[self.enum[label_2]] == -self.cur_player:
                        amount = 0
                        while 0 <= x+dx < 8 and 0 <= y+dy < 8:
                            amount += 1; x += dx; y += dy
                            if status[self.enum[self.rows[x]+self.cols[y]]] == 0: break
                            elif status[self.enum[self.rows[x]+self.cols[y]]] == self.cur_player:
                                if  self.check_again(x, y, dx, dy):
                                    count += amount; break
                                else : count -= (amount+2); break
                    else: break
        if count >= 0: return True 
        else : return False 
    
    def if_give_corner(self, pos:int):
        for i in [0,7,56,63]:
            if abs(i-pos)==1:return False
        return True
        
    def if_corner(self, avail_act):
        for pos in  [0,7,56,63]:
            if pos in avail_act:
                return pos 
        return -1
    
    def eat_amount(self, pos):
        status = self.get_game_state()
        count = 0
        valid_step = [1, -1, 8, -8, 7, -7, 9, -9]
        for d in valid_step:
            temp_count = 0
            total_d = d 
            while 0 <= pos+total_d <=63:
                if status[pos+total_d] == -self.cur_player:
                    temp_count += 1
                    total_d += d
                elif status[pos+total_d] == self.cur_player:
                    count += temp_count
                    break
                elif status[pos+total_d] == 0:
                    break
                elif status[pos+total_d] == 2:
                    break
        return count


    def step(self, reward, obs):
        '''
        status(obs) :  dict     (key:0~63, value:-1,0,1)
        actions_dict : dict     (key:label, value:abs_pos in board)
        actions :      list     (label)
        avail_step :   list     (label)
        '''
        
        self.status = obs
        action_dict = self._init_action_set()
        avail_step =  self._get_available_actions()
        avail_step2 = [self.enum[i] for i in avail_step]
        
        
        if self.if_corner(avail_step2) == 0  :
            return (action_dict[self.rev_enum[self.if_corner(avail_step2)]],pygame.USEREVENT)
        
        good_choose = []
        for label in avail_step:    
            degree = self.how_close_to_edge(label)
            if degree == 0 or degree== 1  and self.if_give_corner(self.enum[label]) and self.check_if_safe(label):
                good_choose.append(self.enum[label])
        
        amount = {i:self.eat_amount(i) for i in good_choose}
        
        maxi = (0,0)
        
        for i in amount.items():
            if i[1] >= maxi[1]:
                maxi = i
        if maxi != (0,0):
            return (action_dict[self.rev_enum[maxi[0]]], pygame.USEREVENT)
        
        if avail_step != []:
            not_bad = []
            for i in avail_step:
                if self.if_give_corner(self.enum[i]):
                    not_bad.append(i)
            if not_bad != []:
                return (action_dict[sample(not_bad,1)[0]], pygame.USEREVENT)
            else:return (action_dict[sample(avail_step,1)[0]], pygame.USEREVENT)
        else: return None 


