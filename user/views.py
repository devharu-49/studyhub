from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum

from todo.models import Tasks
from timer.models import Times
from .models import CustomUser
from .forms import CustomSignupForm, LoginForm, MypageForm

from datetime import timedelta


def signup_view(request):
    if request.method == "POST":  # フォームがPOSTで送信されたとき
        form = CustomSignupForm(
            request.POST
        )  # フォームにPOSTデータを渡してインスタンス作成
        if form.is_valid():  # フォームのバリデーションが成功した場合
            user = form.save()  # データベースに保存
            login(request, user)  # 保存したユーサーでログイン
            return redirect("main")  # メイン画面にredirectする
    else:
        form = CustomSignupForm()  # フォームが送信されていない場合、空のフォームを表示

    return render(
        request, "signup.html", {"form": form}
    )  # signup.htmlテンプレートをレンダリングし、フォームを渡す


def login_view(request):

    form = LoginForm()  # ここで事前にformを定義（GETリクエスト時のフォーム）

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("main")
            else:
                form.add_error(None, "無効なメールアドレスまたはパスワードです。")
        # else:
        #     form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")  # ログインページにリダイレクト


def main_view(request):
    if not request.user.is_authenticated:
        return redirect("login")  # ログインしていない場合、ログインページへリダイレクト

    # 締切日の近いタスクを3件取得
    tasks = (
        Tasks.objects.filter(user=request.user)
        .exclude(is_completed=True)
        .order_by("deadline")[:3]
    )
    return render(request, "main.html", {"tasks": tasks})


# mypage表示
def mypage_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")  # ログインしていない場合、ログインページへリダイレクト
    
    user_info = get_object_or_404(CustomUser, user_id=id)

    if request.method == "POST":
        form = MypageForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect("mypage", id=request.user.user_id)
        
    else:
        form = MypageForm(instance=user_info)

        referer_url = request.META['HTTP_REFERER']

        work_time_list = Times.objects.filter(user_id = id).values_list("count_time")
        work_time_values = [item[0] for item in work_time_list]
        work_time_sum = sum(work_time_values, timedelta())
        
        print(work_time_list)
        print(work_time_values)
        print("あああ")
        print(work_time_sum)
        
    return render(request, "mypage.html", {"form":form, "work_time_sum":work_time_sum, "referer_url":referer_url})