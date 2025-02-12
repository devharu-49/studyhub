from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .forms import CustomSignupForm, LoginForm


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
                return redirect("base")
            else:
                form.add_error(None, "無効なメールアドレスまたはパスワードです。")
        else:
            form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")  # ログインページにリダイレクト


def base_view(request):
    return render(request, "base.html")
