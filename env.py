from sqlite3 import enable_callback_tracebacks
import win32com.client as com

class Cross(object):
    def __init__(self, inp_file_path, ini_file_path):
        self.vissim_com = com.Dispatch("Vissim.Vissim")
        self.vissim_com.LoadNet(inp_file_path)
        self.vissim_com.LoadLayout(ini_file_path)
        self.sim = self.vissim_com.Simulation
        self.net = self.vissim_com.Net
        self.eval = self.vissim_com.Evaluation

        # refer to signal control
        self.signal_control = self.net.SignalControllers.GetSignalControllerByNumber(1) 
        self.cycletime =  self.signal_control.AttValue("CYCLETIME")
        self.light_group = []
        for i in range(1,5):
            self.light_group.append(self.signal_control.SignalGroups.GetSignalGroupByNumber(i))
        
        self.travel_time = []
        for i in range(1,9):
            self.travel_time.append(self.net.TravelTimes.GetTravelTimeByNumber(i))

        self.delay = self.net.Delays.GetDelayByNumber(1)

        self.flow = [0]*8
        self.key_flow = [0]*4
        self.current_time = 0

        self.vehicle_inputs = self.net.VehicleInputs
        self.vehicle_input = []
        for i in range(1,9):
            self.vehicle_input.append(self.vehicle_inputs.GetVehicleInputByNumber(i))

    # configure evalation to do

    #仿真参数设置
    def simulation_config(self, random_seed, runindex, period):
        self.sim.RandomSeed = random_seed
        self.sim.RunIndex = runindex
        self.sim.Period = period

    #仿真初始化
    def reset(self):
        self.sim.Stop()
        self.current_time = 0

    #持续仿真到结束
    def run_continue(self):
        self.sim.RunContinuous()
        #self.sim.Stop()
    
    #单步仿真
    def run_siglestep(self):
        self.sim.RunSingleStep()

    #仿真到某时刻
    def run_end_at(self, time):
        self.sim.BreakAt = time
        self.run_continue()
        # while(self.sim.AttValue("ELAPSEDTIME") < time):
        #     self.run_siglestep()
        
        self.current_time = self.sim.AttValue("ELAPSEDTIME")
        return self.current_time
        # self.sim.Stop()
    
    #获取交通流(只有单步仿真才能用)
    #current_time为选择时间点，time_length为该时间点所在时间段长度
    #东左转，东直行，西直行，西左转，北直行，北左转，南直行，南左转
    def get_flow(self, current_time, time_length):
        for  i in range(0,8):
            sigle_flow = self.travel_time[i].GetResult(current_time, "NVEHICLES", "", 0)
            sigle_flow = sigle_flow * 3600 / time_length
            self.flow[i] = sigle_flow
        
        return self.flow

    #获取关键流量
    def get_key_flow(self):
        self.key_flow[0] = self.flow[1] if self.flow[1] > self.flow[2] else self.flow[2]
        self.key_flow[1] = self.flow[0] if self.flow[0] > self.flow[3] else self.flow[3]
        self.key_flow[2] = self.flow[4] if self.flow[4] > self.flow[6] else self.flow[6]
        self.key_flow[3] = self.flow[5] if self.flow[5] > self.flow[7] else self.flow[7]
        return self.key_flow

    #设置信号灯时长
    def set_light_time(self, greentime1, greentime2, greentime3):
        self.light_group[0].SetAttValue('REDEND', 1)
        self.light_group[0].SetAttValue('GREENEND', greentime1 + 1) 
        self.light_group[1].SetAttValue('REDEND', greentime1 + 1 + 3)
        self.light_group[1].SetAttValue('GREENEND', greentime1 + 1 + 3 + greentime2) 
        self.light_group[2].SetAttValue('REDEND', greentime1 + 1 + 3 + greentime2 + 5)
        self.light_group[2].SetAttValue('GREENEND', greentime1 + 1 + 3 + greentime2 + 5 + greentime3)
        self.light_group[3].SetAttValue('REDEND', greentime1 + 1 + 3 + greentime2 + 5 + greentime3 + 3) 
        self.light_group[3].SetAttValue('GREENEND', self.cycletime - 5 + 1)

    #设置交通流输入
    def set_vehicle_input(self, inputs):
        for i in range(0,8):
            self.vehicle_input[i].SetAttValue('Volume', inputs[i])

    #获取延时
    def get_delay(self, current_time):
        return self.delay.GetResult(current_time, "DELAY", "", 0)       


    #环境与外界信息交换接口，输入行动与周期，输出奖励和下一阶段状态
    def env_interface(self, cycletime, action):
        self.set_light_time(action[0], action[1], action[2])
        self.run_end_at(self.current_time + cycletime)
        flow = self.get_flow(self.current_time, cycletime)
        key_flow = self.get_key_flow()
        status_ = [0]*4
        for i in range(0,4):
            if key_flow[i] > 300 :
                status_[i] = 1
            else :
                status_[i] = 0
        status_num = 8*status_[0] + 4*status_[1] + 2*status_[2] + status_[3]

        delay_time = self.get_delay(self.current_time)
        if delay_time <= 24:
            reward = 0
        elif delay_time <= 26:
            reward = 10
        elif delay_time <= 28:
            reward = 20
        elif delay_time <= 30:
            reward = 30
        elif delay_time <= 32:
            reward = 40
        else:
            reward = 50
        
        return [status_num, reward]
        
    
    #存储q表，p表
