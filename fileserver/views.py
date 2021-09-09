from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import File, Folder
from .forms import FileForm, FolderForm
from urllib.parse import quote_plus
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
# Create your views here.

def get_directory(root):
    folders = []
    while root:
        folders.append(root)
        root = root.root
    return folders[::-1]

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    context_object_name = 'folders'

    def get_queryset(self):
        owned_objects = Folder.objects.filter(root__isnull=True, owner=self.request.user)
        shared_objects = Folder.objects.filter(root__isnull=True, users__in=[self.request.user])
        return owned_objects | shared_objects


class AddFolder(LoginRequiredMixin, generic.CreateView):
    template_name = 'modal_form.html'
    form_class = FolderForm
    
    def get_initial(self):
        initial = super().get_initial()
        initial = initial.copy()
        initial['owner'] = self.request.user
        if 'folder_id' in self.kwargs:
            initial['root'] = self.kwargs['folder_id']
        print(initial)
        return initial

class FolderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Folder
    template_name = 'modal_form.html'
    form_class = FolderForm

class FolderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Folder
    template_name = 'delete_confirm.html'
    
    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('index')

class FolderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Folder
    template_name = 'folder_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["folder_map"] = get_directory(Folder.objects.get(id=self.kwargs['pk']).root)
        return context

class AddFile(LoginRequiredMixin, generic.CreateView):
    template_name = 'modal_form.html'
    form_class = FileForm

    def get_initial(self):
        if 'folder_id' in self.kwargs:
            initial = super().get_initial()
            initial = initial.copy()
            initial['folder'] = self.kwargs['folder_id']
            return initial
        else:
            return super().get_initial()

class FileDetailView(LoginRequiredMixin, generic.DetailView):
    model = File
    template_name = 'file_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["folder_map"] = get_directory(context['file'].folder)
        #print(context['file'].folder.id)
        #ip = requests.get('http://ip.42.pl/raw').text
        ip = 'localhost'
        context['url_encoded'] = 'http://' + ip + ':6969/stream/' + str(quote_plus(context['file'].file.path))
        
        context['data'] = ''
        if context['file'].file_type == 'Text':
            with open(context['file'].file.path, 'r') as f:
                context['data'] = f.read()
        return context

class FileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = File
    template_name = 'modal_form.html'
    form_class = FileForm

class FileDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = File
    template_name = 'delete_confirm.html'
    
    def get_success_url(self):
        if self.request.GET.get('next', ''):
            return (self.request.GET.get('next', ''))
        return  reverse_lazy('index')