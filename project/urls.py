from django.urls import path
from . import view

app_name='project'
urlpatterns =[
    path('',view.projects, name='projects'),
    path('project/<str:pk>/',view.project, name='project'),
    path('create-project/',view.createProject, name='create-project'),
    path('update-project/<str:pk>/',view.updateProject, name='update-project'),
    path('delete-project/<str:pk>/',view.deleteProject, name='delete-project'),
    
    
]