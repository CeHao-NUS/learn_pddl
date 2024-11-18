from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
import json
from datasets import Dataset

# Load maze dataset and only use train set
def load_maze_dataset(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    train_sequences = []
    # Only process training data
    # print dataset size
    print(f"Dataset size: {len(data['train'])}")
    for example in data['train']:
        start = example['start_coordinate']
        end = example['end_coordinate']
        state_sequence = example['state_sequence']
        
        # Format the sequence as: "Start: x y Target: x y Sequence: x y x y ..."
        sequence_text = f"Start: {start[0]} {start[1]} Target: {end[0]} {end[1]} Sequence: " + \
                       " ".join([f"{coord[0]} {coord[1]}" for coord in state_sequence])
        train_sequences.append(sequence_text)
    
    return train_sequences

# Load only training sequences
maze_sequences = load_maze_dataset("/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/datasets/maze/maze_dataset_12x12_fix_start_action_current_state.json")

# Initialize model and tokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(example):
    inputs = tokenizer(example["text"], padding="max_length", truncation=True, max_length=256)
    inputs["labels"] = inputs["input_ids"].copy()
    return inputs

# Create dataset from training sequences only
train_dataset = Dataset.from_dict({"text": maze_sequences}).map(
    tokenize_function, 
    remove_columns=["text"]
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results_fix_start",
    overwrite_output_dir=True,
    num_train_epochs=200,
    per_device_train_batch_size=16,
    save_steps=500,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=10,
    logging_strategy="steps",
    evaluation_strategy="no",
    prediction_loss_only=True,
)

# Initialize trainer with training dataset only
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("./saved_model_fix_start")
tokenizer.save_pretrained("./saved_model_fix_start")