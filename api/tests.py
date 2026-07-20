import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from .model_factories import *
from identity.models import *
from .serializers import *

class SerializerStructureTestCase(APITestCase):
    gender = None
    name_context = None
    relationship_type = None
    identity_name_access = None
    identity = None
    identity_name = None
    identity_relationship = None
    consumer = None
    owner = None
    
    def setUp(self):
        request_factory = APIRequestFactory()
        request = request_factory.get('/')
        
        self.gender = GenderFactory.create(name="Male")
        self.name_context = NameContextFactory.create(name="First Name")
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.identity_name_access = IdentityNameAccess.objects.create(relationship_type=self.relationship_type, name_context=self.name_context)
        self.owner = UserFactory.create(username="owner", password="testpassword")
        request.user = self.owner
        self.consumer = UserFactory.create(username="consumer", password="testpassword")
        self.identity = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity_name = IdentityNameFactory.create(
            identity=self.identity,
            name_context=self.name_context,
            name_value="John",
            is_default=True
        )
        self.identity_relationship = IdentityRelationshipFactory.create(
            identity=self.identity,
            consumer=self.consumer,
            relationship_type=self.relationship_type
        )
        self.gender_serializer = GenderSerializer(instance=self.gender)
        self.name_context_serializer = NameContextSerializer(instance=self.name_context)
        self.relationship_type_serializer = RelationshipTypeSerializer(instance=self.relationship_type)
        self.identity_name_access_serializer = IdentityNameAccessSerializer(instance=self.identity_name_access)
        self.identity_serializer = IdentitySerializer(instance=self.identity, context={'request': request})
        self.identity_name_serializer = IdentityNameSerializer(instance=self.identity_name)
        self.identity_relationship_serializer = IdentityRelationshipSerializer(instance=self.identity_relationship)
        
    def tearDown(self):
        IdentityRelationship.objects.all().delete()
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        AuthUser.objects.all().delete()
        Gender.objects.all().delete()
        NameContext.objects.all().delete()
        RelationshipType.objects.all().delete()
        IdentityNameAccess.objects.all().delete()
        
        IdentityRelationshipFactory.reset_sequence()
        IdentityNameFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        UserFactory.reset_sequence()
        GenderFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        RelationshipTypeFactory.reset_sequence()
        IdentityNameAccessFactory.reset_sequence()
    
    def test_genderSerializerHasAllFields(self):
        data = self.gender_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name']))
    
    def test_genderSerializerHasCorrectFields(self):
        data = self.gender_serializer.data
        self.assertEqual(data['id'], self.gender.id)
        self.assertEqual(data['name'], self.gender.name)
        
    def test_nameContextSerializerHasAllFields(self):
        data = self.name_context_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name']))
        
    def test_nameContextSerializerHasCorrectFields(self):
        data = self.name_context_serializer.data
        self.assertEqual(data['id'], self.name_context.id)
        self.assertEqual(data['name'], self.name_context.name)
        
    def test_relationshipTypeSerializerHasAllFields(self):
        data = self.relationship_type_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name']))
        
    def test_relationshipTypeSerializerHasCorrectFields(self):
        data = self.relationship_type_serializer.data
        self.assertEqual(data['id'], self.relationship_type.id)
        self.assertEqual(data['name'], self.relationship_type.name)
        
    def test_identityNameAccessSerializerHasAllFields(self):
        data = self.identity_name_access_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'relationship_type', 'name_context']))
        
    def test_identityNameAccessSerializerHasCorrectFields(self):
        data = self.identity_name_access_serializer.data
        self.assertEqual(data['id'], self.identity_name_access.id)
        self.assertEqual(data['relationship_type'], self.relationship_type.name)
        self.assertEqual(data['name_context'], self.name_context.name)
        
    def test_identitySerializerHasAllFields(self):
        data = self.identity_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'owner', 'gender', 'is_public', 'names']))
        
    def test_identitySerializerHasCorrectFields(self):
        data = self.identity_serializer.data
        self.assertEqual(data['id'], self.identity.id)
        self.assertEqual(data['owner'], self.owner.username)
        self.assertEqual(data['gender'], self.gender.name)
        self.assertEqual(data['is_public'], self.identity.is_public)
        
    def test_identityNameSerializerHasAllFields(self):
        data = self.identity_name_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'identity', 'name_context', 'name_value', 'is_default']))
        
    def test_identityNameSerializerHasCorrectFields(self):
        data = self.identity_name_serializer.data
        self.assertEqual(data['id'], self.identity_name.id)
        self.assertEqual(data['identity'], self.identity.id)
        self.assertEqual(data['name_context'], self.name_context.name)
        self.assertEqual(data['name_value'], self.identity_name.name_value)
        self.assertEqual(data['is_default'], self.identity_name.is_default)
        
    def test_identityRelationshipSerializerHasAllFields(self):
        data = self.identity_relationship_serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'identity_owner', 'identity', 'consumer_username', 'relationship_type', 'accessible_names']))
        
    def test_identityRelationshipSerializerHasCorrectFields(self):
        data = self.identity_relationship_serializer.data
        self.assertEqual(data['id'], self.identity_relationship.id)
        self.assertEqual(data['identity_owner'], self.identity.owner.username)
        self.assertEqual(data['consumer_username'], self.consumer.username)
        self.assertEqual(data['relationship_type'], self.relationship_type.name)

