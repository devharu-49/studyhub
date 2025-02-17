from django.contrib import admin
from .models import Tasks


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "user")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "title",
                    "description",
                    "is_completed",
                    "deadline",
                    "created_at",
                    "update_at",
                )
            },
        ),
    )
    readonly_fields = (
        "created_at",
        "update_at",
    )


admin.site.register(Tasks, TaskAdmin)
