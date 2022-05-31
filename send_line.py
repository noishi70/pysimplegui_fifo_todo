import requests


def send_line_notify(line_token):

    line_notify_token = line_token
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {line_notify_token}"}
    data = {"message": "1時間経ちました。\nタスクをさぼっていませんか？"}
    requests.post(line_notify_api, headers=headers, data=data)
