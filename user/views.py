from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from todo.models import Tasks
from timer.models import Times
from .models import CustomUser
from .forms import CustomSignupForm, LoginForm, MypageForm
from map.views import search_near_place

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
    # 近くの検索結果を3件取得
    near_place = search_near_place(request)
    keys = ["name", "geometry", "rating", "place_id", "walking_distance","vicinity"]
    filtered_by_key = [{k: r[k] for k in keys} for r in near_place]
    transformed_data = [{"name": item['name'], "lat": str(item['geometry']['location']['lat']), "lng": str(item['geometry']['location']['lng']), "rating":str(item["rating"]), "place_id":item["place_id"], "walking_distance":item["walking_distance"], "vicinity":item["vicinity"]}
    for item in filtered_by_key]

    return render(request, "main.html", {"tasks": tasks, "results" : transformed_data})


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

    range = request.GET.get("range", "week") # 設定された集計期間
    duration_data = get_duration_data(request.user.user_id, range) # グラフ用のデータ取得
    work_time_sum = minutes_to_hms(sum(duration_data["times"])) # 指定期間の合計

    context = {"form":form, "work_time_sum":work_time_sum, "duration_data":duration_data, "range":range}      
    return render(request, "mypage.html", context)


# 指定期間の作業時間データを収集
def get_duration_data(user_id, range='week'):

    now = timezone.localdate() 
    # 週、月、年、全部の選択肢によって場合分け
    if range == "week":
        start_date = now - timedelta(days=6)
    elif range == "month":
        start_date = now - timedelta(days=30)
    elif range == "year":
        start_date = now - timedelta(days=365)
    else:
        start_date = None
    
    # その幅を使ってDBからデータをとってくる
    if start_date:
        count_times = Times.objects.filter(user_id = user_id, created_at__gte = start_date).order_by("created_at")
    else:
        count_times = Times.objects.filter(user_id = user_id).order_by("created_at")
    # 日ごとのデータを入れる配列
    count_times_par_date = []    
    # 計算基準日設定
    if start_date:
        date = start_date
    else:
        current_user = CustomUser.objects.get(user_id = user_id)
        date = current_user.created_at.date()
    # 現在までの日ごとの辞書を作成
    while date <= now:
        count_times_par_date.append({"create_date": date, "count_time": 0})
        date += timedelta(days=1)
    # 集計
    for time in count_times:
        create_date = time.created_at.date()
        count_second = time.count_time.total_seconds()

        for date in count_times_par_date:
            if date["create_date"] and date["create_date"] == create_date:
                date["count_time"] += count_second
                break
        else:
            count_times_par_date.append({"create_date": create_date, "count_time": count_second})
    # データ分割と変換    
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
