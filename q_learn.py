import numpy as np
import random
import math
import os

class QL(object):
    def __init__(self):
        self.action_table = [[0] * 3 for _ in range(120)]
        self.q_table = np.array([[1] * 120 for _ in range(16)])
        self.q0_table = self.q_table
        self.p_table = np.array([[1/120] * 120 for _ in range(16)])
        self.gen_action_table()
        self.beta = 0.6
        self.lr = 0.15
        self.gamma = 0.80
    
    #生成行为表
    def gen_action_table(self):
        index = 0
        for a in range(10, 25, 2):
            for b in range(10, 25, 2):
                for c in range(10, 25, 2):
                    for d in range(10, 25, 2):
                        if a + b + c + d == 70 - 16:
                            self.action_table[index] = [a, b, c]
                            index += 1
    
    #行为决策
    def select_action(self, status):
        p_select_line = self.p_table[status]
        q_select_line = self.q_table[status]
        min_q_poss = np.where(q_select_line==np.min(q_select_line))[0]
        min_q_pos = random.choice(min_q_poss)
        p_select_line[min_q_pos] += self.beta * (1 - p_select_line[min_q_pos])
        for i in range(0,120):
            if i != min_q_pos:
                p_select_line[i] -= self.beta * p_select_line[i]
        self.p_table[status] = p_select_line

        p_select_cumsum = np.cumsum(p_select_line)
        p_select_cumsum = np.insert(p_select_cumsum, 0, 0)
        random_float = random.random()

        #二分查找法查找随机浮点数对应行为
        a = 0
        b = 120
        while(a != b):
            c = math.ceil((a + b)/2)
            if random_float >= p_select_cumsum[c]:
                a = c
            else:
                b = c - 1

        return a

    #学习，更新Q表
    def learn(self, status, action, reward, status_):
        q_predict = self.q_table[status][action]
        q_target = reward + self.gamma * min(self.q_table[status_])
        self.q_table[status][action] = q_predict + self.lr*(q_target - q_predict)
    
    #返回核查阶段的行为值
    def check(self, status):
        q_select_line = self.q_table[status]
        min_q_poss = np.where(q_select_line==np.min(q_select_line))[0]
        min_q_pos = random.choice(min_q_poss)
        return min_q_pos

    #存储q表，p表
    def save_data(self):
        np.save("q.npy", self.q_table)
        np.save("p.npy", self.p_table)
        if(os.path.exists("Q.xls")):
            os.remove("Q.xls")
        output = open("Q.xls", 'w', encoding='utf-8')

        for i in range(len(self.q_table)):
            for j in range(len(self.q_table[i])):
                output.write(str(self.q_table[i][j]))
                output.write('\t')

            output.write('\n')

        output.close() 
        print("Have save Q table to file.")
    
    #读取q表，p表
    def load_data(self):
        if os.path.exists("q.npy"):
            try:
                self.q_table = np.load("q.npy")
                print("已读取q表")
            except:
                print("读取q表有误，请删除后重试")
        
        else:
            print("q表不存在，使用初始q表")
        
        if os.path.exists("p.npy"):
            try:
                self.p_table = np.load("p.npy")
                print("已读取p表")
            except:
                print("读取p表有误，请删除后重试")
        
        else:
            print("p表不存在，使用初始p表")