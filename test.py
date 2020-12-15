class test:
    def __init__(self):
        self.status ={ 0: 0,  1: 0,  2: 0,  3: 0,  4: 0,  5: 0,  6: 0,  7: 0, 
                       8: 1,  9: 1, 10: 1, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 
                      16: 1, 17: 0, 18: 1, 19:-1, 20:-1, 21: 0, 22: 0, 23: 0, 
                      24: 1, 25: 0, 26:-1, 27: 1, 28: 1, 29: 0, 30: 0, 31: 0, 
                      32: 1, 33: 0, 34: 0, 35: 1, 36:-1, 37: 1, 38: 0, 39: 0, 
                      40:-1, 41: 0, 42: 0, 43:-1, 44: 0, 45: 0, 46: 0, 47: 0, 
                      48: 0, 49: 0, 50: 0, 51: 1, 52: 0, 53: 0, 54: 0, 55: 0, 
                      56: 0, 57: 0, 58: 0, 59: 1, 60: 0, 61: 0, 62: 0, 63: 0}
        self.rows = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.cur_player = -1
        self.enum = {}
        count =0
        for i in self.rows:
            for j in self.cols:
                self.enum[i+j] = count
                count+=1
        self.rev_enum = {y:x for x,y in self.enum.items()}
        
    def get_game_state(self):
        return self.status

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
   
    def check_if_safe(self, label):
        status = self.get_game_state()
        row = int(self.enum[label] // 8)
        col = int(self.enum[label] % 8)
        count = 0
        if status[self.enum[label]] == 1 or status[self.enum[label]] == -1:
            return False
        for dx in range(-1,2):
            for dy in range(-1,2):
                x,y = row+dx, col+dy
                while 0 <= x < 8 and 0 <= y < 8:
                    label_2 = self.rows[x] + self.cols[y]
                    if status[self.enum[label_2]] == 0 : break
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


a = test()
print(a.check_if_safe('2D'))

#  0: 0,  1: 0,  2: 0,  3: 0,  4: 0,  5: 0,  6: 0,  7: 0, 
#  8: 1,  9: 1, 10: 1, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 
# 16: 1, 17: 0, 18: 1, 19:-1, 20:-1, 21: 0, 22: 0, 23: 0, 
# 24: 1, 25: 0, 26:-1, 27: 1, 28: 1, 29: 0, 30: 0, 31: 0, 
# 32: 1, 33: 0, 34: 0, 35: 1, 36:-1, 37: 1, 38: 0, 39: 0, 
# 40:-1, 41: 0, 42: 0, 43:-1, 44: 0, 45: 0, 46: 0, 47: 0, 
# 48: 0, 49: 0, 50: 0, 51: 1, 52: 0, 53: 0, 54: 0, 55: 0, 
# 56: 0, 57: 0, 58: 0, 59: 1, 60: 0, 61: 0, 62: 0, 63: 0