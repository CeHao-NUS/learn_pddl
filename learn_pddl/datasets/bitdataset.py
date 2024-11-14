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

class BitDataset(torch.utils.data.Dataset):

    def __init__(self, text_data_dir, n_bits=16, horizon=64):
        self.text_data = load_custom_texts(text_data_dir)
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.n_bits = n_bits
        self.bits =[text_to_bits(text, self.tokenizer, n_bits) for text in self.text_data]
        self.horizon = horizon

    def __len__(self):
        return len(self.bits)
    
    def __getitem__(self, idx):
        return self.bits[idx][:self.horizon]
    
    def decode_bit2text(self, bits):
        return bits_to_text(bits, self.tokenizer, self.n_bits)


if __name__ == "__main__":

    file_dir = 'datasets/dataset.txt'
    dataset = BitDataset(file_dir)