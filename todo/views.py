from django.shortcuts import render
from .models import Tasks


def tasklist_view(request):
    tasks = Tasks.objects.filter(user=request.user)
    return render(request, "todo.html", {"tasks": tasks})
