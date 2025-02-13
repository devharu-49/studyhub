from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from .forms import TaskForm


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


# タスク作成
def taskcreate_view(request):
    if not request.user.is_authenticated:
        return redirect("login")  # 未ログインの場合はログインページにリダイレクト

    if request.method == "POST":  # フォームがPOSTで送信されたとき
        form = TaskForm(request.POST)  # フォームにPOSTデータを渡してインスタンス作成
        if form.is_valid():  # フォームのバリデーションが成功した場合
            task = form.save(commit=False)  # データベースに保存
            task.user = request.user  # 現在ログインしているユーザーをタスクに関連付け
            task.save()
            return redirect("task_list")  # 一覧ページにリダイレクト
        else:
            return render(request, "todoform.html", {"form": form})
    else:
        form = TaskForm()  # フォームが送信されていない場合、空のフォームを表示

    return render(request, "todoform.html", {"form": form})
