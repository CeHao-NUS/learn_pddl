from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from datasets import Dataset

# Import the maze dataset loader
from maze_dataset_loader import load_maze_dataset

# Load maze sequences instead of custom texts
maze_sequences = load_maze_dataset("/home/users/cehao/Zhiwei/test_trans/learn_pddl/learn_pddl/datasets/maze/maze_dataset_12x12_random_action_current_state.json")

# Initialize the model and tokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(example):
    inputs = tokenizer(example["text"], padding="max_length", truncation=True, max_length=256)
    inputs["labels"] = inputs["input_ids"].copy()
    return inputs

# Convert maze sequences to dataset format and tokenize
dataset = Dataset.from_dict({"text": maze_sequences}).map(tokenize_function, remove_columns=["text"])
train_dataset = dataset

# Training arguments remain the same as before
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=10,
    per_device_train_batch_size=16,
    save_steps=100,
    save_total_limit=2,
    logging_dir='./logs',
    logging_steps=10,
    logging_strategy="steps",
    evaluation_strategy="no",
    prediction_loss_only=True,
)

# Initialize and train the model
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Train the model
trainer.train()

# Save the model
trainer.save_model("./saved_model")
tokenizer.save_pretrained("./saved_model")