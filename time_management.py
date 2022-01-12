class Allowed_time:
    def __init__(self, words):
        self.F = ''
        self.T = ''
        self.D = ''
        self.I = ''
        self.S = ''
        try:
            for i in words:
                #print('~~',i)#######
                if i[0] == 'F':
                    self.F = i
                elif i[0] == 'T':
                    self.T = i
                elif i[0] == 'D':
                    self.D = i
                elif i[0] == 'I':
                    self.I = i
                elif i[0] == 'S':
                    self.S = i
        except:
            pass

    def print(self)->str:
        return f'''Từ: {self.F[1:]}, Đến: {self.T[1:]}, 
Ngắt sau mỗi: {self.D[1:]} phút, 
Thời gian nghỉ ngơi: {self.I[1:]} phút, 
Tổng thời gian sử dụng: {self.S[1:]} phút
'''
    def display(self):
        print(f'''{self.F} {self.T} {self.D} {self.I} {self.S}''')

def print_allowed_time(allowed_time:list)->list:
    all_allowed_time = []
    for i in allowed_time:
        all_allowed_time.append(i.print())
    return all_allowed_time

def display_allowed_time(allowed_time:list)->list:
    for i in allowed_time:
        i.display()

def read_file(file_name='Drive_folder/time.txt')->list:
    allowed_times = []
    with open(file_name,'r') as f:
        lines = f.readlines()
        f.close()
        for line in lines:
            words = line.split(' ')
            words[-1] = words[-1].replace('\n','')
            allowed_time = Allowed_time(words)
            allowed_times.append(allowed_time)
    return allowed_times

def write_file(allowed_time,file_name='Drive_folder/time.txt'):
    with open(file_name,'w') as f:
        for elem in allowed_time:
            f.write(f'{elem.F} {elem.T} {elem.D} {elem.I} {elem.S}\n')
        f.close()

def change_time(allowed_time,idx:int,F='',T='',D='',I='',S=''):
    if F:
        allowed_time[idx].F = 'F' + F
    else:
        allowed_time[idx].F = ''
    if T:
        allowed_time[idx].T = 'T' + T
    else:
        allowed_time[idx].T = ''
    if D:
        allowed_time[idx].D = 'D' + D
    else:
        allowed_time[idx].D = ''
    if I:
        allowed_time[idx].I = 'I' + I
    else:
        allowed_time[idx].I = ''
    if S:
        allowed_time[idx].S = 'S' + S
    else:
        allowed_time[idx].S = ''
    write_file(allowed_time)

def add_time(allowed_time:list, F='',T='',D='',I='',S=''):
    if F:
        F = 'F' + F
    if T:
        T = 'T' + T
    if D:
        D = 'D' + D
    if I:
        I = 'I' + I
    if S:
        S = 'S' + S
    allowed_time.append(Allowed_time([F,T,D,I,S]))
    write_file(allowed_time)