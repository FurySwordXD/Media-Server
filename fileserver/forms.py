from django.forms import ModelForm, HiddenInput
from .models import Folder, File

class FileForm(ModelForm):
    
    class Meta:
        model = File
        fields = ['name', 'file', 'folder']
        widgets = {
            'folder': HiddenInput(),
        }


class FolderForm(ModelForm):

    class Meta:
        model = Folder
        fields = '__all__'
        widgets = {
            'root': HiddenInput(),
            
        }