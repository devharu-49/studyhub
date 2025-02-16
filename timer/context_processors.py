from .forms import SaveTimeForm
from user.models import CustomUser

def timer_modal_form(request):
  form = SaveTimeForm()
  return {"timer_modal_form": form}

def get_default_time(request):
  if not request.user.is_authenticated:
        return {"default_time": "00:00:30"}

  user_id = request.user.user_id
  currentuser = CustomUser.objects.get(id = user_id)
  default_time = currentuser.default_time
  return {"default_time": default_time}