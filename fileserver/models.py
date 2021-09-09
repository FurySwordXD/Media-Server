from django.db import models
from django.urls import reverse
from . import check_text
from django.contrib.auth.models import User
# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=100)
    root = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="owner")
    users = models.ManyToManyField(User, related_name="users")

    def get_absolute_url(self):
        return reverse('folder-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

class File(models.Model):
    FILE_TYPES = ["File", "Video", "Audio", "Image", "Text"]
    VIDEO_EXT = [".mp4", ".avi", ".mkv", ".flv", ".wmv", ".webm", ".mov"]
    AUDIO_EXT = [".mp3", ".mpa", ".ogg", ".wav", ".wma", ".aif", ".cda", ".mid"]
    IMAGE_EXT = [".png", ".gif", ".jpg", ".bmp", ".tga", ".tiff"]

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField()
    file_type = models.CharField(max_length=20, choices=zip(FILE_TYPES,FILE_TYPES), default="File", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('folder-detail', kwargs={'pk': self.folder.pk})

    def __str__(self):
        if self.name:
            return self.file.name + ' - ' + self.name
        return self.file.name

    def save(self, *args, **kwargs):
        if self.file.name.lower().endswith(tuple(File.VIDEO_EXT)):
            self.file_type = "Video"
        elif self.file.name.lower().endswith(tuple(File.AUDIO_EXT)):
            self.file_type = "Audio"
        elif self.file.name.lower().endswith(tuple(File.IMAGE_EXT)):
            self.file_type = "Image"
        super().save(*args, **kwargs)
        if self.file_type == "File" and check_text.istextfile(self.file.path):
            self.file_type = "Text"
        super().save(*args, **kwargs)