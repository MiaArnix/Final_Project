from django.urls import path
from . import views

app_name = 'ui'

urlpatterns = [
    path('metadata/', views.metadata_list, name='metadata-list'),
]
