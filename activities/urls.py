from django.urls import path

from activities import views

app_name = 'activities'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]
