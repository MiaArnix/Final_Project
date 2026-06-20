from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'ui'

urlpatterns = [
    path('', RedirectView.as_view(url='identities/'), name='index'),
    path('register/', views.register, name='register'),
    path('metadata/', views.metadata_list, name='metadata-list'),
    path('identities/', views.identity_list, name='identity-list'),
    path('add_relationship/', views.add_relationship, name='add-relationship')
]
