from django.urls import path
from . import views

urlpatterns = [
    path('genders/', views.GenderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='gender-list'),
    path('name-contexts/', views.NameContextViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='name-context-list'),
    path('relationship-types/', views.RelationshipTypeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='relationship-type-list'),
    path('identity-name-access/', views.IdentityNameAccessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='identity-name-access-list'),
    path('identities/', views.IdentityViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='identity-list'),
    path('identities/<int:pk>/', views.IdentityViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update', 'delete': 'destroy'
    }), name='identity-detail'),
]