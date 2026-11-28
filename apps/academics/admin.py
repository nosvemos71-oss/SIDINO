from django.contrib import admin

from .models import AcademicGroup, AcademicPeriod, Course, GroupEnrollment


class GroupEnrollmentInline(admin.TabularInline):
    model = GroupEnrollment
    extra = 0


@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    ordering = ("-start_date",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(AcademicGroup)
class AcademicGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "period")
    list_filter = ("period", "course")
    inlines = (GroupEnrollmentInline,)
