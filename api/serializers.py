from rest_framework import serializers
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityName, IdentityRelationship


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
        
class IdentityRelationshipSerializer(serializers.ModelSerializer):
    relationship_type = serializers.CharField(
        source='relationship_type.name', read_only=True
    )
    
    class Meta:
        model = IdentityRelationship
        fields = ['id', 'identity', 'consumer', 'relationship_type']


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
    names = serializers.SerializerMethodField()
    
    class Meta:
        model = Identity
        fields = ['id', 'owner', 'gender', 'names']
        read_only_fields = ['id', 'owner']
        
    def get_names(self, identity):
        consumer = self.context['request'].user
        
        # return default name if identity is public
        if identity.is_public:
            return IdentityNameSerializer(identity.names.filter(is_default=True), many=True).data
        
        # return all names if consumer is owner or superuser
        if identity.owner == consumer or consumer.is_superuser:
            return IdentityNameSerializer(identity.names.all(), many=True).data
        
        # check if consumer has relationship with identity
        relationship = IdentityRelationship.objects.filter(
            identity=identity,
            consumer=consumer
        ).first()
        
        # return empty list if no relationship found
        if not relationship:
            return []
        
        # get allowed name contexts for the relationship type
        allowed_contexts = IdentityNameAccess.objects.filter(
        relationship_type=relationship.relationship_type).values_list('name_context', flat=True)
        
        # filter identity names by allowed name contexts
        allowed_names = identity.names.filter(name_context_id__in=allowed_contexts)
        
        # if at this point there is no name available, return the default name if exists
        if not allowed_names.exists():
            default_name = identity.names.filter(is_default=True).first()
            if default_name:
                return IdentityNameSerializer([default_name], many=True).data
            else:
                return []
        
        return IdentityNameSerializer(allowed_names, many=True).data 
                              
class IdentityNameSerializer(serializers.ModelSerializer):
    name_context = serializers.CharField(source='name_context.name')
    
    class Meta:
        model = IdentityName
        fields = ['id', 'identity', 'name_value', 'name_context']
        read_only_fields = ['id', 'identity']
        
    