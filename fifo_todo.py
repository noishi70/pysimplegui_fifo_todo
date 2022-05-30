from copyreg import pickle
from genericpath import exists
import PySimpleGUI as sg
import pickle as pk
import load_files
import os

# フォントとテーマの設定
sg.set_options(font=("Times New Roman", 15))
sg.theme("DarkTeal5")

# ファイルパスの設定と読み込み
DIR_PATH = os.path.dirname(__file__)
os.chdir(DIR_PATH)

FILE_PATH = "./files/"
TASK_PATH = FILE_PATH + "tasks.pkl"
DONE_PATH = FILE_PATH + "done.pkl"
tasks, done = load_files.load_files(FILE_PATH, TASK_PATH, DONE_PATH)

# column作成
col_tasks = [
    [
        sg.Button("DONE", key="-DONE_TASK-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Edit", key="-EDIT_TASK-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Delete", key="-DEL_TASK-", button_color=("black", "DarkSalmon")),
    ],
    [sg.Listbox(values=tasks, size=(30, 10), key="-TASKS-")],
]

col_done = [
    [
        sg.Button("REDO", key="-REDO_DONE-", button_color=("black", "PaleTurquoise1")),
        sg.Button("Delete", key="-DEL_DONE-", button_color=("black", "DarkSalmon")),
    ],
    [sg.Listbox(values=done, size=(30, 10), key="-DONE-")],
]

# layoutの作成
layout = [
    [sg.Text("FIFO_TODO", font=("Times New Roman", 30))],
    [sg.Text("Handle tasks in order", font=("Times New Roman", 20))],
    [
        sg.InputText("Enter Your Task", key="-TASK_INPUT-"),
        sg.Button(button_text="Add", key="-ADD-", button_color=("black", "OliveDrab2")),
    ],
    [sg.Column(col_tasks), sg.Column(col_done)],
]

# window呼び出し
window = sg.Window("FIFO_TODO", layout, resizable=True)


while True:  # Event Loop
    event, values = window.Read()  # Event -> key, values -> item

    if event == "-ADD-":  # taskを追加したとき
        if values["-TASK_INPUT-"] == "":  # 空の場合は追加しない
            sg.popup_ok("Input Your Task")
        else:
            if values["-TASK_INPUT-"] not in tasks:  # 重複するタスクは登録しない
                tasks.append(values["-TASK_INPUT-"])
                window.find_element("-TASKS-").Update(values=tasks)
                window.find_element("-ADD-").Update("Add")
                window.find_element("-TASK_INPUT-").Update(value="")
            else:
                sg.popup_ok("Registered tasks")

    elif event == "-DONE_TASK-":  # taskをdoneしたとき
        if values["-TASKS-"] == []:  # 空の場合は追加しない
            sg.popup_ok("Not Selected")
        else:  # 最初のタスクのみdoneが実行できる
            if tasks.index(values["-TASKS-"][0]) == 0:
                tasks.remove(values["-TASKS-"][0])
                done.append(values["-TASKS-"][0])
                window.find_element("-TASKS-").Update(values=tasks)
                window.find_element("-DONE-").Update(values=done)
            else:
                sg.popup_ok("Finish the first task")

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
