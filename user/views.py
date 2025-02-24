from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from todo.models import Tasks
from timer.models import Times
from .models import CustomUser
from .forms import CustomSignupForm, LoginForm, MypageForm

from datetime import timedelta


# サインアップ
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

# ログイン
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

# ログアウト
def logout_view(request):
    logout(request)
    return redirect("login")  # ログインページにリダイレクト

# メインページ
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


# マイページ
def mypage_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")
    
    user_info = get_object_or_404(CustomUser, user_id=id)

    if request.method == "POST":
        form = MypageForm(request.POST, instance=user_info)      
        if form.is_valid():
            is_pomodoro = form.cleaned_data["is_pomodoro"]
            form.save()
            if not is_pomodoro:
                request.session["is_working"] = False
            return redirect("mypage", id=request.user.user_id)
        
    else:
        form = MypageForm(instance=user_info)

    duration_data = get_duration_data(request.user.user_id)
    work_time_sum = minutes_to_hms(sum(duration_data["times"]))
        
    return render(request, "mypage.html", {"form":form, "work_time_sum":work_time_sum, "duration_data":duration_data})


# 指定期間の作業時間データを収集
def get_duration_data(user_id, range='week'):
    # 今を取得
    now = timezone.localdate()
 
    # 週、月、年、全部の選択肢によって場合分け
    # 各選択肢ごとに取得する期間の幅を取得
    if range == "week":
        start_date = now - timedelta(days=6)
    elif range == "month":
        start_date = now - timedelta(days=30)
    elif range == "year":
        start_date = now - timedelta(days=365)
    else:
        start_date = None
    print("たいむs", start_date)
    # print(start_date.date())
    
    # その幅を使ってDBからデータをとってくる
    if start_date:
        count_times = Times.objects.filter(user_id = user_id, created_at__gte = start_date).order_by("created_at")
    else:
        count_times = Times.objects.filter(user_id = user_id).order_by("created_at")
    print("わーくたいむs", count_times.values)

    # グラフ用に整形
    count_times_par_date = []

    date = start_date
    while date <= now:
        count_times_par_date.append({"create_date": date, "count_time": 0})
        date += timedelta(days=1)

    for time in count_times:
        create_date = time.created_at.date()
        count_second = time.count_time.total_seconds()
        print("あああ",create_date, count_second)

        for date in count_times_par_date:
            print("あああ")
            print(date)
            if date["create_date"] and date["create_date"] == create_date:
                date["count_time"] += count_second
                break
        else:
            count_times_par_date.append({"create_date": create_date, "count_time": count_second})

    dates = [date["create_date"].strftime("%m/%d") for date in count_times_par_date]
    times = [date['count_time']/60 for date in count_times_par_date]

    duration_data = {"dates": dates, "times":times}

    return duration_data

# 分から時:分:秒に変換
def minutes_to_hms(minutes):
    hours = int(minutes // 60)
    minutes_remainder = int(minutes % 60)
    seconds = round((minutes % 1) * 60)

    return f"{hours:02}:{minutes_remainder:02}:{seconds:02}"
