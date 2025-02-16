
from django.db import models
from django.contrib.auth import get_user_model


class Times(models.Model):

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_column="user_id")
    count_time = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Times"

    def __str__(self):
        return self.count_time
    