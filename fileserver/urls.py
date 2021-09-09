from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#app_name = 'accounts'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('folder/add/<folder_id>', views.AddFolder.as_view(), name='add-folder'),
    path('folder/add/', views.AddFolder.as_view(), name='add-folder'),
    path('folder/<pk>/', views.FolderDetailView.as_view(), name='folder-detail'),
    path('folder/<pk>/update', views.FolderUpdateView.as_view(), name='update-folder'),
    path('folder/<pk>/delete', views.FolderDeleteView.as_view(), name='delete-folder'),

    path('folder/<folder_id>/file/add/', views.AddFile.as_view(), name='add-file'),
    
    path('file/add/', views.AddFile.as_view(), name='add-file'),
    path('file/<pk>/', views.FileDetailView.as_view(), name='file-detail'),
    path('file/<pk>/update', views.FileUpdateView.as_view(), name='update-file'),
    path('file/<pk>/delete', views.FileDeleteView.as_view(), name='delete-file'),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)