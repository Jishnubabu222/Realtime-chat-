from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/', views.user_list, name='users'),
    path('chat/<int:user_id>/', views.chat_view, name='chat'),
]
