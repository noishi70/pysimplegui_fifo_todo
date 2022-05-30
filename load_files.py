import os
import pickle as pk


def load_files(filepath, taskpath, donepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    if os.path.exists(taskpath):
        tasks = pk.load(open(taskpath, "rb"))
    else:
        tasks = ["task_1", "task_2", "task_3"]

    if os.path.exists(donepath):
        done = pk.load(open(donepath, "rb"))
    else:
        done = ["done_1", "done_2", "done_3"]

    return tasks, done
