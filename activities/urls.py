from django.urls import path

from activities import views

app_name = 'activities'

urlpatterns = [
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.HomeView.as_view(), name='home'),
]
