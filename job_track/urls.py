from django.urls import path
from . import views

app_name = 'job_track'

urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('detail/<int:job_id>', views.job_detail, name='job_detail'),
    path('search', views.search, name='search'),
    path('help', views.help, name='help'),
]