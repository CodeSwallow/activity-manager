from django.urls import path
from django.views.generic import TemplateView

from activities import views

app_name = 'activities'

urlpatterns = [
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('', views.HomeView.as_view(), name='home'),
    path('about/', TemplateView.as_view(template_name='activities/about.html'), name='about'),
    path('create-task/', views.CreateTaskView.as_view(), name='create_task'),
    path('task-list/', views.TaskListView.as_view(), name='task_list'),
    path('task-detail/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
]
