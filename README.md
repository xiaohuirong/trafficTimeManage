# Title

Optimize waiting time of cross using Q-Learning.

## Install

- install dependencies.

```shell
pip3 install pywin32
pip3 install numpy
```

## Usage

- run whole program.

```shell
python main.py
```

- use class Cross in env.py

```python
from env import Cross

#initializing instance
cross = Cross(inp_file, ini_file)
#initializing simulator
cross.simulation_config(40, 0, 3600)
cross.reset()
#set vehicle input
vehicle_inputs = np.array([244, 198, 268, 216, 132, 210, 272, 152])
cross.set_vehicle_input(vehicle_inputs)
#simulate a cycletime
[status_, reward] = cross.env_interface(70, ql.action_table[action])
```

- use class QL in q_learn.py

```python
from q_learn import QL

#initializing instance
ql = QL()
#load exsitent q and p table.
ql.load_data()
#learn
ql.learn(status, action, reward, status_)
#save q and p table
ql.save_data()
#make choice using the trained q table.
action = ql.check(status)
```



## Contributing

<a href="https://github.com/xiaohuirong"><img                   src="https://avatars.githubusercontent.com/u/69972645?s=40&v=4" /></a>

## License

MIT © Hoream
