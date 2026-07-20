from django.urls import path
from . import views

urlpatterns = [
    path('genders/', views.GenderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='gender-list'),
    path('genders/<int:pk>/', views.GenderViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }), name='gender-detail'),
    path('name-contexts/', views.NameContextViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='name-context-list'),
    path('name-contexts/<int:pk>/', views.NameContextViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }), name='name-context-detail'),
    path('relationship-types/', views.RelationshipTypeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='relationship-type-list'),
    path('relationship-types/<int:pk>/', views.RelationshipTypeViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }), name='relationship-type-detail'),
    path('identity-name-access/', views.IdentityNameAccessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='identity-name-access-list'),
    path('identity-name-access/<int:pk>/', views.IdentityNameAccessViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'
    }), name='identity-name-access-detail'),
    path('identities/', views.IdentityViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='identity-list'),
    path('identities/<int:pk>/', views.IdentityViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update', 'delete': 'destroy'
    }), name='identity-detail'),
    path('identity/<int:identity_pk>/relationships/', views.IdentityRelationshipViewSet.as_view({
        'get': 'list', 'post': 'create'}), 
         name='identity-relationship-list'),
    path('identity/<int:identity_pk>/relationships/<int:pk>/', views.IdentityRelationshipViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}), 
         name='identity-relationship-detail'),
    path('identity/<int:identity_pk>/names/', views.IdentityNameViewSet.as_view({
        'get': 'list', 'post': 'create'}), 
         name='identity-name-list'),
    path('identity/<int:identity_pk>/names/<int:pk>/', views.IdentityNameViewSet.as_view({
        'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'}), 
         name='identity-name-detail'),
]