
from create import get_state_traj


# save text as txt

# with open('dataset.txt', 'w') as f:

    # for idx in range(10):
    #     text, length_action = get_state_traj()

        # f.write(text + "\n \n")

lengths = []
for idx in range(1000):
    text, length_action = get_state_traj()
    lengths.append(length_action)


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
sns.histplot(lengths, kde=True)
plt.xlabel('Length of actions')
plt.ylabel('Frequency')
plt.title('Histogram of lengths of actions')
plt.savefig('histogram.png')