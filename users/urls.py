from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    # path('', views.finance_list, name='finance_list'),
    path('', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('login/', views.login_user, name='login_user'),
    path('change_role/', views.change_user_role, name='change_user_role'),
    path('user-management/', views.user_management, name='user_management'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('edit_user_profile/<str:username>/', views.profile, name='edit_user_profile'),

]
