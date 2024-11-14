def load_custom_texts(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    tasks = []
    task = ""
    for line in lines:
        stripped_line = line.strip()
        
        # Check if the line starts a new task (assuming each new task starts with "Task x:")
        if stripped_line.startswith("Task"):
            if task:
                tasks.append(task.strip())  # Append the previous task to the list
            task = stripped_line  # Start a new task
        else:
            task += " " + stripped_line  # Append step to the current task

    if task:
        tasks.append(task.strip())  # Append the last task

    return tasks
