from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'ui'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('metadata/', views.metadata_list, name='metadata-list'),
    path('identities/', views.identity_list, name='identity-list'),
    path('identities/create/', views.create_identity, name='create-identity'),
    path('add_relationship/', views.add_relationship, name='add-relationship'),
    path('delete_relationship/<int:relationship_id>/', views.delete_relationship, name='delete-relationship'),
]
