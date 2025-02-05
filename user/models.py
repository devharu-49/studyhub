import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone
import datetime


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Djangoの createsuperuser コマンドが username を求めるので、適当な値を設定する
        extra_fields.setdefault(
            "username", email
        )  # `username` の代わりに `email` を使う

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # デフォルトのフィールド削除
    username = None
    first_name = None
    last_name = None

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    default_time = models.DurationField(default=datetime.timedelta(minutes=30))

    USERNAME_FIELD = "email"  # ログイン時にemailを使用
    REQUIRED_FIELDS = ["name"]  # サインアップ時にnameが必須

    objects = CustomUserManager()

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
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Times(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    count_time = models.DurationField()

    def __str__(self):
        return self.user_id
