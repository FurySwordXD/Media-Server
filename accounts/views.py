from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django import forms
from django.contrib.auth.views import PasswordChangeView
# Create your views here

class UserEditForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'true',})
        }

class UserEditProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'modal_form.html'
    model = User
    form_class = UserEditForm

    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('index')

class PasswordChangeView(PasswordChangeView):
    template_name = 'modal_form'
    
    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('index')