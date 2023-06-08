from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class Task(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        null=True, blank=True
    )
    team = models.ForeignKey('Team', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('activities:task_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('activities:team_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
