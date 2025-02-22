from .forms import SaveTimeForm
from user.models import CustomUser

def timer_modal_form(request):
  form = SaveTimeForm()
  return {"timer_modal_form": form}

def get_work_time(request):
  if not request.user.is_authenticated:
        return {"work_time": "00:00:30"}

  user_id = request.user.user_id
  currentuser = CustomUser.objects.get(user_id = user_id)
  totalsec = currentuser.work_time.total_seconds()

  hours = int(totalsec // 3600)
  minutes = int((totalsec % 3600) // 60)
  seconds = int(totalsec % 60)
  
  return {"work_time": f"{hours:02}:{minutes:02}:{seconds:02}"}