class IdentityNameAccessSerializerTestCase(APITestCase):
    relationship_type = None
    name_context = None
    identity_name_access = None
    identity_name_access_serializer = None
    
    def setUp(self):
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.name_context = NameContextFactory.create(name="First Name")
        self.identity_name_access = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type,
            name_context=self.name_context
        )
        self.identity_name_access_serializer = IdentityNameAccessSerializer(instance=self.identity_name_access)
    
    def tearDown(self):
        IdentityNameAccess.objects.all().delete()
        RelationshipType.objects.all().delete()
        NameContext.objects.all().delete()
        
        IdentityNameAccessFactory.reset_sequence()
        RelationshipTypeFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        
    def test_relationshipTypeFieldIsReadOnly(self):
        serializer = IdentityNameAccessSerializer(instance=self.identity_name_access, data={'relationship_type': 'Sibling'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_access = serializer.save()
        
        self.assertEqual(updated_access.relationship_type, self.relationship_type)
        
    def test_nameContextFieldIsReadOnly(self):
        serializer = IdentityNameAccessSerializer(instance=self.identity_name_access, data={'name_context': 'Last Name'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_access = serializer.save()
        
        self.assertEqual(updated_access.name_context, self.name_context)
        
    def test_relationshipTypeIdIsWriteOnly(self):
        data = self.identity_name_access_serializer.data
        self.assertNotIn('relationship_type_id', data)
        
        serializer = IdentityNameAccessSerializer(instance=self.identity_name_access, data={'relationship_type_id': self.relationship_type.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_access = serializer.save()
        
        self.assertEqual(updated_access.relationship_type, self.relationship_type)
        
    def test_nameContextIdIsWriteOnly(self):
        data = self.identity_name_access_serializer.data
        self.assertNotIn('name_context_id', data)
        
        serializer = IdentityNameAccessSerializer(instance=self.identity_name_access, data={'name_context_id': self.name_context.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_access = serializer.save()
        
        self.assertEqual(updated_access.name_context, self.name_context)
        
class IdentityNameSerializerTestCase(APITestCase):
    name_context1 = None
    name_context2 = None
    identity1 = None
    identity2 = None
    identity_name1 = None
    identity_name2 = None
    identity_name_serializer = None
    owner = None
    gender = None
    
    def setUp(self):
        self.owner = UserFactory.create(username="owner", password="testpassword")
        self.gender = GenderFactory.create(name="Male")
        self.name_context1 = NameContextFactory.create(name="First Name")
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.identity1 = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity2 = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity_name1 = IdentityNameFactory.create(
            identity=self.identity1,
            name_context=self.name_context1,
            name_value="John",
            is_default=True
        )
        self.identity_name2 = IdentityNameFactory.create(
            identity=self.identity2,
            name_context=self.name_context2,
            name_value="Doe",
            is_default=False
        )
        self.identity_name3 = IdentityNameFactory.create(
            identity=self.identity2,
            name_context=self.name_context1,
            name_value="Jane",
            is_default=True
        )
        self.identity_name_serializer = IdentityNameSerializer(instance=self.identity_name1)
        
    def tearDown(self):
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        NameContext.objects.all().delete()
        
        IdentityNameFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        
    def test_nameContextFieldIsReadOnly(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, data={'name_context': self.name_context2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context1)
        
    def test_identityFieldIsReadOnly(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, data={'identity': self.identity2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.identity, self.identity1)
        
    def test_nameContextIdIsWriteOnly(self):
        data = self.identity_name_serializer.data
        self.assertNotIn('name_context_id', data)
        
        serializer = IdentityNameSerializer(instance=self.identity_name1, data={'name_context_id': self.name_context2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context2)
        
    def test_createNameRequiresIdentityAndValueAndContext(self):
        serializer = IdentityNameSerializer(data={'name_value': 'New Name', 'name_context_id': self.name_context1.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(data={'identity_id': self.identity1.id, 'name_value': 'New Name'})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(data={'identity_id': self.identity1.id, 'name_context_id': self.name_context1.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(data={'identity_id': self.identity1.id, 'name_context_id': self.name_context2.id, 'name_value': 'New Name'})
        self.assertTrue(serializer.is_valid())
        
    def test_onlyOneDefaultNamePerIdentity(self):
        serializer = IdentityNameSerializer(data={
            'identity_id': self.identity1.id,
            'name_context_id': self.name_context2.id,
            'name_value': 'Another Name',
            'is_default': True
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Only one default name is allowed.', str(serializer.errors))
        
    def test_nameContextIdMustBeValid(self):
        serializer = IdentityNameSerializer(data={
            'identity_id': self.identity1.id,
            'name_context_id': 9999,
            'name_value': 'Invalid Context'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_identityIdMustBeValid(self):
        serializer = IdentityNameSerializer(data={
            'identity_id': 9999,
            'name_context_id': self.name_context1.id,
            'name_value': 'Invalid Identity'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_nameHasToBeUniquePerIdentity(self):
        serializer = IdentityNameSerializer(data={
            'identity_id': self.identity1.id,
            'name_context_id': self.name_context1.id,
            'name_value': 'John'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('The fields identity_id, name_context_id must make a unique set.', str(serializer.errors))
        
    def test_itIsPossibleToUpdateNameValue(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, data={'name_value': 'Updated Name'}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_value, 'Updated Name')
        
    def test_itIsPossibleToUpdateNameContext(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, data={'name_context_id': self.name_context2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context2)
        
    def test_itIsPossibleToUpdateIsDefaultToTrue(self):
        self.assertEqual(self.identity_name3.is_default, True)
        
        serializer = IdentityNameSerializer(instance=self.identity_name2, data={'is_default': True}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        self.identity_name3.refresh_from_db()
        
        self.assertEqual(updated_name.is_default, True)
        
        # previously default name is switched to False
        self.assertEqual(self.identity_name3.is_default, False)
        self.assertEqual(IdentityName.objects.filter(identity=self.identity2, is_default=True).count(), 1)

class IdentityRelationshipSerializerTestCase(APITestCase):
    relationship_type = None
    relationship_type2 = None
    name_context = None
    name_context2 = None
    identity = None
    owner = None
    consumer = None
    consumer2 = None
    gender = None
    identity_name = None
    identity_name2 = None
    identity_relationship = None
    identity_name_access = None
    identity_relationship_serializer = None
    
    def setUp(self):
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.relationship_type2 = RelationshipTypeFactory.create(name="Sibling")
        self.consumer = UserFactory.create(username="consumer", password="testpassword")
        self.consumer2 = UserFactory.create(username="consumer2", password="testpassword")
        self.owner = UserFactory.create(username="owner", password="testpassword")
        self.gender = GenderFactory.create(name="Male") 
        self.name_context = NameContextFactory.create(name="First Name")
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.identity_name_access = IdentityNameAccess.objects.create(relationship_type=self.relationship_type, name_context=self.name_context)
        self.identity = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity_relationship = IdentityRelationshipFactory.create(consumer=self.consumer, identity=self.identity, relationship_type=self.relationship_type)
        self.identity_name = IdentityNameFactory.create(identity=self.identity, name_context=self.name_context, name_value="John", is_default=False)
        self.identity_name2 = IdentityNameFactory.create(identity=self.identity, name_context=self.name_context2, name_value="Johnny", is_default=True)
        self.identity_relationship_serializer = IdentityRelationshipSerializer(instance=self.identity_relationship)
        
    def tearDown(self):
        IdentityRelationship.objects.all().delete()
        Identity.objects.all().delete()
        AuthUser.objects.all().delete()
        Gender.objects.all().delete()
        RelationshipType.objects.all().delete()
        
        IdentityRelationshipFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        UserFactory.reset_sequence()
        GenderFactory.reset_sequence()
        RelationshipTypeFactory.reset_sequence()
        
    def test_relationshipTypeFieldIsReadOnly(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, data={'relationship_type': 'Sibling'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.relationship_type, self.relationship_type)
        
    def test_consumerUsernameFieldIsReadOnly(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, data={'consumer_username': 'new_consumer'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.consumer, self.consumer)
        
    def test_identityOwnerFieldIsReadOnly(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, data={'identity_owner': 'new_owner'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.identity.owner, self.owner)
        
    def test_accessibleNamesFieldIsReadOnly(self):
        original_data = self.identity_relationship_serializer.data
        original_accessible_names = original_data['accessible_names']
    
        serializer = IdentityRelationshipSerializer(
            instance=self.identity_relationship, 
            data={'accessible_names': []}, 
            partial=True
        )
    
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
               
        new_serializer = IdentityRelationshipSerializer(instance=updated_relationship)
        self.assertEqual(new_serializer.data['accessible_names'], original_accessible_names)
        
    def test_consumerIsWriteOnly(self):
        data = self.identity_relationship_serializer.data
        self.assertNotIn('consumer', data)
        
    def test_accessibleNamesReturnsOnlyAccessibleNamesPerRules(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship)
        data = serializer.data
        
        self.assertIn('accessible_names', data)
        accessible_names = data['accessible_names']
        
        self.assertEqual(len(accessible_names), 1)
        self.assertEqual(accessible_names[0]['name_context'], self.name_context.name)
        self.assertEqual(accessible_names[0]['name_value'], self.identity_name.name_value)
        
    def test_accessibleNamesReturnsDefaultNameIfNoMatchingRuleFound(self):
        self.identity_name_access.delete()
        
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship)
        data = serializer.data
        
        self.assertIn('accessible_names', data)
        accessible_names = data['accessible_names']
        
        self.assertEqual(len(accessible_names), 1)
        self.assertEqual(accessible_names[0]['name_context'], self.name_context2.name)
        self.assertEqual(accessible_names[0]['name_value'], self.identity_name2.name_value)
        
    def test_accessibleNamesReturnsEmptyListIfNoRuleAndNoDefaultNameFound(self):
        self.identity_name_access.delete()
        self.identity_name2.delete()
        
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship)
        data = serializer.data
        
        self.assertIn('accessible_names', data)
        accessible_names = data['accessible_names']
        
        self.assertEqual(len(accessible_names), 0)
        
    def test_createRelationshipRequiresIdentityAndConsumerAndRelationshipType(self):
        serializer = IdentityRelationshipSerializer(data={'consumer': self.consumer2.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': self.consumer2.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': self.consumer2.id, 'relationship_type_id': self.relationship_type.id})
        self.assertTrue(serializer.is_valid())
        
        
    def test_consumerIdHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': 9999, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_relationshipTypeHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': self.consumer.id, 'relationship_type_id': 9999})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_consumerCannotEqualOwner(self):
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': self.owner.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Owner cannot have a relationship to itself.', str(serializer.errors))
        
    def test_identityIdHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(data={'identity_id': 9999, 'consumer': self.consumer.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_onlyOneRelationshipPerConsumerAndIdentity(self):
        serializer = IdentityRelationshipSerializer(data={'identity_id': self.identity.id, 'consumer': self.consumer.id, 'relationship_type_id': self.relationship_type2.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('The fields identity_id, consumer must make a unique set.', str(serializer.errors))
        
    def test_itIsPossibleToUpdateRelationshipType(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, data={'relationship_type_id': self.relationship_type2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.relationship_type, self.relationship_type2)
        
    def test_itIsNotPossibleToUpdateConsumer(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, data={'consumer': self.consumer2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.consumer, self.consumer)

class IdentitySerializerTestCase(APITestCase):
    owner = None
    owner2 = None
    gender = None
    gender2 = None
    identity = None
    name_context = None
    identity_name = None
    identity_serializer = None
    
    def setUp(self):
        self.owner = UserFactory.create(username="owner", password="testpassword")
        self.owner2 = UserFactory.create(username="owner2", password="testpassword")
        self.gender = GenderFactory.create(name="Male")
        self.gender2 = GenderFactory.create(name="Female")
        self.identity = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.name_context = NameContextFactory.create(name="First Name")
        self.identity_name = IdentityNameFactory.create(identity=self.identity, name_context=self.name_context, name_value="John", is_default=True)
        self.identity_serializer = IdentitySerializer(instance=self.identity)        
        
    def tearDown(self):
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        AuthUser.objects.all().delete()
        Gender.objects.all().delete()
        NameContext.objects.all().delete()
        
        IdentityNameFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        UserFactory.reset_sequence()
        GenderFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        
    def test_ownerIsReadOnly(self):
        serializer = IdentitySerializer(instance=self.identity, data={'owner': self.owner2.username}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.owner, self.owner)
        
    def test_genderIsReadOnly(self):
        serializer = IdentitySerializer(instance=self.identity, data={'gender': self.gender2.name}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.gender, self.gender)
        
    def test_namesIsReadOnly(self):
        original_names = self.identity_serializer.data['names']
    
        serializer = IdentitySerializer(
            instance=self.identity, 
            data={'names': []}, 
            partial=True
        )
    
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
               
        new_serializer = IdentitySerializer(instance=updated_identity)
        self.assertEqual(new_serializer.data['names'], original_names)
        
    def test_genderIdIsWriteOnly(self):
        data = self.identity_serializer.data
        self.assertNotIn('gender_id', data)
        
    def test_namesListIsWriteOnly(self):
        data = self.identity_serializer.data
        self.assertNotIn('names_list', data)
        
    def test_createIdentityRequiresOwnerAndIsPublicAndGenderIdAndNamesList(self):
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'is_public': True, 'gender_id': self.gender.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'is_public': True, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name'}]})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name'}]})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name'}]})      
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())
        
    def test_createIdentityRequiresAtLeastOneDefaultName(self):
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': False}]})
        self.assertFalse(serializer.is_valid())
        
    def test_createIdentityRequiresUniqueNameContexts(self):
        serializer = IdentitySerializer(data={'owner_id': self.owner.id, 'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name 1', 'is_default': True}, {'name_context_id': self.name_context.id, 'name_value': 'New Name 2', 'is_default': False}]})
        self.assertFalse(serializer.is_valid())
        
    def test_genderCanBeUpdated(self):
        serializer = IdentitySerializer(instance=self.identity, data={'gender_id': self.gender2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.gender, self.gender2)
    
    def test_isPublicCanBeUpdated(self):
        serializer = IdentitySerializer(instance=self.identity, data={'is_public': True}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.is_public, True)
        
    def test_ownerCannotBeUpdated(self):
        serializer = IdentitySerializer(instance=self.identity, data={'owner_id': self.owner2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.owner, self.owner)
        
    def test_namesListCannotBeUpdated(self):
        serializer = IdentitySerializer(instance=self.identity, data={'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'Updated Name', 'is_default': True}]}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.names.count(), 1)
        self.assertEqual(updated_identity.names.first().name_value, "John")
        
class GenderAPITestCase(APITestCase):
    gender1 = None
    gender2 = None
    superuser = None
    user = None
    
    def setUp(self):
        self.gender1 = GenderFactory.create(name="Male")    
        self.gender2 = GenderFactory.create(name="Female")
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        self.user = UserFactory.create(username="user", password="testpassword")
        
    def buildUrl(self, id=None):
        if id is not None:
            return reverse('gender-detail', kwargs={'pk': id})
        return reverse('gender-list')
    
    def tearDown(self):
        Gender.objects.all().delete()
        AuthUser.objects.all().delete()
        
        GenderFactory.reset_sequence()
        UserFactory.reset_sequence()
        
    def test_getGenders(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
        names = [item['name'] for item in response.data['results']]
        self.assertIn(self.gender1.name, names)
        self.assertIn(self.gender2.name, names)
    
    def test_getGenderById(self):
        response = self.client.get(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.gender1.id)
        self.assertEqual(response.data['name'], self.gender1.name)
        
    def test_createGenderAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Non-Binary'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Non-Binary')
        
    def test_createGenderAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Non-Binary'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createGenderWithoutAuthentication(self):
        data = {'name': 'Non-Binary'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 401)
        
    def test_updateGenderAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Gender'}
        response = self.client.patch(self.buildUrl(id=self.gender1.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Gender')
        
    def test_updateGenderAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Gender'}
        response = self.client.patch(self.buildUrl(id=self.gender1.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_updateGenderWithoutAuthentication(self):
        data = {'name': 'Updated Gender'}
        response = self.client.patch(self.buildUrl(id=self.gender1.id), data, format='json')
        
        self.assertEqual(response.status_code, 401)
        
    def test_deleteGenderAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteGenderAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_deleteGenderWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 401)
        
class NameContextAPITestCase(APITestCase):
    name_context1 = None
    name_context2 = None
    superuser = None
    user = None
    
    def setUp(self):
        self.name_context1 = NameContextFactory.create(name="First Name")    
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        self.user = UserFactory.create(username="user", password="testpassword")
        
    def buildUrl(self, id=None):
        if id is not None:
            return reverse('name-context-detail', kwargs={'pk': id})
        return reverse('name-context-list')
    
    def tearDown(self):
        NameContext.objects.all().delete()
        AuthUser.objects.all().delete()
        
        NameContextFactory.reset_sequence()
        UserFactory.reset_sequence()
        
    def test_getNameContexts(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
        names = [item['name'] for item in response.data['results']]
        self.assertIn(self.name_context1.name, names)
        self.assertIn(self.name_context2.name, names)
        
    def test_getNameContextById(self):
        response = self.client.get(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.name_context1.id)
        self.assertEqual(response.data['name'], self.name_context1.name)
        
    def test_createNameContextAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Middle Name'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Middle Name')
        
    def test_createNameContextAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Middle Name'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 403)
    
    def test_createNameContextWithoutAuthentication(self):
        data = {'name': 'Middle Name'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_updateNameContextAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Name Context'}
        response = self.client.patch(self.buildUrl(id=self.name_context1.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Name Context')
        
    def test_updateNameContextAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Name Context'}
        response = self.client.patch(self.buildUrl(id=self.name_context1.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
    
    def test_updateNameContextWithoutAuthentication(self):
        data = {'name': 'Updated Name Context'}
        response = self.client.patch(self.buildUrl(id=self.name_context1.id), data, format='json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_deleteNameContextAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteNameContextAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 403)
    
    def test_deleteNameContextWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 401)
    
class RelationshipTypeAPITestCase(APITestCase):
    relationship_type1 = None
    relationship_type2 = None
    superuser = None
    user = None
    
    def setUp(self):
        self.relationship_type1 = RelationshipTypeFactory.create(name="Parent")    
        self.relationship_type2 = RelationshipTypeFactory.create(name="Sibling")
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        self.user = UserFactory.create(username="user", password="testpassword")
        
    def buildUrl(self, id=None):
        if id is not None:
            return reverse('relationship-type-detail', kwargs={'pk': id})
        return reverse('relationship-type-list')
    
    def tearDown(self):
        RelationshipType.objects.all().delete()
        AuthUser.objects.all().delete()
        
        RelationshipTypeFactory.reset_sequence()
        UserFactory.reset_sequence()
        
    def test_getRelationshipTypes(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
        names = [item['name'] for item in response.data['results']]
        self.assertIn(self.relationship_type1.name, names)
        self.assertIn(self.relationship_type2.name, names)
    
    def test_getRelationshipTypeById(self):
        response = self.client.get(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.relationship_type1.id)
        self.assertEqual(response.data['name'], self.relationship_type1.name)
        
    def test_createRelationshipTypeAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Cousin'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Cousin')
        
    def test_createRelationshipTypeAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Cousin'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 403)
    
    def test_createRelationshipTypeWithoutAuthentication(self):
        data = {'name': 'Cousin'}
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_updateRelationshipTypeAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Relationship Type'}
        response = self.client.patch(self.buildUrl(id=self.relationship_type1.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Relationship Type')
        
    def test_updateRelationshipTypeAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Relationship Type'}
        response = self.client.patch(self.buildUrl(id=self.relationship_type1.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
    
    def test_updateRelationshipTypeWithoutAuthentication(self):
        data = {'name': 'Updated Relationship Type'}
        response = self.client.patch(self.buildUrl(id=self.relationship_type1.id), data, format='json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_deleteRelationshipTypeAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteRelationshipTypeAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 403)
    
    def test_deleteRelationshipTypeWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 401)
     
class IdentityNameAccessTestCase(APITestCase):
    relationship_type = None
    relationship_type2 = None
    name_context = None
    identity_name_access = None
    superuser = None
    user = None
    
    def setUp(self):
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.relationship_type2 = RelationshipTypeFactory.create(name="Sibling")
        self.name_context = NameContextFactory.create(name="First Name")
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.identity_name_access = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type,
            name_context=self.name_context
        )
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        self.user = UserFactory.create(username="user", password="testpassword")
        
    def buildUrl(self, id=None):
        if id is not None:
            return reverse('identity-name-access-detail', kwargs={'pk': id})
        return reverse('identity-name-access-list')
    
    def tearDown(self):
        RelationshipType.objects.all().delete()
        NameContext.objects.all().delete()
        IdentityNameAccess.objects.all().delete()
        AuthUser.objects.all().delete()
        
        RelationshipTypeFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        IdentityNameAccessFactory.reset_sequence()
        UserFactory.reset_sequence()
        
    def test_getIdentityNameAccesses(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['relationship_type'], self.relationship_type.name)
        self.assertEqual(response.data['results'][0]['name_context'], self.name_context.name)
        
    def test_getIdentityNameAccessById(self):
        response = self.client.get(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.identity_name_access.id)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        self.assertEqual(response.data['name_context'], self.name_context.name)
        
    def test_createNonUniqueIdentityNameAccess(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type.id,
            'name_context_id': self.name_context.id
        }
        response = self.client.post(self.buildUrl(), data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_createIdentityNameAccessAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type2.id,
            'name_context_id': self.name_context.id
        }
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        self.assertEqual(response.data['name_context'], self.name_context.name)
    
    def test_createIdentityNameAccessAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'relationship_type_id': self.relationship_type.id,
            'name_context_id': self.name_context2.id
        }        
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createIdentityNameAccessWithoutAuthentication(self):
        data = {
            'relationship_type_id': self.relationship_type2.id,
            'name_context_id': self.name_context.id
        }
        response = self.client.post(self.buildUrl(), data, format='json')
        
        self.assertEqual(response.status_code, 401)
        
    def test_updateIdentityNameAccessAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type2.id,
            'name_context_id': self.name_context2.id
        }
        response = self.client.patch(self.buildUrl(id=self.identity_name_access.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        self.assertEqual(response.data['name_context'], self.name_context2.name)
        
    def test_updateIdentityNameAccessAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name_context_id': self.name_context.id
        }
        response = self.client.patch(self.buildUrl(id=self.identity_name_access.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
    
    def test_updateIdentityNameAccessWithoutAuthentication(self):
        data = {
            'name_context_id': self.name_context2.id
        }
        response = self.client.patch(self.buildUrl(id=self.identity_name_access.id), data, format='json')
        
        self.assertEqual(response.status_code, 401)
      
    def test_deleteIdentityNameAccessAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteIdentityNameAccessAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 403)
    
    def test_deleteIdentityNameAccessWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 401)
      
class IdentityTestCase(APITestCase):
    owner1 = None
    consumer1 = None
    consumer2 = None
    consumer3 = None
    consumer4 = None
    gender = None
    name_context_work = None
    name_context_school = None
    name_context_personal = None
    relationship_type_parent = None
    relationship_type_teacher = None
    relationship_type_colleague = None
    relationship_type_friend = None
    access_work = None
    access_school = None
    access_friend = None
    access_family = None
    identity1 = None
    identity1_name_work = None
    identity1_name_school = None
    identity1_name_personal = None
    identity1_rel_parent = None
    identity1_rel_teacher = None
    identity1_rel_colleague = None
    identity2 = None
    identity2_name_work = None
    identity2_rel_parent = None
    identity3 = None
    identity3_name_school = None
    identity3_name_personal = None
    superuser = None
    
    def setUp(self):
        self.owner1 = AuthUser.objects.create_user(username="testuser", password="testpassword")
        self.consumer1 = AuthUser.objects.create_user(username="testuser1", password="testpassword")
        self.consumer2 = AuthUser.objects.create_user(username="testuser2", password="testpassword")
        self.consumer3 = AuthUser.objects.create_user(username="testuser3", password="testpassword")
        self.consumer4 = AuthUser.objects.create_user(username="testuser4", password="testpassword")
        
        self.gender = GenderFactory.create(name="Male")
        
        self.name_context_work = NameContextFactory.create(name="Work")
        self.name_context_school = NameContextFactory.create(name="School")
        self.name_context_personal = NameContextFactory.create(name="Personal")
        
        self.relationship_type_parent = RelationshipTypeFactory.create(name="Parent")
        self.relationship_type_teacher = RelationshipTypeFactory.create(name="Teacher")
        self.relationship_type_colleague = RelationshipTypeFactory.create(name="Coworker")
        self.relationship_type_friend = RelationshipTypeFactory.create(name="Friend")    
        
        self.access_work = IdentityNameAccessFactory.create(relationship_type=self.relationship_type_colleague, name_context=self.name_context_work)
        self.access_school = IdentityNameAccessFactory.create(relationship_type=self.relationship_type_teacher, name_context=self.name_context_school)
        self.access_friend = IdentityNameAccessFactory.create(relationship_type=self.relationship_type_friend, name_context=self.name_context_personal)
        self.access_family = IdentityNameAccessFactory.create(relationship_type=self.relationship_type_parent, name_context=self.name_context_personal)
            
        
        self.identity1 = IdentityFactory.create(owner=self.owner1, gender=self.gender, is_public=False)
        self.identity_name_work = IdentityName.objects.create(
            identity=self.identity1,
            name_context_id=self.name_context_work.id,
            name_value="Work Name",
            is_default=True
        )
        self.identity1_name_school = IdentityName.objects.create(
            identity=self.identity1,
            name_context_id=self.name_context_school.id,
            name_value="School Name",
            is_default=False
        )
        self.identity1_name_personal = IdentityName.objects.create(
            identity=self.identity1,
            name_context_id=self.name_context_personal.id,
            name_value="Personal Name",
            is_default=False
        )
        self.identity1_rel_parent = IdentityRelationship.objects.create(
            identity=self.identity1,
            consumer=self.consumer1,
            relationship_type=self.relationship_type_parent
        )
        self.identity1_rel_teacher = IdentityRelationship.objects.create(
            identity=self.identity1,
            consumer=self.consumer2,
            relationship_type=self.relationship_type_teacher
        )
        self.identity1_rel_colleague = IdentityRelationship.objects.create(
            identity=self.identity1,
            consumer=self.consumer3,
            relationship_type=self.relationship_type_colleague
        )
        
        self.identity2 = IdentityFactory.create(owner=self.owner1, gender=self.gender, is_public=False)
        self.identity2_name_work = IdentityName.objects.create(
            identity=self.identity2,
            name_context_id=self.name_context_work.id,
            name_value="Work Name",
            is_default=True
        )        
        self.identity2_rel_parent = IdentityRelationship.objects.create(
            identity=self.identity2,
            consumer=self.consumer4,
            relationship_type=self.relationship_type_parent
        )
        
        self.identity3 = IdentityFactory.create(owner=self.consumer4, gender=self.gender, is_public=True)
        self.identity3_name_school = IdentityName.objects.create(
            identity=self.identity3,
            name_context_id=self.name_context_school.id,
            name_value="School Name",
            is_default=True
        )
        
        self.identity3_name_personal = IdentityName.objects.create(
            identity=self.identity3,
            name_context_id=self.name_context_personal.id,
            name_value="Personal Name",
            is_default=False
        )
        
        self.superuser = AuthUser.objects.create_superuser(username="superuser", password="testpassword")
        
    def build_url(self, id=None):
        if id is not None:
            return reverse('identity-detail', kwargs={'pk': id})
        return reverse('identity-list')
        
    def tearDown(self):
        Identity.objects.all().delete()
        AuthUser.objects.all().delete()
        Gender.objects.all().delete()
        NameContext.objects.all().delete()
        RelationshipType.objects.all().delete()
        IdentityNameAccess.objects.all().delete()
    
    def test_getIdentityAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getPublicIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.build_url(id=self.identity3.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getPublicIdentityWithoutAuthentication(self):
        response = self.client.get(self.build_url(id=self.identity3.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getPrivateIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getPrivateIdentityWithoutAuthentication(self):
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getBothPublicAndOwnIdentitiesAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.build_url())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertIn(self.identity1.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity2.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity3.id, [item['id'] for item in response.data['results']])
    
    def test_getBothRelatedAndPublicIdentitiesAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.build_url())

        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn(self.identity1.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity3.id, [item['id'] for item in response.data['results']])

    def test_createIdentityAsAuthenticatedUser(self):
        self.client.force_authenticate(user=self.owner1)
        data = {
            'owner_id': self.owner1.id,
            'gender_id': self.gender.id,
            'is_public': True,
            'names_list': [
                {
                    'name_context_id': self.name_context_work.id,
                    'name_value': 'New Work Name',
                    'is_default': True
                }
            ]}
        
        response = self.client.post(self.build_url(), data, format='json')
        self.assertEqual(response.status_code, 201)
        
        response = self.client.get(self.build_url(id=response.data['id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], self.owner1.username)
        self.assertEqual(response.data['gender'], self.gender.name)
        self.assertEqual(response.data['is_public'], data['is_public'])
        self.assertEqual(len(response.data['names']), 1)

    def test_createIdentityWithoutAuthentication(self):
        data = {
            'owner_id': self.owner1.id,
            'gender_id': self.gender.id,
            'is_public': True,
            'names_list': [
                {
                    'name_context_id': self.name_context_work.id,
                    'name_value': 'New Work Name',
                    'is_default': True
                }
            ]}
        
        response = self.client.post(self.build_url(), data, format='json')
        self.assertEqual(response.status_code, 401)
        
    def test_correctNamesReturnedForRelatedConsumer(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 1)
        self.assertEqual(response.data['names'][0]['name_context'], self.name_context_personal.name)
        self.assertEqual(response.data['names'][0]['name_value'], "Personal Name")
        
    def test_allNamesReturnedForOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 3)
        name_contexts = [item['name_context'] for item in response.data['names']]
        self.assertIn(self.name_context_work.name, name_contexts)
        self.assertIn(self.name_context_school.name, name_contexts)
        self.assertIn(self.name_context_personal.name, name_contexts)
        
    def test_allNamesReturnedForSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 3)
        name_contexts = [item['name_context'] for item in response.data['names']]
        self.assertIn(self.name_context_work.name, name_contexts)
        self.assertIn(self.name_context_school.name, name_contexts)
        self.assertIn(self.name_context_personal.name, name_contexts)
        
    def test_allNamesReturnedForPublicIdentity(self):
        response = self.client.get(self.build_url(id=self.identity3.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 2)
        name_contexts = [item['name_context'] for item in response.data['names']]
        self.assertIn(self.name_context_school.name, name_contexts)
        self.assertIn(self.name_context_personal.name, name_contexts)     
           
    def test_updateIdentityAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.build_url(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_public'], True)
    
    def test_updateIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.build_url(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_public'], True)
        
    def test_updateIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.build_url(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 403)
    
    def test_updateIdentityWithoutAuthentication(self):
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.build_url(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 401)
        
    def test_deleteIdentityAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        
        response = self.client.delete(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        
        response = self.client.delete(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityWithoutAuthentication(self):
        response = self.client.delete(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 401)
        
    def test_deleteIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        
        response = self.client.delete(self.build_url(id=self.identity1.id))
        self.assertEqual(response.status_code, 403)
                
        