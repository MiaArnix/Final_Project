from rest_framework import serializers
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityName, IdentityRelationship
from django.contrib.auth import get_user_model

AuthUser = get_user_model()

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
    
    relationship_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RelationshipType.objects.all(), source='relationship_type', write_only=True
    )
    name_context_id = serializers.PrimaryKeyRelatedField(
        queryset=NameContext.objects.all(), source='name_context', write_only=True
    )

    class Meta:
        model = IdentityNameAccess
        fields = ['id', 'relationship_type', 'name_context', 'relationship_type_id', 'name_context_id']
        read_only_fields = ['id', 'relationship_type', 'name_context']

class IdentityNameSerializer(serializers.ModelSerializer):
    name_context = serializers.CharField(source='name_context.name', read_only=True, required=False)
    
    name_context_id = serializers.PrimaryKeyRelatedField(
        queryset=NameContext.objects.all(), source='name_context', write_only=True, required=False
    )
    
    identity_id = serializers.PrimaryKeyRelatedField(
        queryset=Identity.objects.all(), source='identity', write_only=True, required=False
    )
    
    name_value = serializers.CharField(required=False)
    
    class Meta:
        model = IdentityName
        fields = ['id', 'identity', 'identity_id', 'name_value', 'name_context', 'name_context_id', 'is_default']
        read_only_fields = ['id', 'identity', 'name_context']
        
    def validate(self, data):
        is_create_action = self.instance is None
        name_context = data.get('name_context')
        name_value = data.get('name_value')
        is_default = data.get('is_default')
        identity = data.get('identity')
        
        if is_create_action:
            if not identity:
                raise serializers.ValidationError({'identity_id': 'This field is required.'})
            if not name_context:
                raise serializers.ValidationError({'name_context_id': 'This field is required.'})
            if not name_value:
                raise serializers.ValidationError({'name_value': 'This field is required.'})
            if is_default is True and IdentityName.objects.filter(identity=data.get('identity'), is_default=True).exists():
                raise serializers.ValidationError("Only one default name is allowed.")
        else:
            if name_context is not None and name_context not in NameContext.objects.all():
                raise serializers.ValidationError("Invalid name context.")
            
        return data
    
    def create(self, validated_data):
        name_context = validated_data.get('name_context')
        name_value = validated_data.get('name_value')
        is_default = validated_data.get('is_default', False)  
        identity = validated_data.get('identity')
        
        if IdentityName.objects.filter(name_context=name_context, identity=identity).exists():
            raise serializers.ValidationError("A name with this context already exists in this identity.")
        
        identity_name = IdentityName.objects.create(
            identity=identity,
            name_value=name_value,
            name_context=name_context,
            is_default=is_default
        )
        
        return identity_name
    
    def update(self, instance, validated_data):
        name_context = validated_data.pop('name_context', None)
        name_value = validated_data.pop('name_value', None)
        is_default = validated_data.pop('is_default', None)
        
        if name_context is not None:
            instance.name_context = name_context
        
        if name_value is not None:
            instance.name_value = name_value
        
        if is_default is not None:
            # if setting this name as default, set current default name to false
            if is_default:
                IdentityName.objects.filter(identity=instance.identity, is_default=True).update(is_default=False)
            instance.is_default = is_default
        
        instance.save()
        return instance
        
