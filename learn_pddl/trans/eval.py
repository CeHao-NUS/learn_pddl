from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

import learn_pddl
import os

# Load the fine-tuned GPT-2 model and tokenizer
model_path = "./saved_model"
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load custom_texts from dataset.txt
from learn_pddl.datasets.load_fun import load_custom_texts
custom_texts = load_custom_texts(os.path.join(os.path.dirname(learn_pddl.__file__),"datasets/dataset.txt"))

# Ensure PAD token is set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    model.resize_token_embeddings(len(tokenizer))

def generate_follow_up_steps(prompt, max_length=1000, temperature=0.05, top_p=0.95):
    model.eval()
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    # Check if input_ids is empty
    if input_ids.numel() == 0:
        print(f"Empty input for prompt: {prompt}")
        return prompt  # Return prompt as-is if input_ids is empty

    try:
        # Generate follow-up steps
        outputs = model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            pad_token_id=tokenizer.pad_token_id
        )

        # Decode and return the generated steps following the prompt
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text
    except Exception as e:
        print(f"Error during generation for prompt '{prompt}': {e}")
        return prompt


# '''
# Evaluate the model by generating follow-up steps
for i, task in enumerate(custom_texts):
    # Use only the initial prompt part (first sentence)
    prompt = task.split('.')[0] + "."  # e.g., "Task 1: Move the robot to the charging station."
    generated_steps = generate_follow_up_steps(prompt)
    print(f"Input Prompt: {prompt}")
    print("\n")
    print(f"Generated Steps: {generated_steps}")
    print("\n")
    print(f"Ground Truth: {task}")
    print("----" * 10)
# '''

# prompt = 'Task 30: Make coffee.'
# print(generate_follow_up_steps(prompt))