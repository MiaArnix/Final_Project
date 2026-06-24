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
    consumer = serializers.CharField(
        source='consumer.username', read_only=True
    )
    identity_owner = serializers.CharField(
        source='identity.owner.username', read_only=True
    )
    
    class Meta:
        model = IdentityRelationship
        fields = ['id', 'identity_owner','identity', 'consumer', 'relationship_type']


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
    owner = serializers.CharField(source='owner.username', read_only=True)
    gender = serializers.CharField(source='gender.name', read_only=True)
    names = serializers.SerializerMethodField(read_only=True)
    
    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), write_only=True, required=False
    )
    is_public = serializers.BooleanField(required=False)
    names_list = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    
    class Meta:
        model = Identity
        fields = ['id', 'owner', 'gender', 'names', 'gender_id', 'is_public', 'names_list']
        read_only_fields = ['id', 'owner']
        
    def validate(self, data):
        is_create_action = self.instance is None
        names_list = data.get('names_list', [])
        gender_id = data.get('gender_id')
        is_public = data.get('is_public')
        
        if is_create_action:
            if gender_id is None:
                raise serializers.ValidationError("The 'gender_id' field is required.")
            if is_public is None:
                raise serializers.ValidationError("The 'is_public' field is required.")
            if not names_list:
                raise serializers.ValidationError("At least one name must be provided.")
        
            default_names = [name for name in names_list if name.get('is_default')]
            if len(default_names) != 1:
                raise serializers.ValidationError("Exactly one default name must be provided.")
        
        return data
    
    def create(self, validated_data):
        gender = validated_data.get('gender_id')
        is_public = validated_data.get('is_public')
        names_list = validated_data.get('names_list')
        
        if not names_list or len(names_list) == 0:
            raise serializers.ValidationError({
            "names_list": "At least one name must be provided."
        })
        
        identity = Identity.objects.create(
            owner=self.context['request'].user,
            gender=gender,
            is_public=is_public
        )
        
        for name_data in names_list:
            name_context_id = name_data.get('name_context_id')
            name_value = name_data.get('name_value')
            is_default = name_data.get('is_default', False)
            
            if not name_context_id or not name_value:
                raise serializers.ValidationError("Each name must have a 'name_context_id' and 'name_value'.")
            
            name_context = NameContext.objects.get(id=name_context_id)
            IdentityName.objects.create(
                identity=identity,
                name_context=name_context,
                name_value=name_value,
                is_default=is_default
            )
            
        return identity
    
    def update(self, instance, validated_data):
        gender = validated_data.pop('gender_id', None)
        is_public = validated_data.pop('is_public', None)
        
        if gender is not None:
            instance.gender = gender

        if is_public is not None:
            instance.is_public = is_public

        instance.save()
        return instance
    
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
        fields = ['id', 'identity', 'name_value', 'name_context', 'is_default']
        read_only_fields = ['id', 'identity']
        
    