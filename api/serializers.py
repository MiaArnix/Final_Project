from rest_framework import serializers
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class NameContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameContext
        fields = ['id', 'name']


class RelationshipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipType
        fields = ['id', 'name']


class IdentityNameAccessSerializer(serializers.ModelSerializer):
    relationship_type = serializers.CharField(
        source='relationship_type.name', read_only=True
    )
    name_context = serializers.CharField(
        source='name_context.name', read_only=True
    )

    class Meta:
        model = IdentityNameAccess
        fields = ['id', 'relationship_type', 'name_context']
