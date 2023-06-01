from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from activities.models import Task


class HomeView(View):
    template_name = 'activities/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(View):
    template_name = 'activities/profile.html'

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        return render(request, self.template_name, {'tasks': tasks})


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'activities/create_task.html'
    fields = ['title', 'description']
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
