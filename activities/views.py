from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from activities.models import Task, Team


class HomeView(View):
    template_name = 'activities/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'activities/profile.html'

    def get(self, request):
        tasks = Task.objects.filter(created_by=request.user)
        return render(request, self.template_name, {'tasks': tasks})


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'activities/create_task.html'
    fields = ['title', 'description']
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'activities/task_list.html.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'activities/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class TeamListView(ListView):
    model = Team
    template_name = 'activities/team_list.html'
    context_object_name = 'teams'

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)


class TeamDetailView(DetailView):
    model = Team
    template_name = 'activities/team_detail.html'
    context_object_name = 'team'

    def get_queryset(self):
        return Team.objects.filter(members=self.request.user)


class CalendarView(View):  # TODO: currently a placeholder, will be implemented later
    template_name = 'activities/calendar.html'

    def get(self, request):
        return render(request, self.template_name)


class SettingsView(View):  # TODO: currently a placeholder, will be implemented later
    template_name = 'activities/settings.html'

    def get(self, request):
        return render(request, self.template_name)
