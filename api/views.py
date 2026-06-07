from rest_framework import viewsets
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityName
from .serializers import (
    GenderSerializer,
    NameContextSerializer,
    RelationshipTypeSerializer,
    IdentityNameAccessSerializer,
    IdentitySerializer,
    IdentityNameSerializer
)


class SuperuserWriteElseRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)
    
## need to allow users to read if they have a relationship with the identity, and write if they are the owner of the identity

#TBD       


class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [SuperuserWriteElseRead]


class NameContextViewSet(viewsets.ModelViewSet):
    queryset = NameContext.objects.all()
    serializer_class = NameContextSerializer
    permission_classes = [SuperuserWriteElseRead]


class RelationshipTypeViewSet(viewsets.ModelViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer
    permission_classes = [SuperuserWriteElseRead]


class IdentityNameAccessViewSet(viewsets.ModelViewSet):
    queryset = IdentityNameAccess.objects.all()
    serializer_class = IdentityNameAccessSerializer
    permission_classes = [SuperuserWriteElseRead]
    
class IdentityViewSet(viewsets.ModelViewSet):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    permission_classes = [AllowAny]
    
class IdentityNameViewSet(viewsets.ModelViewSet):
    queryset = IdentityName.objects.all()
    serializer_class = IdentityNameSerializer
    permission_classes = [AllowAny]