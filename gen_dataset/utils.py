
# ========================= read the texts
def load_custom_texts(file_path, remove_newline=False):

    based_path = file_path

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
    return text.replace("\n", " ")

def convert_state_trajectory(text_data, no_first_line=True):
    # 1. first row is task description
    # 2. the rest are steps

    # create a dict, key is the task, value is the steps {task: [['close', 'infridge'], ['open', 'onpan']]}
    task_dict = {}
    for idx, texts in enumerate(text_data):
        lines = texts.strip().split("\n")
        task = f"task_{idx}"
        steps = lines
        task_dict[task] = []

        for i, step in enumerate(steps):

            step_no_index = step
            # seperate by whitespace 
            simplified_state = [item.split()[-1] for item in step_no_index.split(' ')]
            task_dict[task].append(simplified_state)

    return task_dict
