import numpy as np
import random

# p_table = np.array([[1/120] * 120 for _ in range(16)])
# q_table = np.random.randint(1, 100, (16, 120))

# np.save("q.npy", q_table)
# np.save("p.npy", p_table)

q_table = np.load("q.npy")
p_table = np.load("p.npy")

status = 0
q_select_line = q_table[status]
min_q_poss = np.where(q_select_line==np.min(q_select_line))[0]
min_q_pos = random.choice(min_q_poss)

print(q_table[status])
print(min_q_pos)