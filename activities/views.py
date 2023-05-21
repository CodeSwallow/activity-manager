from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = 'activities/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ProfileView(View):
    template_name = 'activities/profile.html'

    def get(self, request):
        return render(request, self.template_name)
