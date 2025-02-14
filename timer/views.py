from django.shortcuts import render
from django.http import HttpResponse


def update_default_time(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def save_time(request):
    return HttpResponse("Hello, world. You're at the polls index.")
