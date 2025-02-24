from django.shortcuts import render, redirect, get_object_or_404
from .models import Tasks
from .forms import TaskForm


# タスク一覧取得
def tasklist_view(request):
    # 現在ログインしているユーザーに関連するタスクを選択
    # select_relatedを使って、tasksに関連するuser情報も一度に取得する（クエリ数を減らすため）
    tasks = (
        Tasks.objects.select_related("user")
        .filter(user=request.user)
        .order_by("deadline")
    )
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


# タスク削除
def taskdelete_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")  # 未ログインならログインページへリダイレクト

    task = get_object_or_404(
        Tasks, id=id, user=request.user
    )  # 自分のタスクのみ削除可能

    task.delete()
    return redirect("task_list")


# タスク編集
def taskedit_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")  # 未ログインならログインページへリダイレクト

    task = get_object_or_404(
        Tasks, id=id, user=request.user
    )  # 自分のタスクのみ編集可能

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)  # 既存のデータをフォームに適用
        if form.is_valid():
            form.save()
            return redirect("task_list")  # 一覧ページへリダイレクト

    else:
        form = TaskForm(instance=task)  # 既存のデータをフォームにセット

    return render(request, "todoform.html", {"form": form, "task": task})


def statusedit_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")  # 未ログインならログインページへリダイレクト

    task = get_object_or_404(
        Tasks, id=id, user_id=request.user.user_id
    )  # 自分のタスクのみ編集可能

    if request.method == "POST":
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed", "update_at"])

    return redirect("task_list")  # 一覧ページへリダイレクト


# Todoタイトル検索、完了未完了ソート機能
def tasksearch_view(request):
    query = request.GET.get("q", "")  # 検索キーワード取得
    status = request.GET.get("status", "")  # 完了・未完了の状態を取得

    tasks = Tasks.objects.filter(
        user=request.user
    )  # ユーザーに関連するタスクのみをフィルタリングして取得

    if query:
        tasks = tasks.filter(
            title__icontains=query
        )  # 検索ワードが空でない場合、タイトルに部分一致するタスクをフィルタリングして取得

    # 完了・未完了の状態が指定されている場合、その状態でフィルタリング
    if status == "completed":
        tasks = tasks.filter(is_completed=True)  # 完了タスクのみ
    elif status == "incomplete":
        tasks = tasks.filter(is_completed=False)  # 未完了タスクのみ

    tasks = tasks.order_by("deadline")  # タスクを締切日順に昇順に並び替え

    return render(
        request, "todo.html", {"tasks": tasks, "query": query, "status": status}
    )  # tasks（タスク一覧）、query（検索キーワード）、status（選択された状態）をコンテキストとしてtodo.htmlへ渡してレンダリング
