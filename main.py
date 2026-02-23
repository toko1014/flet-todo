import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

# 新しいタスクを入力するテキストフィールド
    new_task = ft.TextField(hint_text="新しいタスクを入力", expand=True)
    # タスクリストを表示するカラム
    tasks_view = ft.Column()

    #ドラッグ中のビジュアルフィードバック（受け入れ可能なターゲットの上に来た時）
    def drag_will_accept(e):
        #ドロップ先となるタスクの枠線を白くして、どこにドロップできるかわかりやすくする
        e.control.content.border = ft.border.all(2,ft.Colors.WHITE)
        e.control.update()

    #ドラッグがターゲットから離れた時の処理
    def drag_leave(e):
        #枠線を元に戻す
        e.control.content.border = None
        e.control.update()

    #タスクがドロップされた時の入れ替え処理
    def move_task(e):
        #ドラッグ元のコントロール（DragTarget）を取得
        src = page.get_control(e.src_id).data
        #ドロップ先のコントロール（DragTarget）を取得
        dest = e.control

        #ドロップ先の枠線を元に戻す
        dest.content.border = None

        #もしドラッグ元とドロップ先が同じなら何もしない
        if src == dest:
            dest.update()
            return
        
        #tasks_view.controlsリスト内でのインデックスを取得
        src_index = tasks_view.controls.index(src)
        dest_index = tasks_view.controls.index(dest)

        #リストからドラッグ元のタスクを一旦削除
        tasks_view.controls.pop(src_index)
        #ドロップ先の位置にタスクを挿入
        tasks_view.controls.insert(dest_index, src)

        page.update()

    #タスク完了時の処理
    def task_status_change(e):
        #チェックボックスが配置されているft.Rowを取得
        task_row = e.control.data
        #Row内のft.Textコントロールを取得(インデックス１に配置)
        task_text_control = task_row.controls[1]

        #チェックの状態に応じてテキストの装飾を変更
        if e.control.value:
            #チェックが入ったら取り消し線を適用
            task_text_control.style = ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH,color=ft.Colors.GREY)
        else:
            #チェックが外れたら装飾をリセット
            task_text_control.style = ft.TextStyle(decoration=ft.TextDecoration.NONE,color=ft.Colors.WHITE)

        #Row内のTextコントロールのstyleプロパティを更新するために、Row自体を更新
        task_row.update()
        page.update()

    # タスク削除時の処理
    def delete_task(e):
        # 該当するタスクをtasks_viewから削除する
        tasks_view.controls.remove(e.control.data)
        page.update()

    # 「追加」ボタンが押されたときの処理
    def add_clicked(e):
        if new_task.value:
            task_name = new_task.value

            #1.各コントロールを作成
            task_checkbox = ft.Checkbox(value=False, on_change=task_status_change)
            task_text = ft.Text(task_name,expand=True)
            delete_button = ft.IconButton(icon=ft.Icons.DELETE,
                                          tooltip="削除",
                                          on_click=delete_task)
            #Draggableコントロールを変数に格納する
            draggable_item = ft.Draggable(
                content=ft.IconButton(icon=ft.Icons.DRAG_HANDLE, tooltip="移動")
            )

            #2.Rowにコントロールを配置（Draggableでラップしたハンドルを追加）
            task_row = ft.Row(
                controls=[
                    draggable_item,
                    task_checkbox,
                    task_text,
                    delete_button,
                ],
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            #3.Row全体をDragTargetでラップ
            task_wrapper = ft.DragTarget(
                content=task_row,
                on_will_accept=drag_will_accept,
                on_accept=move_task,
                on_leave=drag_leave,
            )

            #4.各コントロールに、親となるtask_wrapperをデータとして持たせる
            task_checkbox.data = task_wrapper
            delete_button.data = task_wrapper

            #Draggableコントロールに直接データを設定する
            draggable_item.data = task_wrapper

            tasks_view.controls.append(task_wrapper)

            new_task.value = ""
            new_task.focus()
            page.update()

    # 画面に表示する要素を配置
    page.add(
        ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        new_task,
                        ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=add_clicked),
                    ],spacing=30
                ),
                tasks_view,
            ],
        )
    )

ft.app(target=main)
