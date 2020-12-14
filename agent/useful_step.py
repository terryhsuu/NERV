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
        self.enum = {r+c:i+j*8 for j, c in enumerate(self.cols) for i, r in enumerate(self.rows)}
    
    def _init_action_set(self): 
        actions = {}
        for i, row in enumerate(self.rows):
            for j , col in enumerate(self.cols):
                x = 0.1 * self.side_length + 0.8 * (j+0.5) / 8 * self.side_length
                y = 0.1 * self.side_length + 0.8 * (i+0.5) / 8 * self.side_length
                actions[row+col] = tuple([sum(i) for i in zip(self.top_left, (x, y))])
        return actions

    def _is_available(self, label, flip=False):
        if self._check_around(label, flip):
            return True

    def _check_around(self, label, flip):
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
                    if self._check_direction(row, col, i, j, flip=flip):
                        is_avail = True
        return is_avail

    def _check_direction(self, row, col, dx, dy, flip): 
        '''
        沿著有白棋的方向看看末端有沒有黑棋
        有的話就更新status
        '''
        is_avail = False
        status = self.get_game_state()
        x, y = [dx], [dy]
        while 0 <= row+x[-1] < 8 and 0 <= col+y[-1] < 8:
            label = self.rows[row+x[-1]] + self.cols[col+y[-1]]
            if status[self.enum[label]] == 0:
                break
            if status[self.enum[label]] == self.cur_player:
                if flip:
                    for r, c in zip(x, y):
                        self.status.update(self.rows[row+r]+self.cols[col+c], self.cur_player)
                    is_avail = True
                    break
                else:
                    return True
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        return is_avail

    def _get_available_actions(self):
        avail = []
        for row in self.rows:
            for col in self.cols:
                if self._is_available(row+col):
                    avail.append(row+col)  
        return avail

    def get_game_state(self):
        return self.status

    def get_actions(self): 
        return self.actions

    def update(self, label, cur_player):
        '''
        update  status
        '''
        self.status[self.enum[label]] == -1*cur_player

    def how_close_to_edge(self, label):
        edge = {0,1,2,3,4,5,6,7,8,16,24,32,40,48,56,15,22,30,38,46,54,57,58,59,60,61,62,63}
        degree = 63
        for i in edge:
            if degree > abs(self.enum[label]-i):
                degree = abs(self.enum[label])
                if degree == 0: break
        return degree

    def check_if_safe(self, label):
        is_safe = True
        status = self.get_game_state()
        row = int(self.enum[label] // 8)
        col = int(self.enum[label] % 8)
        for dx in range(-1,2):
            for dy in range(-1,2):
                x, y = dx, dy
                while 0 <= row+x < 8 and 0 <= col+y < 8:
                    label_2 = self.rows[row+x] + self.cols[col+y]
                    if status[self.enum[label_2]] == 0:
                        break
                    if status[self.enum[label_2]] == -self.cur_player:
                        while 0 <= row-x-dx < 8 and 0 <= col-y-dy < 8:
                            x = x - dx
                            y = y - dy
                            if status[self.enum[self.rows[x]+self.cols[y]]] == 0:
                                is_safe = False
                                break
        return is_safe
        
    def if_corner(self, avail_act):
        for i in  [0,7,56,63]:
            if i in avail_act:
                return i
        return False
    

        


