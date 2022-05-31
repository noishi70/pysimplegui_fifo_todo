from multiprocessing.spawn import import_main_path
import PySimpleGUI as sg
import pickle as pk
import datetime
import requests
import load_files
import os
from copyreg import pickle
from genericpath import exists
from matplotlib.pyplot import flag
from send_line import send_line_notify


# フォントとテーマの設定
sg.set_options(font=("Times New Roman", 15))
sg.theme("DarkTeal5")

# ファイルパスの設定と読み込み
DIR_PATH = os.path.dirname(__file__)
os.chdir(DIR_PATH)

FILE_PATH = "./files/"
TASK_PATH = FILE_PATH + "tasks.pkl"
DONE_PATH = FILE_PATH + "done.pkl"
TOKEN_PATH = FILE_PATH + "linetoken.txt"
tasks, done = load_files.load_files(FILE_PATH, TASK_PATH, DONE_PATH)

if not os.path.exists(TOKEN_PATH):
    sg.popup_error("./file/linetoken.txt doesn't exist")
else:
    with open(TOKEN_PATH, mode="r") as f:
        token = f.read()

timer = 3600

# column作成
col_tasks = [
    [
        sg.Button("SET", key="-SET_TASK-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Edit", key="-EDIT_TASK-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Delete", key="-DEL_TASK-", button_color=("black", "DarkSalmon")),
    ],
    [sg.Text("Task List", font=("Times New Roman", 15))],
    [sg.Listbox(values=tasks, size=(30, 10), key="-TASKS-")],
]

col_doing = [
    [sg.Text("The Task in Progress", font=("Times New Roman", 15))],
    [
        sg.InputText("", key="-DOING_INPUT-", size=(30, 10)),
        sg.Button("DONE", key="-DONE_TASK-", button_color=("black", "PaleTurquoise1")),
    ],
    [
        sg.Text(
            datetime.timedelta(seconds=timer),
            key="-TIMER-",
            justification="c",
            size=(20),
            font=("Times New Roman", 20),
        )
    ],
]

col_done = [
    [
        sg.Button("REDO", key="-REDO_DONE-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Delete", key="-DEL_DONE-", button_color=("black", "DarkSalmon")),
        sg.Button("Clear", key="-CLEAR_DONE-", button_color=("black", "firebrick3")),
    ],
    [sg.Text("Done List", font=("Times New Roman", 15))],
    [sg.Listbox(values=done, size=(30, 10), key="-DONE-")],
]

# layoutの作成
layout = [
    [sg.Text("FIFO_TODO", font=("Times New Roman", 30))],
    [sg.Text("Handle tasks in order", font=("Times New Roman", 20))],
    [
        sg.InputText("Enter Your Task", key="-TASK_INPUT-", size=(30, 10)),
        sg.Button(button_text="Add", key="-ADD-", button_color=("black", "OliveDrab2")),
    ],
    [
        sg.Column(col_tasks),
        sg.Column(col_doing, pad=((0, 0), (0, 120))),
        sg.Column(col_done),
    ],
]

# window呼び出し
window = sg.Window("FIFO_TODO", layout, resizable=True)

index = None
flag_doing = False

while True:  # Event Loop
    event, values = window.Read(
        timeout=1000, timeout_key="-TIMEOUT-"
    )  # Event -> key, values -> item
    if event == "-TIMEOUT-":
        if flag_doing == True:
            timer -= 1
            window.find_element("-TIMER-").Update(
                value=datetime.timedelta(seconds=timer)
            )
            if timer == 0:  # timerが終わったらLINEで通知
                send_line_notify(token)
                timer = 3600
        else:
            pass
    if event == "-ADD-":  # taskを追加したとき
        if values["-TASK_INPUT-"] == "":  # 空の場合は追加しない
            sg.popup_ok("Input Your Task")
        else:
            if values["-TASK_INPUT-"] not in tasks:  # 重複するタスクは登録しない
                if index != None:
                    tasks.insert(index, values["-TASK_INPUT-"])
                    index = None
                else:
                    tasks.append(values["-TASK_INPUT-"])
                window.find_element("-TASKS-").Update(values=tasks)
                window.find_element("-ADD-").Update("Add")
                window.find_element("-TASK_INPUT-").Update(value="")
            else:
                sg.popup_ok("Registered tasks")

    elif event == "-SET_TASK-":
        if values["-TASKS-"] == []:  # 空の場合は追加しない
            sg.popup_ok("Not Selected")
        else:
            if values["-DOING_INPUT-"] == "":
                if tasks.index(values["-TASKS-"][0]) == 0:
                    tasks.remove(values["-TASKS-"][0])
                    window.find_element("-TASKS-").Update(values=tasks)
                    window.find_element("-DOING_INPUT-").Update(
                        value=values["-TASKS-"][0]
                    )
                    flag_doing = True
                else:
                    sg.popup_ok("Select the first task")
            else:
                sg.popup_ok("Finish the previous task")

    elif event == "-DONE_TASK-":  # taskをdoneしたとき
        if values["-DOING_INPUT-"] == "":  # 空の場合は追加しない
            sg.popup_ok("Set Your Task")
        else:
            done.append(values["-DOING_INPUT-"])
            window.find_element("-DONE-").Update(values=done)
            window.find_element("-DOING_INPUT-").Update(value="")
            flag_doing = False
            timer = 3600
            window.find_element("-TIMER-").Update(
                value=datetime.timedelta(seconds=timer)
            )

    elif event == "-DEL_TASK-":  # taskをdelしたとき
        if values["-TASKS-"] == []:  # 空の売位は追加しない
            sg.popup_ok("Not Selected")
        else:  # taskの消去
            tasks.remove(values["-TASKS-"][0])
            window.find_element("-TASKS-").Update(values=tasks)

    elif event == "-EDIT_TASK-":  # taskをeditしたとき
        if values["-TASKS-"] == []:  # 空の場合は警告
            sg.popup_ok("Not Selected")
        else:
            edit_val = values["-TASKS-"][0]  # inputウインドウに値を表示してボタンをsaveに変更
            index = tasks.index(edit_val)
            tasks.remove(values["-TASKS-"][0])
            window.find_element("-TASKS-").Update(values=tasks)
            window.find_element("-TASK_INPUT-").Update(value=edit_val)
            window.find_element("-ADD-").Update("Save")

    elif event == "-DEL_DONE-":  # doneをdelしたとき
        if values["-DONE-"] == []:  # 空場合は警告
            sg.popup_ok("Not Selected")
        else:
            done.remove(values["-DONE-"][0])
            window.find_element("-DONE-").Update(values=done)

    elif event == "-CLEAR_DONE-":  # doneをdelしたとき
        value_yes_or_no = sg.popup_yes_no("Clear Done Tasks")
        if value_yes_or_no == "Yes":
            done = []
            window.find_element("-DONE-").Update(values=done)
        else:
            pass

    elif event == "-REDO_DONE-":  # doneをredoしたとき
        if values["-DONE-"] == []:  # 空の場合は警告
            sg.popup_ok("Not Selected")
        else:  # tasksの先頭に戻す
            done.remove(values["-DONE-"][0])
            tasks.insert(0, values["-DONE-"][0])
            window.find_element("-DONE-").Update(values=done)
            window.find_element("-TASKS-").Update(values=tasks)

    elif event == None:
        break

# taskとdoneを書き込んで終了
pk.dump(tasks, open(TASK_PATH, "wb"))
pk.dump(done, open(DONE_PATH, "wb"))

window.Close()
