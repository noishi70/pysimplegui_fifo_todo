# pysimplegui_fifo_todo

PySimpleGUI で作成した FIFO 型の TODO リスト

登録した順番でのタスクの処理のみ可能

重要度を無視して手の付けやすいタスクからしかやらない自分を戒めるために作成

タスクをさぼって携帯をいじっていてもLINEで催促されるので安心

## 機能

- 左上のテキストウィンドウでタスクを追加
  - 何も入力しないとエラーウィンドウが表示
  - 重複するタスクは追加不可
- Task List で 一番上の タスクをクリックし、 SET を押してタスク開始
  - 一番上から順番にしかタスクを選択出来ないようにしてあるので注意
- Editで追加したTaskを編集
- タスクを終えたら DONE で終了
  - タイマーで 1 時間をカウントしており、タスクが終わらなければ 1 時間ごとに LINE に通知
- Done List に終えたタスクが一覧で表示される
  - REDO で Task List に戻す
  - Delete で選択したタスクだけ消去
  - Clear で全消去

## 参考画像
- 全体図
</br>

![概観](https://user-images.githubusercontent.com/74105563/171169323-9190ecbf-e5dc-40c6-b8ff-5bad473c8e9e.png)

- エラーウィンドウ
</br>

![エラーウィンドウ](https://user-images.githubusercontent.com/74105563/171170947-c78aa74e-81ef-4770-b94f-bb98668c6d6a.png)

- LINEへの通知
</br>

![LINEへの通知](https://user-images.githubusercontent.com/74105563/171169733-854878b1-17ae-4f5e-9da5-1b8508398c74.png)