class IdentityRelationshipSerializer(serializers.ModelSerializer):
    relationship_type = serializers.CharField(
        source='relationship_type.name', read_only=True
    )
    consumer_username = serializers.CharField(
        source='consumer.username', read_only=True, required=False
    )
    identity_owner = serializers.CharField(
        source='identity.owner.username', read_only=True, required=False
    )
    accessible_names = serializers.SerializerMethodField(read_only=True)
    
    # fields for create and update actions
    consumer = serializers.PrimaryKeyRelatedField(
        queryset=AuthUser.objects.all(), write_only=True, required=False
    )
    relationship_type_id = serializers.PrimaryKeyRelatedField(
        queryset=RelationshipType.objects.all(), source='relationship_type', write_only=True
    )
    identity_id = serializers.PrimaryKeyRelatedField(
        queryset=Identity.objects.all(), source='identity', write_only=True, required=False
    )
    
    class Meta:
        model = IdentityRelationship
        fields = ['id', 'identity_owner', 'identity', 'identity_id', 'consumer', 'consumer_username', 'relationship_type', 'relationship_type_id', 'accessible_names']
        read_only_fields = ['id', 'identity', 'identity_owner', 'consumer_username', 'accessible_names', 'relationship_type']
        
    def get_accessible_names(self, obj):
        # get allowed name contexts for this relationship type
        allowed_contexts = IdentityNameAccess.objects.filter(
            relationship_type=obj.relationship_type
        ).values_list('name_context', flat=True)
        
        # filter identity names by allowed name contexts
        allowed_names = obj.identity.names.filter(name_context_id__in=allowed_contexts)
        
        # if no names match the allowed contexts, return the default name if it exists
        if not allowed_names.exists():
            default_name = obj.identity.names.filter(is_default=True).first()
            if default_name:
                return IdentityNameSerializer([default_name], many=True).data
            else:
                return []
        
        return IdentityNameSerializer(allowed_names, many=True).data

    def validate(self, data):
        is_create_action = self.instance is None
        relationship_type = data.get('relationship_type')
        
        if is_create_action:
            consumer = data.get('consumer')
            identity = data.get('identity')
           
            if consumer is None or relationship_type is None or identity is None:
                raise serializers.ValidationError("Consumer, identity and relationship type fields are required.")
            if consumer is None:
                raise serializers.ValidationError("Consumer does not exist.")
            if identity.owner == consumer:
                raise serializers.ValidationError("Owner cannot have a relationship to itself.")
            if relationship_type not in RelationshipType.objects.all():
                raise serializers.ValidationError("Invalid relationship type.")
            
            # replace the username with the actual user instance
            data['consumer'] = consumer  
            
        return data
    
    def create(self, validated_data):
        consumer = validated_data.get('consumer')
        relationship_type = validated_data.get('relationship_type')
        identity = validated_data.get('identity')
        
        if IdentityRelationship.objects.filter(identity=identity, consumer=consumer).exists():
            raise serializers.ValidationError("A relationship between this identity and consumer already exists.")
        
        relationship = IdentityRelationship.objects.create(
            identity=identity,
            consumer=consumer,
            relationship_type=relationship_type
        )
        
        return relationship
    
    def update(self, instance, validated_data):
        relationship_type = validated_data.pop('relationship_type', None)
        
        if relationship_type is not None:
            if relationship_type not in RelationshipType.objects.all():
                raise serializers.ValidationError("Invalid relationship type.")
            instance.relationship_type = relationship_type
        
        instance.save()
        return instance
  
class IdentitySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    gender = serializers.CharField(source='gender.name', read_only=True)
    names = IdentityNameSerializer(many=True, read_only=True)  
    
    gender_id = serializers.PrimaryKeyRelatedField(
        queryset=Gender.objects.all(), write_only=True, required=False
    )
    is_public = serializers.BooleanField(required=False)
    names_list = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=AuthUser.objects.all(), source='owner', write_only=True, required=False)
    
    class Meta:
        model = Identity
        fields = ['id', 'owner', 'owner_id', 'gender', 'names', 'gender_id', 'is_public', 'names_list']
        read_only_fields = ['id', 'owner', 'names']
        
    def validate(self, data):
        is_create_action = self.instance is None
        names_list = data.get('names_list', [])
        gender_id = data.get('gender_id')
        is_public = data.get('is_public')
        owner = data.get('owner')
        
        if is_create_action:
            if not owner:
                raise serializers.ValidationError({'owner_id': 'This field is required.'})
            if not gender_id:
                raise serializers.ValidationError({'gender_id': 'This field is required.'})
            if not is_public:
                raise serializers.ValidationError({'is_public': 'This field is required.'})
            if not names_list:
                raise serializers.ValidationError({'names_list': 'At least one name must be provided.'})
        
            default_names = [name for name in names_list if name.get('is_default')]
            if len(default_names) != 1:
                raise serializers.ValidationError("Exactly one default name must be provided.")
            
            contexts = [name.get('name_context_id') for name in names_list]
            if len(contexts) != len(set(contexts)):
                raise serializers.ValidationError("Duplicate name contexts are not allowed in names_list.")
        
        return data
    
    def create(self, validated_data):
        gender = validated_data.get('gender_id')
        is_public = validated_data.get('is_public')
        names_list = validated_data.get('names_list')
        owner = validated_data.get('owner')
        
        if not names_list or len(names_list) == 0:
            raise serializers.ValidationError({
            "names_list": "At least one name must be provided."
        })
        
        identity = Identity.objects.create(
            owner=owner, gender=gender, is_public=is_public
        )
        
        for name in names_list:
            name_context_id = name.get('name_context_id')
            name_value = name.get('name_value')
            is_default = name.get('is_default', False)
            
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