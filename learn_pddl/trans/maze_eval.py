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

def main():
    # Load model and tokenizer
    model_path = "/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/trans/saved_model_fix_start"
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model.to(device)
    
    # Load test cases from json file
    with open("/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/datasets/maze/maze_dataset_12x12_fix_start_action_current_state.json", 'r') as f:
        test_data = json.load(f)
    
    # Create results directory
    results_dir = "evaluation_results_fix_start"
    os.makedirs(results_dir, exist_ok=True)
    
    # Evaluate each test case
    results = []
    with open(os.path.join(results_dir, "evaluation_results.txt"), 'w') as f:
        # Print the total number of test cases in validation dataset
        f.write(f"Total number of test cases: {len(test_data['validation'])}\n")
        for idx, test_case in enumerate(test_data['validation']):
            start_pos = test_case['start_coordinate']
            target_pos = test_case['end_coordinate']
            maze = test_case['current_maze']
            
            result, generated_text = generate_and_evaluate_path(
                model, tokenizer, start_pos, target_pos, maze
            )
            results.append(result)
            
            # Write results to file
            f.write(f"\nTest Case {idx + 1}:\n")
            f.write(f"Start: {start_pos}, Target: {target_pos}\n")
            f.write(f"Generated Sequence:\n{parse_state_sequence(generated_text)[1]}\n\n")
            f.write("Generated Maze with Path:\n")
            f.write('\n'.join([' '.join(row) for row in result['maze_with_path']]) + "\n")
            f.write(f"Success: {result['success']}\n")
            if not result['success']:
                f.write(f"Failure Reason: {result['failure_reason']}\n")
            f.write(f"Path Length: {result['path_length']}\n")
            f.write("="*80 + "\n")
    
    # Calculate and print overall metrics
    success_rate = sum(1 for r in results if r['success']) / len(results)
    avg_path_length = np.mean([r['path_length'] for r in results])
    
    print(f"\nEvaluation Results:")
    print(f"Number of test cases: {len(results)}")
    print(f"Success Rate: {success_rate:.4f}")
    print(f"Average Path Length: {avg_path_length:.2f}")
    
    # Save metrics to file
    with open(os.path.join(results_dir, "metrics.txt"), 'w') as f:
        f.write(f"Number of test cases: {len(results)}\n")
        f.write(f"Success Rate: {success_rate:.4f}\n")
        f.write(f"Average Path Length: {avg_path_length:.2f}\n")

if __name__ == "__main__":
    main()