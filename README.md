# pysimplegui_fifo_todo

PySimpleGUI で作成した FIFO 型の TODO リスト

## 機能

- 左上のテキストウィンドウでタスクを追加
  - 何も入力しないとエラーウィンドウが表示
  - 重複するタスクは追加不可
- Task List で 一番上の タスクをクリックし、 SET を押してタスク開始
  - 一番上から順番にしかタスクを選択出来ないようにしてあるので注意
- タスクを終えたら DONE で終了
  - タイマーで 1 時間をカウントしており、タスクが終わらなければ 1 時間ごとに LINE に通知
- Done List に終えたタスクが一覧で表示される
  - REDO で Task List に戻す
  - Delete で選択したタスクだけ消去
  - Clear で全消去

## 参考画像

![外観](fig%5Coverall.png)
