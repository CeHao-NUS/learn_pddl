from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import json
import numpy as np

def evaluate_state_sequence(generated_states, start_pos, target_pos, maze):
    """
    Evaluate the generated state sequence.
    
    Args:
        generated_states: List of [row, col] coordinates
        start_pos: Starting position [row, col]
        target_pos: Target position [row, col]
        maze: Original maze layout
    
    Returns:
        dict containing evaluation results
    """
    # Convert string maze to 2D list if needed
    if isinstance(maze, str):
        maze = [list(row.split()) for row in maze.strip().split('\n')]
    
    # Validate starting position
    if list(generated_states[0]) != list(start_pos):
        return {
            'success': False,
            'failure_reason': f'Invalid start position. Expected {start_pos}, got {generated_states[0]}',
            'path_length': 0,
            'path': generated_states,
            'maze_with_path': maze
        }
    
    # Validate path
    path_length = 0
    current_maze = [row[:] for row in maze]  # Create a copy of the maze
    
    for i in range(len(generated_states) - 1):
        curr_pos = generated_states[i]
        next_pos = generated_states[i + 1]
        
        # Check if positions are adjacent
        row_diff = abs(next_pos[0] - curr_pos[0])
        col_diff = abs(next_pos[1] - curr_pos[1])
        
        # Position should either be same or adjacent
        valid_move = (row_diff == 0 and col_diff <= 1) or (row_diff <= 1 and col_diff == 0)
        
        if not valid_move:
            return {
                'success': False,
                'failure_reason': f'Invalid move from {curr_pos} to {next_pos}',
                'path_length': path_length,
                'path': generated_states,
                'maze_with_path': current_maze
            }
        
        # Check if hit wall
        if maze[next_pos[0]][next_pos[1]] == '#':
            return {
                'success': False,
                'failure_reason': f'Hit wall at position {next_pos}',
                'path_length': path_length,
                'path': generated_states,
                'maze_with_path': current_maze
            }
        
        # Valid move, mark path
        if next_pos != curr_pos:  # Only count actual moves
            path_length += 1
            if maze[next_pos[0]][next_pos[1]] == 'O':  # Only mark empty spaces
                current_maze[next_pos[0]][next_pos[1]] = 'X'
    
    # Check if reached target
    if list(generated_states[-1]) == list(target_pos):
        return {
            'success': True,
            'failure_reason': None,
            'path_length': path_length,
            'path': generated_states,
            'maze_with_path': current_maze
        }
    else:
        return {
            'success': False,
            'failure_reason': 'Did not reach target',
            'path_length': path_length,
            'path': generated_states,
            'maze_with_path': current_maze
        }



def generate_and_evaluate_path(model, tokenizer, start_pos, target_pos, maze, max_length=100, temperature=0.7):
    """
    Generate a path and evaluate it using the transformer model.
    """
    device = next(model.parameters()).device
    
    # Create prompt
    prompt = f"Start: {start_pos[0]} {start_pos[1]} Target: {target_pos[0]} {target_pos[1]} Sequence:"
    
    # Generate sequence
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        do_sample=True,
        temperature=temperature,
        top_p=0.95,
        pad_token_id=tokenizer.pad_token_id
    )
    
    # Decode and parse the generated sequence
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    generated_states = parse_state_sequence(generated_text)[0]
    
    if generated_states is None:
        return {
            'success': False,
            'failure_reason': 'Failed to parse generated sequence',
            'path_length': 0,
            'path': [],
            'maze_with_path': maze
        }, generated_text
    
    # Evaluate the generated path
    result = evaluate_state_sequence(generated_states, start_pos, target_pos, maze)
    return result, generated_text

def parse_state_sequence(text):
    """
    Parse and format state sequence from "1 2 2 2" to "(1,2) -> (2,2)"
    """
    parts = text.split('Sequence:')
    if len(parts) != 2:
        return None
        
    # Get just the sequence numbers
    sequence_part = parts[1].strip()
    numbers = [int(num) for num in sequence_part.split()]
    
    # Convert to coordinate pairs with formatting
    states = []
    formatted_sequence = []
    for i in range(0, len(numbers), 2):
        if i + 1 < len(numbers):
            states.append([numbers[i], numbers[i+1]])
            formatted_sequence.append(f"({numbers[i]},{numbers[i+1]})")
    
    return states, " -> ".join(formatted_sequence)

def test_single_path(start_pos, target_pos):
    """
    Test a single path with given start and target positions.
    """
    # Load model and tokenizer
    model_path = "/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/trans/saved_model_new"
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    # Load first maze from dataset
    maze_path = "/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/datasets/maze/maze_dataset_12x12_random_action_current_state.json"
    with open(maze_path, 'r') as f:
        maze = json.load(f)['validation'][0]['current_maze']
    
    # Generate and evaluate path
    result, generated_text = generate_and_evaluate_path(model, tokenizer, start_pos, target_pos, maze)
    
    # Print results
    print(f"\nPath from {start_pos} to {target_pos}:")
    print(f"Generated sequence: {parse_state_sequence(generated_text)[1]}")
    print("\nMaze with path:")
    print('\n'.join([' '.join(row) for row in result['maze_with_path']]))
    print(f"\nSuccess: {result['success']}")
    if not result['success']:
        print(f"Failure reason: {result['failure_reason']}")
    print(f"Path length: {result['path_length']}")


if __name__ == "__main__":

    start = [1, 1]
    target = [1, 2]
    test_single_path(start, target)