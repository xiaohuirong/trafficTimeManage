from tokenize import Special
from q_learn import QL
from real import Real
from threading import Timer, Lock, Thread
import json
import time
from flask import Flask, jsonify
from flask_cors import *
from math import floor

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

lane_name = ["East_West_Straight", "East_West_Left", "South_North_Straight", "South_North_Left"]

color_set = [{lane_name[0]: "red", lane_name[1]: "red", lane_name[2]: "red", lane_name[3]: "yellow" },\
            {lane_name[0]: "green", lane_name[1]: "red", lane_name[2]: "red", lane_name[3]: "red" },\
            {lane_name[0]: "yellow", lane_name[1]: "red", lane_name[2]: "red", lane_name[3]: "red" },\
            {lane_name[0]: "red", lane_name[1]: "green", lane_name[2]: "red", lane_name[3]: "red" },\
            {lane_name[0]: "red", lane_name[1]: "yellow", lane_name[2]: "red", lane_name[3]: "red" },\
            {lane_name[0]: "red", lane_name[1]: "red", lane_name[2]: "green", lane_name[3]: "red" },\
            {lane_name[0]: "red", lane_name[1]: "red", lane_name[2]: "yellow", lane_name[3]: "red" },\
            {lane_name[0]: "red", lane_name[1]: "red", lane_name[2]: "red", lane_name[3]: "green" },\
            {lane_name[0]: "red", lane_name[1]: "red", lane_name[2]: "red", lane_name[3]: "red" }]




special_car = {lane_name[0]: False,\
                lane_name[1]: False,\
                lane_name[2]: False,\
                lane_name[3]: False } 

key_flow = {lane_name[0]: 180,\
                lane_name[1]: 250,\
                lane_name[2]: 320,\
                lane_name[3]: 280 }

light_time = {lane_name[0]: action[0],\
                lane_name[1]: action[1],\
                lane_name[2]: action[2],\
                lane_name[3]: action[3]}


people = {"Road1": 0, "Road2": 0, "Road3": 0, "Road4": 0}

cross_data = {"Key_Flow": key_flow,\
                "Special_Car": special_car,\
                "Light_Time": light_time,\
                "Light_Status": color_set[light_status],\
                "People": people }

app = Flask(__name__)
CORS(app, resources={ r"/*" : {"origins" : "*"}})
thread_lock = Lock()


@app.route('/api/info', methods=['GET'])
def get_tasks():
    global cross_data, thread_lock
    with thread_lock:
        send_data = cross_data
    return jsonify(send_data)

def reveive_people_data():
    global cross_data, thread_lock, people
    people_server = Real(4999)
    while True:
        people_data = people_server.get_data()
        people["Road1"] = people_data[0]
        people["Road2"] = people_data[1]
        people["Road3"] = people_data[2]
        people["Road4"] = people_data[3]
        with thread_lock:
            cross_data["People"] = people

def receive_and_save():
    global special_car, key_flow, light_time, lock, light_status, timer, thread_lock, cross_data, color_set, lane_name
    server = Real(5000)
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
                    with thread_lock:
                        cross_data["Light_Status"] = color_set[8]
                        cross_data["Light_Status"][lane_name[floor(((light_status + 7) % 8) / 2)]] = "yellow"
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    print(cross_data["Light_Status"])
                    timer = Timer(5, change_lightstatus, args=(1,))
                    timer.start()

        elif receive_data[5] :
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 3:
                    with thread_lock:
                        cross_data["Light_Status"] = color_set[8]
                        cross_data["Light_Status"][lane_name[floor(((light_status + 7) % 8) / 2)]] = "yellow"
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    print(cross_data["Light_Status"])
                    timer = Timer(5, change_lightstatus, args=(3,))
                    timer.start()

        elif receive_data[6] :
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 5:
                    with thread_lock:
                        cross_data["Light_Status"] = color_set[8]
                        cross_data["Light_Status"][lane_name[floor(((light_status + 7) % 8) / 2)]] = "yellow"
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    print(cross_data["Light_Status"])
                    timer = Timer(5, change_lightstatus, args=(5,))
                    timer.start()

        elif receive_data[7]:
            if lock == False:
                lock = True
                timer.cancel()
                if light_status != 7:
                    with thread_lock:
                        cross_data["Light_Status"] = color_set[8]
                        cross_data["Light_Status"][lane_name[floor(((light_status + 7) % 8) / 2)]] = "yellow"
                    light_status = 8
                    print("-----------------------------------")
                    print("light_status: %d" % light_status)
                    print("interval: 3")
                    print(cross_data["Light_Status"])
                    timer = Timer(5, change_lightstatus, args=(7,))
                    timer.start()

        else:
            if lock and light_status != 8:
                lock = False
                light_control()
                
        
        special_car[lane_name[0]] = receive_data[4]
        special_car[lane_name[1]] = receive_data[5]
        special_car[lane_name[2]] = receive_data[6]
        special_car[lane_name[3]] = receive_data[7]

        key_flow[lane_name[0]] = receive_data[0]
        key_flow[lane_name[1]] = receive_data[1]
        key_flow[lane_name[2]] = receive_data[2]
        key_flow[lane_name[3]] = receive_data[3]

        status_list= [0]*4
        for i in range(0,4):
            if receive_data[i] > 300 :
                status_list[i] = 1
            else :
                status_list[i] = 0
        status = 8*status_list[0] + 4*status_list[1] + 2*status_list[2] + status_list[3]
        

        action_index = ql.check(status)
        action = ql.action_table[action_index]
        action.append(54-sum(action))
        
        light_time = {lane_name[0]: action[0],\
                lane_name[1]: action[1],\
                lane_name[2]: action[2],\
                lane_name[3]: action[3]}

        with thread_lock:
            cross_data["Key_Flow"] = key_flow
            cross_data["Special_Car"] = special_car
            cross_data["Light_Time"] = light_time 
        
        

        # print(cross_data)
        # json_data = json.dumps(cross_data, indent=4)

        # with open('cross_data.json', 'w') as json_file:
        #     json_file.write(json_data)
        
def change_lightstatus(light_status_):
    global light_status, cross_data, color_set
    light_status = light_status_
    with thread_lock:
        cross_data["Light_Status"] = color_set[light_status]
    print("-----------------------------------")
    print("light_status: %d" % light_status)
    print(cross_data["Light_Status"])

def timer_func():
    global light_status
    light_status  =  (light_status + 1) % 8
 
    light_control()

def light_control():
    global special_car, key_flow, light_time, lock, light_status, timer, cross_data, color_set

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
    
    with thread_lock:
        cross_data["Light_Status"] = color_set[light_status]

    print("-----------------------------------")
    print("light_status: %d" % light_status)
    print("interval: %d" % interval)
    print(cross_data["Light_Status"])
    
    timer = Timer(interval, timer_func)
    timer.start()
    
    

if __name__=='__main__':
    light_control()
    
    t = Thread(target=receive_and_save)
    t.daemon = True
    t.start()

    t2 = Thread(target=reveive_people_data)
    t2.daemon = True
    t2.start()

    app.run(host="0.0.0.0", port=5001)
