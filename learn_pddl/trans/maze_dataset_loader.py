import json
import os
from typing import List, Tuple

def load_maze_dataset(file_path: str) -> List[str]:
    """
    Loads maze coordinate sequences from a JSON file and formats them for the transformer.
    Returns list of strings where each string is a sequence of coordinates.
    """
    # Read JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    sequences = []
    
    # Process both training and validation data if available
    for split in ['train', 'validation']:
        if split in data:
            for example in data[split]:
                # Get start and end coordinates
                start = example['start_coordinate']
                end = example['end_coordinate']
                
                # Get state sequence
                state_sequence = example['state_sequence']
                
                # Format prompt with start and target
                prompt = f"Start: {start[0]} {start[1]} Target: {end[0]} {end[1]}"
                
                # Format state sequence as space-separated numbers
                sequence = " ".join([f"{state[0]} {state[1]}" for state in state_sequence])
                
                # Combine prompt and sequence
                full_sequence = f"{prompt} Sequence: {sequence}"
                sequences.append(full_sequence)
    
    return sequences

def format_state_sequence(sequence: List[Tuple[int, int]]) -> str:
    """
    Formats a state sequence into a space-separated string of numbers.
    """
    return " ".join([f"{x} {y}" for x, y in sequence])