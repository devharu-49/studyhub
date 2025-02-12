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

        extra_fields.pop("username", None)

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
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # ログイン時にemailを使用
    REQUIRED_FIELDS = ["name"]  # サインアップ時にnameが必須

    objects = CustomUserManager()

    class Meta:
        db_table = "Users"  # CustomUserとして作成されたテーブル名をUsersに変更
        verbose_name = "User"  # 管理サイト上でのテーブル名表記指定
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name


class Tasks(models.Model):

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

    class Meta:
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.title


class Times(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    count_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Times"

    def __str__(self):
        return f"{self.user_id.name} - {self.datetime}"
