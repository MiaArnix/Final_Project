from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from users.models import Gender, NameContext, RelationshipType, IdentityNameAccess
from .serializers import (
    GenderSerializer,
    NameContextSerializer,
    RelationshipTypeSerializer,
    IdentityNameAccessSerializer,
)

class GenderViewSet(viewsets.ModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [IsAuthenticated]


class NameContextViewSet(viewsets.ModelViewSet):
    queryset = NameContext.objects.all()
    serializer_class = NameContextSerializer
    permission_classes = [IsAuthenticated]


class RelationshipTypeViewSet(viewsets.ModelViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer
    permission_classes = [IsAuthenticated]


class IdentityNameAccessViewSet(viewsets.ModelViewSet):
    queryset = IdentityNameAccess.objects.all()
    serializer_class = IdentityNameAccessSerializer
    permission_classes = [IsAuthenticated]