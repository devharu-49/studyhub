from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SaveTimeForm
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.contrib.auth.models import User
import datetime


def update_default_time(request):
    
    return HttpResponse("Hello, world. You're at the polls index.")

# DBに勉強時間登録
def save_time(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        form = SaveTimeForm(request.POST)

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

