from django.db import models
from django.contrib.auth import get_user_model


class Tasks(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE
    )  # Userが削除されたら削除
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
