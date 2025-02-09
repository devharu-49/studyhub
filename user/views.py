from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .forms import CustomSignupForm


def signup_view(request):
    if request.method == "POST":  # フォームがPOSTで送信されたとき
        form = CustomSignupForm(
            request.POST
        )  # フォームにPOSTデータを渡してインスタンス作成
        if form.is_valid():  # フォームのバリデーションが成功した場合
            user = form.save()  # データベースに保存
            login(request, user)  # 保存したユーサーでログイン
            return redirect(
                "base"
            )  # あとでメイン画面にredirectするように書き直す(ビュー名を使用する)
    else:
        form = CustomSignupForm()  # フォームが送信されていない場合、空のフォームを表示

    return render(
        request, "signup.html", {"form": form}
    )  # signup.htmlテンプレートをレンダリングし、フォームを渡す


def base_view(request):
    return render(request, "base.html")
