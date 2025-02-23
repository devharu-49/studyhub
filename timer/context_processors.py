from django.shortcuts import render, redirect
from .forms import SaveTimeForm
from user.models import CustomUser

# 作業時間登録フォームを渡す
def timer_modal_form(request):
  form = SaveTimeForm()
  return {"timer_modal_form": form}

# 現在のフェースを取得
# def set_is_working(request):
#     if "is_working" not in request.session:
#        request.session["is_working"] = True


# 時間のフォーマットを整える
def format_time(time):
  hours = int(time // 3600)
  minutes = int((time % 3600) // 60)
  seconds = int(time % 60)

  return f"{hours:02}:{minutes:02}:{seconds:02}"

# 作業時間、休憩時間、ポモドーロON/OFF, 現在のフェーズを渡す
def get_set_time(request):
  if not request.user.is_authenticated:
        # return redirect("login")
        return {"work_time": "00:00:30"}

  user_id = request.user.user_id
  currentuser = CustomUser.objects.get(user_id = user_id)
  is_pomodoro = currentuser.is_pomodoro
  if not is_pomodoro:
     request.session["is_working"] = True

  is_working =  request.session.get("is_working", True)
  
  if is_working:
    set_time = format_time(currentuser.work_time.total_seconds())
  else:  
    set_time = format_time(currentuser.break_time.total_seconds())
  

  return {"set_time": set_time, "is_pomodoro": is_pomodoro, "is_working": is_working}
  
