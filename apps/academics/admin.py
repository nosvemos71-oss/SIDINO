
from django.contrib import admin

from .models import Area, Subject


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    search_fields = ("name",)
    list_filter = ("is_active",)
    inlines = [SubjectInline]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "area",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
        "area__name",
    )

    list_filter = (
        "area",
        "is_active",
    )
