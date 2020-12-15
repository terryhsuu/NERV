from base_agent import*

class UsefulStep():
    def __init__(self, width=600, height=600):
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
    
    def if_give_corner(self, pos:int):
        for i in [0,7,56,63]:
            if abs(i-pos)==1:return False
        
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

if __name__=='__main__':
    a = UsefulStep()
    print(a.enum['2B'])