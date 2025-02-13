from django.shortcuts import render, get_object_or_404
from .models import Tasks


# タスク一覧取得
def tasklist_view(request):
    # 現在ログインしているユーザーに関連するタスクを選択
    # select_relatedを使って、tasksに関連するuser情報も一度に取得する（クエリ数を減らすため）
    tasks = Tasks.objects.select_related("user").filter(user=request.user)
    return render(request, "todo.html", {"tasks": tasks})


# タスク詳細取得
def taskdetail_view(request, id):
    # Tasksテーブルからidが一致し、かつuserがログイン中のユーザーのタスクを取得する。
    # データが存在しない場合は自動的に「404エラー」
    task = get_object_or_404(Tasks, id=id, user=request.user)
    return render(request, "tododetail.html", {"task": task})
