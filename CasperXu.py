from base_agent import *
from useful_step import *
from random import *


class MyAgent(BaseAgent,UsefulStep):
    def __init__(self):
        super().__init__()
        super(BaseAgent, self).__init__()
        super(UsefulStep, self).__init__()
    
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
            return action_dict[self.rev_enum[self.if_corner(avail_step2)]]
        
        good_choose = []
        for label in avail_step:    
            degree = self.how_close_to_edge(label)
            if degree == 0 or degree== 1  and self.if_give_corner(self.enum[label]):
                good_choose.append(self.enum[label])
        
        amount = {i:self.eat_amount(i) for i in good_choose}
        
        maxi = (0,0)
        
        for i in amount.items():
            if i[1] >= maxi[1]:
                maxi = i
        if maxi != (0,0):
            return action_dict[self.rev_enum[maxi[0]]]
        
        if avail_step != []:
            return action_dict[sample(avail_step,1)[0]]
        else: return None

                
if __name__=='__main__':
    obs = { 0: 0,  1: 0,  2: 0,  3: 0,  4: 0,  5: 0,  6: 0,  7: 0, 
            8: 0,  9: 0, 10: 0, 11: 1, 12: 0, 13: 0, 14: 0, 15: 0, 
           16: 0, 17: 0, 18: 1, 19: 1, 20:-1, 21: 0, 22: 0, 23: 0, 
           24: 0, 25: 0, 26: 0, 27: 1, 28: 1, 29: 0, 30: 0, 31: 0, 
           32: 0, 33: 0, 34: 0, 35: 1, 36:-1, 37: 1, 38: 0, 39: 0, 
           40: 0, 41: 0, 42: 0, 43:-1, 44: 0, 45:-1, 46: 0, 47: 0, 
           48: 0, 49: 0, 50: 0, 51: 1, 52: 0, 53: 0, 54: 0, 55: 0, 
           56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}
    a = MyAgent()
    print(a.step({-1:3, 1:3}, obs))


                


            

            

             
        
        