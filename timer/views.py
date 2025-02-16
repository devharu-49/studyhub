from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import SaveTimeForm
from user.models import CustomUser
import datetime
import json

# デフォルトのタイマー時間を変更
def update_default_time(request):
    if not request.user.is_authenticated:
        data = {"message": "ERROR"}
        return JsonResponse(data)
    
    if request.method == "POST":
        current_user_id = request.user.user_id
        post_data = json.loads(request.body)
        timeparts = [int(part) for part in post_data["settingtime"].split(":")]
        totalsec = (timeparts[0]*3600) + (timeparts[1]*60) + (timeparts[2])

        current_user = CustomUser.objects.get(user_id = current_user_id)
        current_user.default_time = datetime.timedelta(seconds=totalsec)
        current_user.save()

    else:
        data = {"message": "GET"}
        return JsonResponse(data)

    data = {"massage": "OK"}
    return JsonResponse(data)


# DBに勉強時間登録
def save_time(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        post_data = request.POST.copy()
        timeparts = [int(part) for part in post_data.get("count_time").split(":")]
        totalsec = (timeparts[0]*3600) + (timeparts[1]*60) + (timeparts[2])
        post_data["count_time"] =  datetime.timedelta(seconds=totalsec)

        form = SaveTimeForm(post_data)

        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.user
            form.save()

    else:
        return redirect(request.META['HTTP_REFERER'])

    return redirect(request.META['HTTP_REFERER'])


