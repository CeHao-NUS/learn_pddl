from diffusion import GaussianDiffusion
from temporal import TemporalUnet
from learn_pddl.datasets.bitdataset import BitDataset

from utils.training import Trainer

bit_length = 16
horizon = 64


dataset = BitDataset(text_data_dir='datasets/dataset.txt', n_bits=bit_length, horizon=horizon)
model = TemporalUnet(horizon=horizon, transition_dim=bit_length, cond_dim=bit_length)
diffusion  =GaussianDiffusion(model, horizon=horizon, observation_dim=bit_length, action_dim=0)


trainer = Trainer(diffusion_model=diffusion, dataset=dataset, renderer=None)