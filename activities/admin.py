from django.contrib import admin

from activities.models import Task, SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'completed', 'created']
    list_filter = ['user', 'completed', 'created']
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    ordering = ['completed', 'created']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'task', 'completed', 'created']
    list_filter = ['task', 'completed', 'created']
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    ordering = ['completed', 'created']
