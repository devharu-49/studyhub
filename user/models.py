import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class CustomUser(AbstractUser):
    # デフォルトのフィールド削除
    username = None
    first_name = None
    last_name = None
    date_joined = None
    last_login = None

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    default_time = models.DurationField(default=datetime.timedelta(minutes=30))

    USERNAME_FIELD = "email"  # ログイン時にemailを使用
    REQUIRED_FIELDS = ["name"]  # サインアップ時にnameが必須

    # CustomUserとして作成されたテーブル名をUsersに変更
    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.name


class Todos(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE
    )  # Userが削除されたら削除
    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


class Times(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    count_time = models.DurationField()

    def __str__(self):
        return self.user_id
