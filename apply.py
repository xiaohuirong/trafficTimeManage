from q_learn import QL
from real import Real
from threading import Timer
import json
import time

ql = QL()
ql.load_data()

data = None
lock = 0
timer = None
lock = False

status = 0
light_status = 0

action_index = ql.check(status)
action = ql.action_table[action_index]
action.append(54-sum(action))




special_car = {"East West Straight": False,\
                "East West Left": False,\
                "South North Straight": False,\
                "South North Left": False } 

key_flow = {"East West Straight": 180,\
                "East West Left": 250,\
                "South North Straight": 320,\
                "South North Left": 280 }

light_time = {"East West Straight": action[0],\
                "East West Left": action[1],\
                "South North Straight": action[2],\
                "South North Left": action[3]}



def receive_and_save():
    global special_car, key_flow, light_time, lock, light_status, timer
    server = Real()
    while(1):
        receive_data = server.get_data()
        # time.sleep(5)
        # receive_data = [1, 1, 2, 0, 0, 0, 0, 0]
        # receive_data[5] = int(input())
        if receive_data[4] :
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 1:
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    timer = Timer(5, change_lightstatus, args=(1,))
                    timer.start()

        elif receive_data[5] :
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 3:
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    timer = Timer(5, change_lightstatus, args=(3,))
                    timer.start()

        elif receive_data[6] :
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 5:
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    timer = Timer(5, change_lightstatus, args=(5,))
                    timer.start()

        elif receive_data[7]:
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 7:
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    timer = Timer(5, change_lightstatus, args=(7,))
                    timer.start()

        else:
            if lock and light_status != 8:
                lock = False
                light_control()
                
        
        special_car["East West Straight"] = receive_data[4]
        special_car["East West Left"] = receive_data[5]
        special_car["South North Straight"] = receive_data[6]
        special_car["South North Left"] = receive_data[7]

        key_flow["East West Straight"] = receive_data[0]
        key_flow["East West Left"] = receive_data[1]
        key_flow["South North Straight"] = receive_data[2]
        key_flow["South North Left"] = receive_data[3]

        status_list= [0]*4
        for i in range(0,4):
            if key_flow[i] > 300 :
                status_list[i] = 1
            else :
                status_list[i] = 0
        status = 8*status_list[0] + 4*status_list[1] + 2*status_list[2] + status_list[3]
        

        action_index = ql.check(status)
        action = ql.action_table[action_index]
        action.append(54-sum(action))
        
        light_time = {"East West Straight": action[0],\
                "East West Left": action[1],\
                "South North Straight": action[2],\
                "South North Left": action[3]}

        cross_data = {"Key Flow": key_flow,\
                "Special Car": special_car,\
                "Light Time": light_time}
        
        

        print(cross_data)
        json_data = json.dumps(cross_data, indent=4)

        with open('cross_data.json', 'w') as json_file:
            json_file.write(json_data)
        
def change_lightstatus(light_status_):
    global light_status
    light_status = light_status_
    print("-----------------------------------")
    print("light_status: %d" % light_status)

def timer_func():
    global light_status
    light_status  =  (light_status + 1) % 8
    light_control()

def light_control():
    global special_car, key_flow, light_time, lock, light_status, timer

    if light_status == 0 or light_status == 4:
        interval = 5
    elif light_status == 1:
        interval = action[0]
    elif light_status == 2 or light_status == 6:
        interval = 3
    elif light_status == 3:
        interval = action[1]
    elif light_status == 5:
        interval = action[2]
    else: 
        interval = action[3]
    
    print("-----------------------------------")
    print("light_status: %d" % light_status)
    print("interval: %d" % interval)
    
    timer = Timer(interval, timer_func)
    timer.start()
    
    

if __name__=='__main__':
    light_control()
    while True:
        receive_and_save()
    


