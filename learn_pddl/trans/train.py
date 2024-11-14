from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
import torch
from datasets import Dataset

# Step 1: Define function to load custom texts from dataset.txt
from learn_pddl.datasets.load_fun import load_custom_texts
custom_texts = load_custom_texts("datasets/dataset.txt")

# Step 2: Initialize the GPT-2 model and tokenizer
model_name = "gpt2"  # Use GPT-2 model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # Use EOS token as padding token

# Step 3: Preprocess the data by tokenizing and setting labels
def tokenize_function(example):
    inputs = tokenizer(example["text"], padding="max_length", truncation=True, max_length=128)
    inputs["labels"] = inputs["input_ids"].copy()  # Set labels for causal language modeling
    return inputs

# Convert custom text data to dataset format and tokenize
dataset = Dataset.from_dict({"text": custom_texts}).map(tokenize_function, remove_columns=["text"])
train_dataset = dataset  # Use the full dataset for training

# Calculate save_steps based on the number of epochs and dataset size
num_epochs = 200
batch_size = 5
num_training_steps = (len(train_dataset) // batch_size) * num_epochs
save_every_n_epochs = 10
save_steps = num_training_steps // (num_epochs / save_every_n_epochs)

# Step 4: Set up training arguments, including logging strategy
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=num_epochs,
    per_device_train_batch_size=batch_size,
    save_steps=save_steps,
    save_total_limit=2,
    logging_dir='./logs',  # Directory to save logs
    logging_steps=10,      # Log training loss every 10 steps
    logging_strategy="steps",  # Log based on steps rather than epochs
    evaluation_strategy="no",  # Turn off evaluation to avoid using a validation set
    prediction_loss_only=True, # Only calculate the loss
)

# Step 5: Define a custom Trainer class to compute the loss if needed
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        device = model.module.device if hasattr(model, 'module') else model.device  # Handle DataParallel case
        inputs = {key: val.to(device) for key, val in inputs.items()}  # Move inputs to the device
        outputs = model(**inputs)
        loss = outputs.loss
        return (loss, outputs) if return_outputs else loss

# Step 6: Initialize the Trainer with the training dataset only
trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset
)

# Step 7: Train the model
trainer.train()

# Step 8: Save the trained model and tokenizer
trainer.save_model("./saved_model")  # Save model to directory "saved_model"
tokenizer.save_pretrained("./saved_model")  # Save tokenizer
