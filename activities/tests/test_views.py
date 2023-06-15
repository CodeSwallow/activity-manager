from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from activities.models import Task, SubTask, Team


def create_user(username='user', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(username, password)


def create_task(title='Task', description='Task description', created_by=None, team=None):
    """Create and return a new task."""
    if created_by is None:
        created_by = create_user()
    return Task.objects.create(title=title, description=description, created_by=created_by, team=team)


class HomeViewTests(TestCase):
    """
    Test the HomeView view.
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('activities:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/home.html')


class ProfileViewTests(TestCase):
    """
    Test the ProfileView view.
    """

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities:profile'))
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('activities:profile'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('activities:profile'))
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

    def test_logged_in_uses_correct_template(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('activities:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/profile.html')

    def test_logged_in_uses_correct_context(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('activities:profile'))

        self.assertEqual(str(response.context['user']), 'user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/profile.html')
        self.assertEqual(response.context['user'].username, 'user')

    def test_tasks_in_context(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('activities:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/profile.html')
        self.assertEqual(response.context['tasks'].count(), 0)


class TaskListViewTests(TestCase):
    """
    Test the TaskListView view.
    """

    def test_task_list_view_url_exists_at_desired_location(self):
        response = self.client.get('/task-list/')
        self.assertEqual(response.status_code, 302)

    def test_task_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities:task_list'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('activities:task_list'))
        self.assertRedirects(response, '/accounts/login/?next=/task-list/')

    def test_logged_in_uses_correct_template(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('activities:task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/task_list.html')

    def test_logged_in_uses_correct_task_context(self):
        user = create_user()
        self.client.force_login(user)
        response = self.client.get(reverse('activities:task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/task_list.html')
        self.assertEqual(response.context['tasks'].count(), 0)

    def test_logged_in_user_sees_only_his_tasks(self):
        other_user = create_user(username='other_user')
        create_task(title='Task', description='Task description', created_by=other_user)

        user = create_user()
        create_task(title='Task', description='Task description', created_by=user)
        self.client.force_login(user)
        response = self.client.get(reverse('activities:task_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/task_list.html')
        self.assertEqual(response.context['tasks'].count(), 1)


class TaskDetailViewTests(TestCase):
    """
    Test the TaskDetailView view.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()
        cls.task = create_task(title='Task', description='Task description', created_by=cls.user)

    def test_task_detail_view_url_exists_at_desired_location(self):
        response = self.client.get('/task-detail/1/')
        self.assertEqual(response.status_code, 302)

    def test_task_detail_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities:task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('activities:task_detail', args=[self.task.id]))
        self.assertRedirects(response, '/accounts/login/?next=/task-detail/1/')
