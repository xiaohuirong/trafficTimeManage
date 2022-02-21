from q_learn import QL
from env import Cross
import numpy as np
import os

ql = QL()
ql.load_data()
path = os.getcwd()
inp_file = path + "\\vissim\\dan.inp"
ini_file = path + "\\vissim\\vissim.ini"
cross = Cross(inp_file, ini_file)
cross.simulation_config(40, 0, 3600)
cross.reset()
cycletime = cross.cycletime
#东左转，东直行，西直行，西左转，北直行，北左转，南直行，南左转
vehicle_inputs = np.array([244, 198, 268, 216, 132, 210, 272, 152])
cross.set_vehicle_input(vehicle_inputs)

for episolon in range(10):
    status = 0
    delay = 0
    print("episolon=%d" % episolon)

    for i in range(50):
        action = ql.select_action(status)
        [status_, reward] = cross.env_interface(70, ql.action_table[action])
        ql.learn(status, action, reward, status_)
        status = status_
        delay += cross.get_delay(cross.current_time)
    
    print("Total delay : %f s" % delay)
    cross.reset()
    print('-----------')
print("Learning is OK!")
ql.save_data()


print('\n-------------------')
print('Checking starts')


delay = 0
for i in range(50):
    cross.env_interface(70, [13, 13, 13])
    delay += cross.get_delay(cross.current_time)
print("Total delay before : %f s" % delay)

cross.reset()
delay = 0
status = 0
for i in range(50):
    action = ql.check(status)
    [status, reward] = cross.env_interface(70, ql.action_table[action])
    delay += cross.get_delay(cross.current_time)
print("Total delay after : %f s" % delay)




