def check_if_safe(self,label):
    status = self.get_game_state()
    pos = self.enum[label]
    valid_step = [1, -1, 8, -8, 7, -7, 9, -9]
    
    for i in valid_step:
        pos_ = pos
        count = 0 
        while 0 <= pos_ + i <= 63:
            pos_+=i
            if status[pos_] == self.cur_player:
                continue
            elif status[pos_] == -self.cur_player:
                amount = 0
                while 0 <= pos_+i <=63:
                    amount += 1
                    pos_ += i
                    if status[pos_] == self.cur_player:
                        if check_again(pos_, i):
                            count += amount
                        else: 
                            count -= (amount+2)
                    elif status[pos_] == -self.cur_player:
                        continue
                    else:
                        break
            else: break
                
def check_again(self, pos):
    status = self.get_game_state()
    while 0 <= pos+i <= 63:
        pos += i
        if status[pos] == self.cur_player:
            continue
        elif status[pos] == -self.cur_player:
            return True
        else:
            break
    return False


def check_again1(self,x, y, dx, dy):
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

def check_if_safe1(self, label:str):
    status = self.get_game_state()
    row = int(self.enum[label] // 8)
    col = int(self.enum[label] % 8)
    count = 0
    for dx in range(-1,2):
        for dy in range(-1,2):
            x,y = row+dx, col+dy
            while 0 <= x < 8 and 0 <= y < 8:
                label_2 = self.rows[x] + self.cols[y]
                if status[self.enum[label_2]] == -self.cur_player:
                    amount = 0
                    while 0 <= x+dx < 8 and 0 <= y+dy < 8:
                        print(x+dx, y+dy)
                        amount += 1; x += dx; y += dy
                        if status[self.enum[self.rows[x]+self.cols[y]]] == self.cur_player:
                            if  self.check_again(x, y, dx, dy):
                                count += amount
                                break
                            else : 
                                count -= (amount+2);
                                break
                        else:break
                else: break
    if count >= 0: return True 
    else : return False 