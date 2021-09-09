from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, LogoutView
#app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='generic_form.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<pk>/', views.UserEditProfileView.as_view(), name='profile'),
    path('change_password/', views.PasswordChangeView.as_view(template_name='modal_form.html'), name='password_change'),
]