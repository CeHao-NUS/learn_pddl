

import learn_pddl
import os

def load_custom_texts(file_path, remove_newline=True):

    based_path = os.path.join(os.path.dirname(learn_pddl.__file__),file_path)

    with open(based_path, 'r') as file:
        lines = file.readlines()

    texts = []
    text = ""
    for line in lines:
        if not text: # start a new line
            text = text + line
        else:
            if line == "\n":
                texts.append(text)
                text = ""
            else:
                text = text + line
    
    if remove_newline: 
        return [remove_next_line(text) for text in texts] 
    else:
        return texts

def remove_next_line(text):
    return text.replace("\n", "")


class StateTrajectory:
    def __init__(self, text):
        lines = text.strip().split("\n")
        self.task = lines[0]  # First line is the task description
        self.steps = lines[1:]  # Remaining lines are the steps
        self.simplified_states = self._simplify_states(self.steps)
    
    def _simplify_states(self, steps):
        # Simplify each step to remove object names and "|"
        simplified = []
        for step in steps:
            state = step.split(".")[1].strip()  # Extract the state after the step number
            simplified_state = " ".join([item.split()[-1] for item in state.split('|')])
            simplified.append(simplified_state)
        return simplified
    
    @property
    def generate_formatted_string_task(self):
        # Generate the formatted string
        formatted_string = f"{self.task}\n"
        for i, state in enumerate(self.simplified_states, start=1):
            formatted_string += f"{i}. {state}\n"
        return formatted_string

    def __str__(self):
        # Pretty-print the object details
        output = f"Task: {self.task}\n\nSteps:\n"
        output += "\n".join(self.steps)
        output += "\n\nSimplified States:\n"
        output += "\n".join(self.simplified_states)
        return output

if __name__ == "__main__":
    custom_texts = load_custom_texts("datasets/dataset.txt", remove_newline=False)
    # print(custom_texts)

    texts = ""
    for text in custom_texts:
        state_traj = StateTrajectory(text)
        # print(state_traj)
        # print(state_traj.generate_formatted_string_task)
        texts += state_traj.generate_formatted_string_task
        texts += "\n"
        # print("----" * 10)

    # save to new txt
    with open("dataset_simplified.txt", "w") as file:
        file.write(texts)