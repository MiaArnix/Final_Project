from rest_framework import viewsets, serializers
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly 
from rest_framework.exceptions import PermissionDenied, NotFound
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityRelationship, IdentityName
from .serializers import (
    GenderSerializer,
    NameContextSerializer,
    RelationshipTypeSerializer,
    IdentityNameAccessSerializer,
    IdentitySerializer, 
    IdentityRelationshipSerializer,
    IdentityNameSerializer
)

class IdentityPermission(BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated and not obj.is_public:
            raise PermissionDenied("You must be authenticated to access this identity.")
        if request.method in SAFE_METHODS:
            perm = 'identity.read_identity'
        elif request.method == 'DELETE':
            perm = 'identity.delete_identity'
        else: 
            perm = 'identity.write_identity'
        
        if not request.user.has_perm(perm, obj):
            raise PermissionDenied("You do not have permission to access this identity.")

        return True

class IdentityNamePermission(BasePermission):
    
    def has_permission(self, request, view):
        identity_id = view.kwargs.get('identity_pk')
        
        try:
            identity = Identity.objects.get(pk=identity_id)
        except Identity.DoesNotExist:
            raise NotFound("Identity does not exist.")

        if request.method in SAFE_METHODS:
            perm = 'identity.read_identity_name'
        else: 
            perm = 'identity.write_identity_name'
            
        if not request.user.has_perm(perm, identity):
            raise PermissionDenied("You do not have permission to access this identity name.")
        return True
    
    def has_object_permission(self, request, view, name):
        try:
            identity = name.identity
        except Identity.DoesNotExist:
            raise NotFound("Identity does not exist.")

        if request.method in SAFE_METHODS:
            perm = 'identity.read_identity_name'
        else: 
            perm = 'identity.write_identity_name'
        
        if not request.user.has_perm(perm, identity):
            raise PermissionDenied("You do not have permission to access this identity name.")

        return True
    
class IdentityRelationshipPermission(BasePermission):
    def has_permission(self, request, view):
        identity_id = view.kwargs.get('identity_pk')
        
        try:
            identity = Identity.objects.get(pk=identity_id)
        except Identity.DoesNotExist:
            raise NotFound("Identity does not exist.")
        
        perm = 'identity.access_identity_relationship'    
        if not request.user.has_perm(perm, identity):
            raise PermissionDenied("You do not have permission to access this identity relationship.")

        return True
    
    def has_object_permission(self, request, view, obj):
        identity = obj.identity 
        perm = 'identity.access_identity_relationship'

        if not request.user.has_perm(perm, identity):
            raise PermissionDenied("You do not have permission to access this relationship.")

        return True

class MetadataPermission(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.has_perm('identity.write_metadata')

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [MetadataPermission, IsAuthenticatedOrReadOnly]

class NameContextViewSet(viewsets.ModelViewSet):
    queryset = NameContext.objects.all()
    serializer_class = NameContextSerializer
    permission_classes = [MetadataPermission, IsAuthenticatedOrReadOnly]

class RelationshipTypeViewSet(viewsets.ModelViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer
    permission_classes = [MetadataPermission]

class IdentityNameAccessViewSet(viewsets.ModelViewSet):
    queryset = IdentityNameAccess.objects.all()
    serializer_class = IdentityNameAccessSerializer
    permission_classes = [MetadataPermission, IsAuthenticatedOrReadOnly]
    
class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    permission_classes = [IdentityPermission, IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Identity.objects.all()
        identity_id = self.request.query_params.get('pk')
    
        if identity_id:
            queryset = queryset.filter(id=identity_id)
            
        if self.action == 'list':
            consumer = self.request.user
            if consumer.is_authenticated:
                public_identities = queryset.filter(is_public=True)
                user_identities = queryset.filter(relationships__consumer=consumer)
                owned_identities = queryset.filter(owner=consumer)
                queryset = (public_identities | user_identities | owned_identities).distinct()
            else:
                queryset = queryset.filter(is_public=True)
    
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def to_representation(self,instance):
        data = super().to_representation(instance)
        user = self.request.user
        
        # filter related entities based on access permissions
        if instance.is_public or instance.owner == user or user.is_superuser:  
            return data
        
        relationship = instance.relationships.filter(consumer=user).first()
        
        if not relationship:
            data['names'] = []
            return data
        
        allowed_contexts = IdentityNameAccess.objects.filter(relationship_type=relationship.relationship_type).values_list('name_context_id', flat=True)
        
        allowed_names = instance.identity_names.filter(name_context_id__in=allowed_contexts)
        
        if allowed_names.exists():
            data['names'] = IdentityNameSerializer(allowed_names, many=True).data
        else:
            # Fall back to default name if no matches
            default_name = instance.identity_names.filter(is_default=True).first()
            data['names'] = IdentityNameSerializer([default_name], many=True).data if default_name else []
        
        return data
     
class IdentityRelationshipViewSet(viewsets.ModelViewSet):
    queryset = IdentityRelationship.objects.all()
    serializer_class = IdentityRelationshipSerializer
    permission_classes = [IdentityRelationshipPermission, IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        identity_id = self.kwargs.get('identity_pk')
        
        try:
            identity = Identity.objects.get(pk=identity_id)
        except Identity.DoesNotExist:
            raise NotFound("Identity does not exist.")

        serializer.save(identity=identity)
    
    def get_queryset(self):
        user = self.request.user
        queryset = IdentityRelationship.objects.all()
        
        # filter by identity owner - only return relationships for identities owned by user
        identity_id = self.kwargs.get('identity_pk')
        relationship_id = self.kwargs.get('pk')
        
        if relationship_id and identity_id:
            queryset = queryset.filter(id=relationship_id, identity_id=identity_id, identity__owner=user)
        elif identity_id:
            queryset = queryset.filter(identity_id=identity_id, identity__owner=user)
        else:
            queryset = queryset.filter(identity__owner=user)
        
        return queryset
    
class IdentityNameViewSet(viewsets.ModelViewSet):
    queryset = IdentityName.objects.all()
    serializer_class = IdentityNameSerializer
    permission_classes = [IdentityNamePermission, IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        identity_id = self.kwargs.get('identity_pk')
        
        try: 
            identity = Identity.objects.get(pk=identity_id)
        except Identity.DoesNotExist:
            raise NotFound("Identity does not exist.")

        serializer.save(identity=identity)
    
    def get_queryset(self):
        identity_id = self.kwargs.get('identity_pk')
        name_id = self.kwargs.get('pk')
        
        queryset = IdentityName.objects.all()
        
        if name_id and identity_id:
            queryset = queryset.filter(id=name_id, identity_id=identity_id)
        elif identity_id:
            queryset = queryset.filter(identity_id=identity_id )

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # prevent deletion of default name
        if instance.is_default:
            raise serializers.ValidationError(
                "Cannot delete the default name. Set another name as default first.")
        
        return super().destroy(request, *args, **kwargs)