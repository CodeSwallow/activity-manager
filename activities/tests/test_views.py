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

    def test_logged_in_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('activities:task_detail', args=[self.task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/task_detail.html')

    def test_logged_in_uses_correct_task_context(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('activities:task_detail', args=[self.task.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/task_detail.html')
        self.assertEqual(response.context['task'].title, 'Task')
        self.assertEqual(response.context['task'].description, 'Task description')

    def test_logged_in_user_sees_only_his_tasks(self):
        other_user = create_user(username='other_user')
        other_task = create_task(title='Task', description='Task description', created_by=other_user)

        self.client.force_login(self.user)
        response = self.client.get(reverse('activities:task_detail', args=[other_task.id]))

        self.assertEqual(response.status_code, 404)


class TaskCreateViewTests(TestCase):
    """
    Test the TaskCreateView view.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = create_user()

    def test_task_create_view_url_exists_at_desired_location(self):
        response = self.client.get('/create-task/')
        self.assertEqual(response.status_code, 302)

    def test_task_create_view_url_accessible_by_name(self):
        response = self.client.get(reverse('activities:create_task'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('activities:create_task'))
        self.assertRedirects(response, '/accounts/login/?next=/create-task/')

    def test_logged_in_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('activities:create_task'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/create_task.html')

    def test_logged_in_user_can_create_task(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('activities:create_task'), data={
            'title': 'Task',
            'description': 'Task description'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Task')
        self.assertEqual(Task.objects.first().description, 'Task description')
        self.assertEqual(Task.objects.first().created_by, self.user)

