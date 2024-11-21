import random

def generate_sequence_with_11_12(prob=0.3):
    """
    Generate a random sequence based on the rules, with numbers 11 and 12 added randomly.
    
    Args:
    - prob (float): The probability of inserting 11 or 12 between, at the beginning, or at the end (0 <= prob <= 1).
    
    Returns:
    - list: The generated sequence.
    """
    # Define the initial structure of the sequence
    base_sequence = [1, 2, (3, 4), 5, (6, 7), {8}, 9, 10]

    # Rule 1: Randomly decide the order of 3 and 4, keeping them between 2 and 5
    three_four = random.choice([(3, 4), (4, 3)])

    # Rule 2: Randomly decide the order of 6 and 7
    six_seven = random.choice([(6, 7), (7, 6)])

    # Rule 3: Place 8 in any position before 9 and 10
    # Create a list of the sequence without {8}
    sequence_without_eight = [1, 2, three_four, 5, six_seven, 9, 10]
    
    # Flatten the sequence (expand tuples into individual elements)
    flattened_sequence = []
    for item in sequence_without_eight:
        if isinstance(item, tuple):
            flattened_sequence.extend(item)
        else:
            flattened_sequence.append(item)
    
    # Insert 8 into a random position before 9
    eight_position = random.randint(0, len(flattened_sequence) - 2)  # -2 to ensure 8 is before 9 and 10
    flattened_sequence.insert(eight_position, 8)

    # Add 11 and 12 randomly at the beginning and end based on the probability
    final_sequence = []

    # Add at the beginning
    if random.random() < prob:
        final_sequence.append(random.choice([11, 12]))

    # Add 11 and 12 randomly between numbers based on the probability
    for i in range(len(flattened_sequence)):
        final_sequence.append(flattened_sequence[i])
        if i < len(flattened_sequence) - 1:  # Only add between numbers
            if random.random() < prob:  # Decide whether to add 11 or 12
                final_sequence.append(random.choice([11, 12]))

    # Add at the end
    if random.random() < prob:
        final_sequence.append(random.choice([11, 12]))

    return final_sequence