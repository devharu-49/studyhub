from django.contrib import admin
from .models import Times

class TimesAdmin(admin.ModelAdmin):
    # exclude = ("groups", "user_permissions", "date_joined", "last_login")
    list_display = ("user_id", "count_time", "created_at")
    readonly_fields = ["user_id"]
    fieldsets = (
        (None, {"fields": ("user_id", "count_time", "created_at")}),
    )

admin.site.register(Times)
