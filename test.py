class test:
    def __init__(self, status, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
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
        # self.actions = self._init_action_set()
        self.status = status
        self.cur_player = -1
        self.enum = {}
        count =0
        for i in self.rows:
            for j in self.cols:
                self.enum[i+j] = count
                count+=1
        self.rev_enum = {y:x for x,y in self.enum.items()}

    def if_give_corner2(self,label):
        status = self.status
        # print(self.cur_player)
        status[self.enum[label]] = self.cur_player
        self.cur_player = -self.cur_player
        avail = self._get_available_actions()
        status[self.enum[label]] = 0
        self.cur_player = -self.cur_player
        for i in [0, 7, 56, 63]:
            if self.rev_enum[i] in avail:
                return False
        return True
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
    def predict(self, label):
        status = self.get_game_state()
        count = 0
        pos = self.enum[label]
        valid_step = [1, -1, 8, -8, 7, -7, 9, -9]
        color_change = []
        for d in valid_step:
            temp_count = 0
            total_d = d
            path = []
            while 0 <= pos+total_d <=63:
                if status[pos+total_d] == -self.cur_player:
                    temp_count += 1
                    path.append(total_d)
                    total_d += d
                elif status[pos+total_d] == self.cur_player:
                    count += temp_count
                    for i in path:
                        status[pos+i] = self.cur_player
                        color_change.append(pos+i)
                    break
                else :
                    break
        return color_change

    def predict2(self,label):
        '''
        estimate how much enemy can eat
        '''
        status = self.get_game_state()
        status[self.enum[label]] = self.cur_player
        color_change = self.predict(label)
        self.cur_player = -self.cur_player
        avail = self._get_available_actions()
        if_ok = True
        for i in avail:
            if self.eat_amount(i) >= len(color_change):
                if_ok = False ; break
        self.cur_player = -self.cur_player
        status[self.enum[label]] = 0
        for i in color_change:
            status[i] = -self.cur_player
        return if_ok

    def eat_amount(self, label):
        status = self.get_game_state()
        count = 0
        pos = self.enum[label]
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
                else :
                    break
        return count
status = {
 0: 0,  1: 0,  2: 0,  3:-1,  4: 0,  5:-1,  6: 1,  7: 1, 
 8: 0,  9: 0, 10: 1, 11:-1, 12:-1, 13: 1, 14: 1, 15:-1, 
16: 0, 17: 0, 18: 0, 19:-1, 20: 1, 21: 1, 22: 1, 23: 1, 
24: 0, 25:-1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1, 31:-1, 
32: 0, 33: 0, 34: 1, 35: 1, 36: 1, 37: 1, 38: 0, 39:-1, 
40: 0, 41: 0, 42: 0, 43: 0, 44: 1, 45: 1, 46:-1, 47:-1, 
48: 0, 49: 0, 50: 0, 51: 0, 52: 1, 53:-1, 54:-1, 55:-1, 
56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0}

a = test(status = status)
# print(a._get_available_actions())
print(a.predict2('6D'))
# print(a.get_game_state())