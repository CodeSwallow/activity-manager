from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from activities.models import Task, SubTask, Team


def create_user(username='user', password='test_pass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(username, password)


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

        self.assertEqual(str(response.context['user']), 'user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'activities/profile.html')
