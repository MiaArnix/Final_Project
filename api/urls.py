from django.urls import path
from . import views

urlpatterns = [
    path('genders/', views.GenderViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='gender-list'),
    path('name-contexts/', views.NameContextViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='name-context-list'),
    path('relationship-types/', views.RelationshipTypeViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='relationship-type-list'),
    path('identity-name-access/', views.IdentityNameAccessViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='identity-name-access-list'),
    path('identities/', views.IdentityViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='identity-list'),
    path('identity-names/', views.IdentityNameViewSet.as_view({
        'get': 'list',
        'post': 'create', 'patch': 'update', 'delete': 'destroy'
    }), name='identity-name-list')
]