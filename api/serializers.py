from rest_framework import serializers
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityName


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
        
class IdentitySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    gender = serializers.CharField(source='gender.name')
    names = serializers.StringRelatedField(many=True)
    class Meta:
        model = Identity
        fields = ['id', 'owner', 'gender', 'names']
        read_only_fields = ['id', 'owner']
        
class IdentityNameSerializer(serializers.ModelSerializer):
    name_context = serializers.CharField(source='name_context.name')
    
    class Meta:
        model = IdentityName
        fields = ['id', 'identity', 'name_value', 'name_context']
        read_only_fields = ['id', 'identity']