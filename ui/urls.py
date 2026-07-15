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
    path('identities/<int:identity_id>/', views.edit_identity, name='edit-identity'),
    path('identities/<int:identity_id>/delete/', views.delete_identity, name='delete-identity'),
    path('add-relationship/', views.add_relationship, name='add-relationship'),
    path('delete_relationship/<int:relationship_id>/', views.delete_relationship, name='delete-relationship'),
    path('add-name/', views.add_name, name='add-name'),
    path('delete-name/<int:name_id>/', views.delete_name, name='delete-name'),
    path('edit-name/<int:name_id>/', views.edit_name, name='edit-name'),
]
