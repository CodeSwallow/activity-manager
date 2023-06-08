from django.test import TestCase
from django.contrib.auth import get_user_model

from activities.models import Task, SubTask, Team


def create_user(username='user', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(username, password)


def create_team(name='Team', description='Team description', created_by=None):
    """Create and return a new team."""
    if created_by is None:
        created_by = create_user()
    return Team.objects.create(name=name, description=description, created_by=created_by)


def create_task(title='Task', description='Task description', created_by=None, team=None):
    """Create and return a new task."""
    if created_by is None:
        created_by = create_user()
    return Task.objects.create(title=title, description=description, created_by=created_by, team=team)


def create_subtask(title='Subtask', description='Subtask description', task=None):
    """Create and return a new subtask."""
    if task is None:
        task = create_task()
    return SubTask.objects.create(title=title, description=description, task=task)


class TaskModelTests(TestCase):
    """
    Test the Task model.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.team = create_team(created_by=cls.user)

    def test_get_absolute_url(self):
        task = create_task(created_by=self.user, team=self.team)
        self.assertEqual(task.get_absolute_url(), f'/task-detail/{task.id}/')

    def test_object_name_is_title(self):
        task = create_task(created_by=self.user, team=self.team)
        self.assertEqual(str(task), task.title)


class SubTaskModelTests(TestCase):
    """
    Test the SubTask model.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.task = create_task(created_by=cls.user)

    def test_object_name_is_title(self):
        subtask = create_subtask(task=self.task)
        self.assertEqual(str(subtask), subtask.title)
