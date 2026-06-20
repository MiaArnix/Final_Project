from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity
from .serializers import (
    GenderSerializer,
    NameContextSerializer,
    RelationshipTypeSerializer,
    IdentityNameAccessSerializer,
    IdentitySerializer,
)

class IdentityPermission(BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            perm = 'identity.read_identity'
        elif request.method == 'DELETE':
            perm = 'identity.delete_identity'
        else: 
            perm = 'identity.write_identity'
        
        return request.user.has_perm(perm, obj)

class IdentityNamePermission(BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        perm = 'identity.access_identity_name'
        return request.user.has_perm(perm, obj)

class MetadataPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            perm = 'identity.read_metadata'
        else:
            perm = 'identity.write_metadata'
        
        return request.user.has_perm(perm)

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [MetadataPermission]


class NameContextViewSet(viewsets.ModelViewSet):
    queryset = NameContext.objects.all()
    serializer_class = NameContextSerializer
    permission_classes = [MetadataPermission]


class RelationshipTypeViewSet(viewsets.ModelViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer
    permission_classes = [MetadataPermission]


class IdentityNameAccessViewSet(viewsets.ModelViewSet):
    queryset = IdentityNameAccess.objects.all()
    serializer_class = IdentityNameAccessSerializer
    permission_classes = [MetadataPermission]
    
class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    permission_classes = [IdentityPermission]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        consumer = self.request.user
        identity_id = self.request.query_params.get('identity_id')
        
        # filter by identity id if given
        if identity_id:
            queryset = queryset.filter(id=identity_id)
            
        # return public identities if not authenticated
        if not consumer.is_authenticated:
            return queryset.filter(is_public=True)
        
        # return public identities + the ones with relationship to consumer + the ones owned by consumer
        public_identities = queryset.filter(is_public=True)
        user_identities = queryset.filter(relationships__consumer=consumer)
        owned_identities = queryset.filter(owner=consumer)

        return (public_identities | user_identities | owned_identities).distinct()
