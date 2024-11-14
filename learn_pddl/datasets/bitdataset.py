import numpy as np
from transformers import AutoTokenizer

from collections import namedtuple
import numpy as np
import torch
import pdb

Batch = namedtuple('Batch', 'trajectories conditions')

# Define int2bits and bits2int as before
def int2bits(x, n, out_dtype=None):
    """Convert an integer x in (...) into bits in (..., n)."""
    x = np.right_shift(np.expand_dims(x, -1), np.arange(n))
    x = np.mod(x, 2)
    if out_dtype and out_dtype != x.dtype:
        x = x.astype(out_dtype)
    return x

def bits2int(x, out_dtype):
    """Converts bits x in (..., n) into an integer in (...)."""
    x = x.astype(out_dtype)
    x = np.sum(x * (2 ** np.arange(x.shape[-1])), axis=-1)
    return x

def text_to_bits(text, tokenizer, n_bits=16):
    """Tokenize text and convert tokens to binary bits."""
    # Tokenize without special tokens
    tokens = tokenizer(text, add_special_tokens=False, return_tensors="np")["input_ids"].squeeze()
    # print('tokens:', tokens)
    bits = int2bits(tokens, n=n_bits, out_dtype=np.int32)
    return bits

def bits_to_text(bits, tokenizer, n_bits=16):
    """Convert binary bits back to text using tokenizer."""
    # Convert bits to token IDs
    token_ids = bits2int(bits, out_dtype=np.int32)
    
    # Decode token IDs to text, skip special tokens to ensure clean output
    text = tokenizer.decode(token_ids, skip_special_tokens=True)
    return text

from learn_pddl.datasets.load_fun import load_custom_texts
Batch = namedtuple('Batch', 'trajectories conditions')


class Normalizer:
    def normalize(self, text, type):
        pass

    def unnormalize(self, bits, type):
        # return bits_to_text(bits)
        pass

class BitDataset(torch.utils.data.Dataset):

    def __init__(self, text_data_dir, n_bits=16, horizon=64, observation_dim=16, action_dim=0):
        self.text_data = load_custom_texts(text_data_dir)
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.n_bits = n_bits
        self.bits =[text_to_bits(text, self.tokenizer, n_bits) for text in self.text_data]
        self.horizon = horizon

        self.observation_dim = observation_dim
        self.action_dim = action_dim

        self.normalizer = Normalizer()  

    def __len__(self):
        return len(self.bits)
    
    def get_conditions(self, observations):
        '''
            condition on current observation for planning
        '''
        return {0: observations[0]}
    
    def __getitem__(self, idx):
        observations = self.bits[idx][:self.horizon]
        # to float
        observations = observations.astype(np.float32)

        text = self.text_data[idx]
    
        conditions = self.get_conditions(observations)
        # trajectories = np.concatenate([actions, observations], axis=-1)
        trajectories = observations
        batch = Batch(trajectories, conditions)

        assert observations.shape == (32, 16)
        return batch
    
    def decode_bit2text(self, bits):
        return bits_to_text(bits, self.tokenizer, self.n_bits)


if __name__ == "__main__":

    file_dir = 'datasets/dataset.txt'
    dataset = BitDataset(file_dir)