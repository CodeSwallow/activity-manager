from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView


class HomeView(View):
    template_name = 'activities/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(View):
    template_name = 'activities/profile.html'

    def get(self, request):
        return render(request, self.template_name)


class CreateTaskView(CreateView):
    template_name = 'activities/create_task.html'
