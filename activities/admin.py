from django.contrib import admin

from activities.models import Task, SubTask, Team


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'completed', 'created']
    list_filter = ['user', 'completed', 'created']
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    ordering = ['completed', 'created']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'completed', 'created']
    list_filter = ['task', 'completed', 'created']
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    ordering = ['completed', 'created']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    list_filter = ['created']
    search_fields = ['name', 'description']
    date_hierarchy = 'created'
    ordering = ['created']
