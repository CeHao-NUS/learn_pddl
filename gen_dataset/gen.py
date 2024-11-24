
from create import get_state_traj

from tqdm import tqdm

def gen_fun1(traj):
    # ================================ convert to any format ========================

    # 1. (action, obj) 

    text = ""

    for key, value in traj[0]['s'].state_list.items():
        text += key + " " + value + " | "
    text += "\n"

    # for key, value in traj[-1]['s'].state_list.items():
    #     text += key + " " + value + " | "
    # text += "\n"

    length_actions = 0
    for traj_i in traj:
        actions = traj_i['a']
        length_actions += len(actions)

        action_text = ' '.join(' '.join(pair) for pair in actions)
        text += action_text 


    return text, length_actions


def gen_fun2(traj):
    # 2. (p1, p2)

    # 7 objects

    text = ""
    # text += "Task: "
    # for key, value in traj[0]['s'].state_list.items():
    #     text += key + " " + value 

    for key, value in traj[0]['s'].state_list.items():
        text += key + " " + value + "\n"

    
    length_actions = 0
    for traj_i in traj:
        actions = traj_i['a']
        length_actions += len(actions)

        for action in actions:
            text += action[0] + " " + action[1] + "\n"

    return text, length_actions



# ================================ generate dataset ========================


variance_prob = 0.5
num_traj = int(1e4)

# '''
# save text as txt



with open('dataset.txt', 'w') as f:

    for idx in tqdm(range(num_traj)):
        traj = get_state_traj(prob = variance_prob)
        text, length_action = gen_fun2(traj)

        f.write(text + "\n\n")

# '''

# ================================ generate dataset ========================
'''
lengths = []
for idx in tqdm(range(num_traj)):
    traj = get_state_traj(prob = variance_prob)
    text, length_action = gen_fun1(traj)
    lengths.append(length_action)

import numpy as np

print('min length is', np.min(lengths))
print('max length is', np.max(lengths))
print('mean length is', np.mean(lengths))
print('median length is', np.median(lengths))
print('mode length is', np.argmax(np.bincount(lengths)))
print('std length is', np.std(lengths))

# print them in a row
print(np.min(lengths), np.max(lengths), np.mean(lengths), np.median(lengths), np.std(lengths))

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
sns.histplot(lengths, kde=True)
plt.xlabel('Length of actions')
plt.ylabel('Frequency')
plt.title('Histogram of lengths of actions')
plt.savefig('histogram.png')

'''

