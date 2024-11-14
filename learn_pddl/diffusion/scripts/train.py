from learn_pddl.diffusion.diffusion import GaussianDiffusion
from learn_pddl.diffusion.temporal import TemporalUnet
from learn_pddl.datasets.bitdataset import BitDataset

from learn_pddl.diffusion.utils.training import Trainer

import learn_pddl.diffusion.utils as utils

bit_length = 16
horizon = 32


dataset = BitDataset(text_data_dir='datasets/dataset.txt', n_bits=bit_length, horizon=horizon)
model = TemporalUnet(horizon=horizon, transition_dim=bit_length, cond_dim=bit_length).to('cuda:0')
diffusion  =GaussianDiffusion(model, horizon=horizon, observation_dim=bit_length, action_dim=0).to('cuda:0')


trainer = Trainer(diffusion_model=diffusion, dataset=dataset, renderer=None)

#-----------------------------------------------------------------------------#
#------------------------ test forward & backward pass -----------------------#
#-----------------------------------------------------------------------------#

utils.report_parameters(model)

print('Testing forward...', end=' ', flush=True)
batch = utils.batchify(dataset[0])
loss, _ = diffusion.loss(*batch)
loss.backward()
print('✓')


#-----------------------------------------------------------------------------#
#--------------------------------- main loop ---------------------------------#
#-----------------------------------------------------------------------------#

n_steps_per_epoch = 5
n_train_steps = 100

savepath = 'logs/diffusion'

n_epochs = int(n_train_steps // n_steps_per_epoch)

for i in range(n_epochs):
    print(f'Epoch {i} / {n_epochs} | {savepath}')
    trainer.train(n_train_steps=n_steps_per_epoch)
