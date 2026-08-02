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
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'name_context': self.name_context2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context1)
        
    def test_identityFieldIsReadOnly(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'identity': self.identity2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.identity, self.identity1)
        
    def test_nameContextIdIsWriteOnly(self):
        data = self.identity_name_serializer.data
        self.assertNotIn('name_context_id', data)
        
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'name_context_id': self.name_context2.id}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context2)
        
    def test_createNameRequiresIdentityAndValueAndContext(self):
        serializer = IdentityNameSerializer(data={'name_value': 'New Name', 'name_context_id': self.name_context1.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={ 'name_value': 'New Name'})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={'name_context_id': self.name_context1.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={'name_context_id': self.name_context2.id, 'name_value': 'New Name'})
        self.assertTrue(serializer.is_valid())
        
    def test_onlyOneDefaultNamePerIdentity(self):
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={
            'identity_id': self.identity1.id,
            'name_context_id': self.name_context2.id,
            'name_value': 'Another Name',
            'is_default': True
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Only one default name is allowed.', str(serializer.errors))
        
    def test_nameContextIdMustBeValid(self):
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={
            'name_context_id': 9999,
            'name_value': 'Invalid Context'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_identityIdMustBeValid(self):
        serializer = IdentityNameSerializer(context={'identity_pk': 9999},data={'name_context_id': self.name_context1.id, 'name_value': 'Invalid Identity'})
        
        self.assertFalse(serializer.is_valid())
        self.assertIn('Identity does not exist.', str(serializer.errors))
        
    def test_nameHasToBeUniquePerIdentity(self):
        serializer = IdentityNameSerializer(context={'identity_pk': self.identity1.id}, data={
            'name_context_id': self.name_context1.id,
            'name_value': 'John'
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('A name with this context already exists in this identity.', str(serializer.errors))
        
    def test_itIsPossibleToUpdateNameValue(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'name_value': 'Updated Name'}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_value, 'Updated Name')
        
    def test_itIsPossibleToUpdateNameContext(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'name_context_id': self.name_context2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context2)
        
    def test_itIsPossibleToUpdateToSameNameContext(self):
        serializer = IdentityNameSerializer(instance=self.identity_name1, context={'identity_pk': self.identity1.id}, data={'name_context_id': self.name_context1.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        
        self.assertEqual(updated_name.name_context, self.name_context1)

    def test_itIsNotPossibleToUpdateToNonUniqueNameContext(self):
        serializer = IdentityNameSerializer(
            instance=self.identity_name2,
            context={'identity_pk': self.identity1.id},
            data={'name_context_id': self.name_context1.id},
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('A name with this context already exists in this identity.', str(serializer.errors))
        
    def test_itIsPossibleToUpdateIsDefaultToTrue(self):
        self.assertEqual(self.identity_name3.is_default, True)
        
        serializer = IdentityNameSerializer(instance=self.identity_name2, context={'identity_pk': self.identity2.id}, data={'is_default': True}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_name = serializer.save()
        self.identity_name3.refresh_from_db()
        
        self.assertEqual(updated_name.is_default, True)
        
        # previously default name is switched to False
        self.assertEqual(self.identity_name3.is_default, False)
        self.assertEqual(IdentityName.objects.filter(identity=self.identity2, is_default=True).count(), 1)

    def test_itIsNotPossibleToUpdateIsDefaultToFalseOnTheDefaultName(self):
        serializer = IdentityNameSerializer(instance=self.identity_name3, context={'identity_pk': self.identity2.id}, data={'is_default': False}, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn('Cannot unset the default name. Set another name as default instead.', str(serializer.errors))

        self.identity_name3.refresh_from_db()
        self.assertEqual(self.identity_name3.is_default, True)
        self.assertEqual(IdentityName.objects.filter(identity=self.identity2, is_default=True).count(), 1)

    def test_itIsPossibleToUpdateIsDefaultToFalseOnANonDefaultName(self):
        serializer = IdentityNameSerializer(instance=self.identity_name2, context={'identity_pk': self.identity2.id}, data={'is_default': False}, partial=True)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.save().is_default, False)
        self.assertEqual(IdentityName.objects.filter(identity=self.identity2, is_default=True).count(), 1)

    def test_hasToPromoteAnotherNameToRemoveDefault(self):
        serializer = IdentityNameSerializer(instance=self.identity_name2, context={'identity_pk': self.identity2.id}, data={'is_default': True}, partial=True)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.identity_name3.refresh_from_db()

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
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'relationship_type': 'Sibling'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.relationship_type, self.relationship_type)
        
    def test_consumerIsReadOnly(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'consumer_username': self.consumer2.username}, partial=True)

        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()

        self.assertEqual(updated_relationship.consumer, self.consumer)

    def test_createRelationshipWithConsumerUsername(self):
        serializer = IdentityRelationshipSerializer(
            context={'identity_pk': self.identity.id},
            data={'consumer_username': self.consumer2.username, 'relationship_type_id': self.relationship_type.id}
        )

        self.assertTrue(serializer.is_valid())
        new_relationship = serializer.save()

        self.assertEqual(new_relationship.consumer, self.consumer2)
        self.assertEqual(new_relationship.identity, self.identity)

    def test_createRelationshipWithUnknownConsumerUsername(self):
        serializer = IdentityRelationshipSerializer(
            context={'identity_pk': self.identity.id},
            data={'consumer_username': 'nobody_by_that_name', 'relationship_type_id': self.relationship_type.id}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('consumer_username', serializer.errors)

    def test_createRelationshipRequiresConsumerIdOrUsername(self):
        serializer = IdentityRelationshipSerializer(
            context={'identity_pk': self.identity.id},
            data={'relationship_type_id': self.relationship_type.id}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('Consumer (consumer_id or consumer_username), identity and relationship type fields are required.', str(serializer.errors))

    def test_createRelationshipAcceptsConsumerIdAndUsernameWhenTheyAgree(self):
        serializer = IdentityRelationshipSerializer(
            context={'identity_pk': self.identity.id},
            data={'consumer_id': self.consumer2.id, 'consumer_username': self.consumer2.username, 'relationship_type_id': self.relationship_type.id}
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.save().consumer, self.consumer2)

    def test_createRelationshipRejectsConflictingConsumerIdAndUsername(self):
        serializer = IdentityRelationshipSerializer(
            context={'identity_pk': self.identity.id},
            data={'consumer_id': self.consumer2.id, 'consumer_username': self.consumer.username, 'relationship_type_id': self.relationship_type.id}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn('Consumer_id and consumer_username refer to different users.', str(serializer.errors))

    def test_consumerUsernameIsReturnedOnRead(self):
        self.assertEqual(self.identity_relationship_serializer.data['consumer_username'], self.consumer.username)

    def test_identityOwnerFieldIsReadOnly(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'identity_owner': 'new_owner'}, partial=True)
        
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.identity.owner, self.owner)
        
    def test_accessibleNamesFieldIsReadOnly(self):
        original_data = self.identity_relationship_serializer.data
        original_accessible_names = original_data['accessible_names']
    
        serializer = IdentityRelationshipSerializer(
            instance=self.identity_relationship, 
            context={'identity_pk': self.identity.id},
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
        serializer = IdentityRelationshipSerializer(data={'consumer_id': self.consumer2.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer2.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer2.id, 'relationship_type_id': self.relationship_type.id})
        self.assertTrue(serializer.is_valid())
              
    def test_consumerIdHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': 9999, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
        
    def test_relationshipTypeHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer.id, 'relationship_type_id': 9999})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Invalid pk "9999" - object does not exist.', str(serializer.errors))
    
    def test_identityIdHasToBeValid(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': 9999}, data={'consumer_id': self.consumer.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Identity does not exist.', str(serializer.errors))   
             
    def test_consumerCannotEqualOwner(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id},data={'consumer_id': self.owner.id, 'relationship_type_id': self.relationship_type.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Owner cannot have a relationship to itself.', str(serializer.errors))
        
    def test_consumerIdMapsToConsumerOnCreation(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer2.id, 'relationship_type_id': self.relationship_type.id})
        self.assertTrue(serializer.is_valid())
        
        new_relationship = serializer.save()
        self.assertEqual(new_relationship.consumer, self.consumer2)
        
    def test_onlyOneRelationshipPerConsumerAndIdentity(self):
        serializer = IdentityRelationshipSerializer(context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer.id, 'relationship_type_id': self.relationship_type2.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('A relationship between this identity and consumer already exists.', str(serializer.errors))
        
    def test_itIsPossibleToUpdateRelationshipType(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'relationship_type_id': self.relationship_type2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()
        
        self.assertEqual(updated_relationship.relationship_type, self.relationship_type2)
        
    def test_itIsNotPossibleToUpdateConsumer(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()

        self.assertEqual(updated_relationship.consumer, self.consumer)

    def test_updateWithSameConsumer(self):
        serializer = IdentityRelationshipSerializer(instance=self.identity_relationship, context={'identity_pk': self.identity.id}, data={'consumer_id': self.consumer.id, 'relationship_type_id': self.relationship_type2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_relationship = serializer.save()

        self.assertEqual(updated_relationship.consumer, self.consumer)
        self.assertEqual(updated_relationship.relationship_type, self.relationship_type2)

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
        
    # helper for request
    def make_request(self, user):
        factory = APIRequestFactory()
        request = factory.post('/')
        request.user = user
        return request
        
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
        
    def test_createIdentityRequiresNamesListWithExactlyOneDefault(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id})
        self.assertFalse(serializer.is_valid())
        self.assertIn('At least one name must be provided.', str(serializer.errors))

        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': []})
        self.assertFalse(serializer.is_valid())

        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name'}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Exactly one default name must be provided.', str(serializer.errors))

        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())

    def test_createIdentityWithoutIsPublicDefaultsToFalse(self):
        request = self.make_request(self.owner)
        serializer = IdentitySerializer(context={'request': request}, data={'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())

        new_identity = serializer.save()
        self.assertEqual(new_identity.is_public, False)

    def test_createIdentityRejectsNullIsPublic(self):
        serializer = IdentitySerializer(data={'is_public': None, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn('is_public', serializer.errors)

    def test_createIdentityRequiresAtLeastOneDefaultName(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': False}]})
        self.assertFalse(serializer.is_valid())
        
    def test_createIdentityRequiresUniqueNameContexts(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name 1', 'is_default': True}, {'name_context_id': self.name_context.id, 'name_value': 'New Name 2', 'is_default': False}]})
        self.assertFalse(serializer.is_valid())
        
    def test_createIdentityRequiresValidGenderId(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': 9999, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        
    def test_createIdentityRequiresKnownNameContextId(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': 9999999, 'name_value': 'New Name', 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn('Unknown name_context_id', str(serializer.errors))

    def test_createIdentityRequiresNameValueInNamesList(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Each name must have a 'name_context_id' and 'name_value'.", str(serializer.errors))

    def test_createIdentityDoesNotLeaveEmptyIdentityWhenANameFails(self):
        request = self.make_request(self.owner)
        identities_before = Identity.objects.count()
        serializer = IdentitySerializer(context={'request': request}, data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': 9999999, 'name_value': 'New Name', 'is_default': True}]})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(Identity.objects.count(), identities_before)

    def test_createIdentityRejectsNameValueOver100Chars(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'x' * 101, 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn('at most 100 characters', str(serializer.errors))

    def test_createIdentityAcceptsNameValueOfExactly100Chars(self):
        request = self.make_request(self.owner)
        serializer = IdentitySerializer(context={'request': request}, data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'x' * 100, 'is_default': True}]})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.save().names.first().name_value, 'x' * 100)

    def test_createIdentityRejectsNonStringNameValue(self):
        serializer = IdentitySerializer(data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 12345, 'is_default': True}]})
        self.assertFalse(serializer.is_valid())
        self.assertIn("must be a string", str(serializer.errors))

    def test_createIdentityIgnoresPayloadOwnerAndUsesAuthenticatedUser(self):
        serializer = IdentitySerializer(data={'owner_id': 9999, 'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('owner_id', serializer.validated_data)

    def test_publicIdentityCanBeCreated(self):
        request = self.make_request(self.owner)
        serializer = IdentitySerializer(context={'request': request}, data={'is_public': True, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())
        
        new_identity = serializer.save()
        self.assertEqual(new_identity.is_public, True)
        
    def test_privateIdentityCanBeCreated(self):
        request = self.make_request(self.owner)
        serializer = IdentitySerializer(context={'request': request}, data={'is_public': False, 'gender_id': self.gender.id, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())

        new_identity = serializer.save()
        self.assertEqual(new_identity.is_public, False)
        
    def test_genderCanBeUpdated(self):
        serializer = IdentitySerializer(instance=self.identity, data={'gender_id': self.gender2.id}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()
        
        self.assertEqual(updated_identity.gender, self.gender2)
    
    def test_genderCanBeUpdatedToNull(self):
        serializer = IdentitySerializer(instance=self.identity, data={'gender_id': None}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()

        self.assertIsNone(updated_identity.gender)

    def test_genderIsKeptWhenGenderIdIsNotInThePayload(self):
        serializer = IdentitySerializer(instance=self.identity, data={'is_public': True}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_identity = serializer.save()

        self.assertEqual(updated_identity.gender, self.gender)

    def test_createIdentityWithNullGender(self):
        request = self.make_request(self.owner)
        serializer = IdentitySerializer(context={'request': request}, data={'is_public': False, 'gender_id': None, 'names_list': [{'name_context_id': self.name_context.id, 'name_value': 'New Name', 'is_default': True}]})
        self.assertTrue(serializer.is_valid())

        self.assertIsNone(serializer.save().gender)

    def test_nullGenderIsReturnedAsNull(self):
        self.identity.gender = None
        self.identity.save()
        data = IdentitySerializer(instance=self.identity).data

        self.assertIn('gender', data)
        self.assertIsNone(data['gender'])

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
        
    def test_getGenderByWrongId(self):
        response = self.client.get(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
        
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
        
    def test_updateGenderWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Gender'}
        response = self.client.patch(self.buildUrl(id=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)
        
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
        
    def test_deleteGenderWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
        
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
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        NameContext.objects.all().delete()
        AuthUser.objects.all().delete()

        NameContextFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        IdentityNameFactory.reset_sequence()
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
        
    def test_getNameContextByWrongId(self):
        response = self.client.get(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
        
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
        
    def test_updateNameContextWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Name Context'}
        response = self.client.patch(self.buildUrl(id=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)
    
    def test_deleteNameContextAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteNameContextOfADefaultNameIsBlocked(self):
        identity = IdentityFactory.create(owner=self.user, is_public=False)
        IdentityNameFactory.create(identity=identity, name_context=self.name_context1, name_value="John", is_default=True)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))

        self.assertEqual(response.status_code, 400)
        self.assertIn('Cannot delete this name context. It holds the default name of at least one identity.', str(response.data))
        self.assertTrue(NameContext.objects.filter(pk=self.name_context1.pk).exists())
        self.assertEqual(identity.names.count(), 1)

    def test_deleteNameContextOfOnlyNonDefaultNamesIsAllowed(self):
        identity = IdentityFactory.create(owner=self.user, is_public=False)
        IdentityNameFactory.create(identity=identity, name_context=self.name_context1, name_value="John", is_default=True)
        secondary = IdentityNameFactory.create(identity=identity, name_context=self.name_context2, name_value="Johnny", is_default=False)

        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.name_context2.id))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(IdentityName.objects.filter(pk=secondary.pk).exists())
        self.assertTrue(Identity.objects.filter(pk=identity.pk).exists())
        self.assertEqual(identity.names.count(), 1)
        self.assertEqual(identity.names.first().is_default, True)

    def test_deleteNameContextAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))

        self.assertEqual(response.status_code, 403)
    
    def test_deleteNameContextWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 401)
        
    def test_deleteNameContextWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
    
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
        
    def test_getRelationshipTypeByWrongId(self):
        response = self.client.get(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
        
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
        
    def test_updateRelationshipTypeWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'Updated Relationship Type'}
        response = self.client.patch(self.buildUrl(id=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)
    
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
        
    def test_deleteRelationshipTypeWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
     
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
        
    def test_getIdentityNameAccessByWrongId(self):
        response = self.client.get(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)
        
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
        
    def test_updateOnlyRelationshipTypeOfIdentityNameAccess(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(id=self.identity_name_access.id), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        self.assertEqual(response.data['name_context'], self.name_context.name)

    def test_updateOnlyNameContextOfIdentityNameAccess(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'name_context_id': self.name_context2.id
        }
        response = self.client.patch(self.buildUrl(id=self.identity_name_access.id), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        self.assertEqual(response.data['name_context'], self.name_context2.name)

    def test_partialUpdateIdentityNameAccessIntoDuplicate(self):
        other_access = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type2,
            name_context=self.name_context
        )
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.patch(self.buildUrl(id=other_access.id), data, format='json')

        self.assertEqual(response.status_code, 400)

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
        
    def test_updateIdentityNameAccessWithWrongId(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'name_context_id': self.name_context2.id
        }
        response = self.client.patch(self.buildUrl(id=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)
      
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
        
    def test_deleteIdentityNameAccessWithWrongId(self):
        self.client.force_authenticate(user=self.superuser) 
        response = self.client.delete(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)

class IdentityNameAPITestCase(APITestCase):
    identity1 = None
    gender = None
    name_context1 = None
    name_context2 = None
    name_context3 = None
    identity_name1 = None
    identity_name2 = None
    relationship_type = None
    identity_relationship = None
    name_access = None
    owner = None
    superuser = None
    user = None
    user2 = None
    public_identity = None
    public_identity_name = None
    public_identity_name2 = None
    
    def setUp(self):
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        self.user = UserFactory.create(username="user", password="testpassword")
        self.user2 = UserFactory.create(username="user2", password="testpassword")
        self.owner = UserFactory.create(username="owner", password="testpassword")
        
        self.gender = GenderFactory.create(name="Male")
        self.name_context1 = NameContextFactory.create(name="First Name")
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.name_context3 = NameContextFactory.create(name="Nickname")
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.name_access = IdentityNameAccessFactory.create(relationship_type=self.relationship_type, name_context=self.name_context1)
        
        self.identity1 = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity_name1 = IdentityNameFactory.create(identity=self.identity1, name_context=self.name_context1, name_value="John", is_default=False)
        self.identity1_name2 = IdentityNameFactory.create(identity=self.identity1, name_context=self.name_context2, name_value="Doe", is_default=True) 
        self.identity_relationship = IdentityRelationshipFactory.create(identity=self.identity1, consumer=self.user, relationship_type=self.relationship_type)
        
        self.public_identity = IdentityFactory.create(owner=self.user2, gender=self.gender, is_public=True)
        self.public_identity_name = IdentityNameFactory.create(identity=self.public_identity, name_context=self.name_context1, name_value="Public Name", is_default=True)
        self.public_identity_name2 = IdentityNameFactory.create(identity=self.public_identity, name_context=self.name_context2, name_value="Public Last Name", is_default=False)
        
    def buildUrl(self, id, nameId):
        if nameId is not None:
            return reverse('identity-name-detail', kwargs={'identity_pk': id, 'pk': nameId})
        return reverse('identity-name-list', kwargs={'identity_pk': id})
    
    def tearDown(self):
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        NameContext.objects.all().delete()
        AuthUser.objects.all().delete()
        
        IdentityNameFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        UserFactory.reset_sequence()
    
    def test_getIdentityNamesAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(self.identity1.id, None))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getIdentityNamesAsRegularUserWithRelationship(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.buildUrl(self.identity1.id, None))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNamesAsRegularUserWithoutRelationship(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.buildUrl(self.identity1.id, None))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNamesWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(self.identity1.id, None))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNamesAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(self.identity1.id, None))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getIdentityNamesWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(9999, None))
        
        self.assertEqual(response.status_code, 404)

    def test_getIdentityNameByIdAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.identity_name1.id)
        self.assertEqual(response.data['name_value'], self.identity_name1.name_value)
        self.assertEqual(response.data['name_context'], self.identity_name1.name_context.name)
        
    def test_getIdentityNameByIdAsRegularUserWithRelationship(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNameByIdAsRegularUserWithoutRelationship(self):        
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNameByIdWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityNameByIdAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.identity_name1.id)
        self.assertEqual(response.data['name_value'], self.identity_name1.name_value)
        self.assertEqual(response.data['name_context'], self.identity_name1.name_context.name)
        
    def test_getNamesOfPublicIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.buildUrl(self.public_identity.id, None))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getNamesOfPublicIdentityWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(self.public_identity.id, None))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getNameOfPublicIdentityByIdAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.buildUrl(self.public_identity.id, self.public_identity_name.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.public_identity_name.id)
        self.assertEqual(response.data['name_value'], self.public_identity_name.name_value)
        self.assertEqual(response.data['name_context'], self.public_identity_name.name_context.name)
        
    def test_getNameOfPublicIdentityByIdWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(self.public_identity.id, self.public_identity_name.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.public_identity_name.id)
        self.assertEqual(response.data['name_value'], self.public_identity_name.name_value)
        self.assertEqual(response.data['name_context'], self.public_identity_name.name_context.name)
        
    def test_getNameOfIdentityByWrongId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(self.identity1.id, 9999))
        
        self.assertEqual(response.status_code, 404)
        
    def test_createIdentityNameAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_context_id': self.name_context3.id,
            'name_value': 'New Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name_value'], 'New Name')
        self.assertEqual(response.data['name_context'], self.name_context3.name)
        
    def test_createIdentityNameAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name_context_id': self.name_context3.id,
            'name_value': 'New Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createIdentityNameWithoutAuthentication(self):
        data = {
            'name_context_id': self.name_context3.id,
            'name_value': 'New Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createIdentityNameAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'name_context_id': self.name_context3.id,
            'name_value': 'New Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name_value'], 'New Name')
        self.assertEqual(response.data['name_context'], self.name_context3.name)
        
    def test_createIdentityNameWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_context_id': self.name_context3.id,
            'name_value': 'New Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(9999, None), data, format='json')
        
        self.assertEqual(response.status_code, 404)
        
    def test_cannotCreateSecondDefaultIdentityName(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_context_id': self.name_context1.id,
            'name_value': 'Another Default',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('Only one default name is allowed.', str(response.data))
        
    def test_cannotCreateIdentityNameWithDuplicateContext(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_context_id': self.name_context1.id,
            'name_value': 'Duplicate Context Name',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity1.id, None), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('A name with this context already exists in this identity.', str(response.data))
        
    def test_updateIdentityNameAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.identity1.id, self.identity_name1.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name_value'], 'Updated Name')
        
    def test_updateIdentityNameAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.identity1.id, self.identity_name1.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_updateIdentityNameWithoutAuthentication(self):
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.identity1.id, self.identity_name1.id), data, format='json')        
        self.assertEqual(response.status_code, 403)
    
    def test_updateIdentityNameAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.identity1.id, self.identity_name1.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name_value'], 'Updated Name')
        
    def test_updateIdentityNameWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(9999, self.identity_name1.id), data, format='json')
        
        self.assertEqual(response.status_code, 404)
        
    def test_updateIdentityNameWithWrongNameId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.identity1.id, 9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)

    def test_updateIdentityNameWithMismatchedIdentityAndNameIds(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'name_value': 'Updated Name'
        }
        response = self.client.patch(self.buildUrl(self.public_identity.id, self.identity_name1.id), data, format='json')

        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityNameAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteIdentityNameAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_deleteIdentityNameWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 403) 
        
    def test_deleteIdentityNameAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(self.identity1.id, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_cannotDeleteDefaultIdentityName(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(self.identity1.id, self.identity1_name2.id))
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("Cannot delete the default name", response.data[0])
        
    def test_deleteIdentityNameWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(9999, self.identity_name1.id))
        
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityNameWithWrongNameId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(self.identity1.id, 9999))
        
        self.assertEqual(response.status_code, 404)

    def test_deleteIdentityNameWithMismatchedIdentityAndNameIds(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(self.public_identity.id, self.identity_name1.id))

        self.assertEqual(response.status_code, 404)

class IdentityAPITestCase(APITestCase):
    owner1 = None
    consumer1 = None
    consumer2 = None
    consumer3 = None
    consumer4 = None
    superuser = None
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
        
    def buildUrl(self, id=None):
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
    
    def test_getIdentityListAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        
    def test_getBothPublicAndOwnIdentitiesAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
        self.assertIn(self.identity1.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity2.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity3.id, [item['id'] for item in response.data['results']])
        
    def test_getBothRelatedAndPublicIdentitiesAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertIn(self.identity1.id, [item['id'] for item in response.data['results']])
        self.assertIn(self.identity3.id, [item['id'] for item in response.data['results']])
        
    def test_getOnlyPublicIdentitiesWithoutAuthentication(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIn(self.identity3.id, [item['id'] for item in response.data['results']])
    
    def test_getIdentityAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getIdentityAsRegularUserWithRelationship(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getIdentityAsRegularUserWithoutRelationship(self):
        self.client.force_authenticate(user=self.consumer4)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getIdentityWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 403) 
        
    def test_getPublicIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.buildUrl(id=self.identity3.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getPublicIdentityWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(id=self.identity3.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_getIdentityListCanBeFilteredByIdentityId(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(f"{self.buildUrl()}?pk={self.identity1.id}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.identity1.id)
        
    def test_getIdentityWithWrongId(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.buildUrl(id=9999))
        
        self.assertEqual(response.status_code, 404)

    def test_createIdentityAsAuthenticatedUser(self):
        self.client.force_authenticate(user=self.owner1)
        data = {
            'gender_id': self.gender.id,
            'is_public': True,
            'names_list': [
                {
                    'name_context_id': self.name_context_work.id,
                    'name_value': 'New Work Name',
                    'is_default': True
                }
            ]}
        
        response = self.client.post(self.buildUrl(), data, format='json')
        self.assertEqual(response.status_code, 201)
        
        response = self.client.get(self.buildUrl(id=response.data['id']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['owner'], self.owner1.username)
        self.assertEqual(response.data['gender'], self.gender.name)
        self.assertEqual(response.data['is_public'], data['is_public'])
        self.assertEqual(len(response.data['names']), 1)

    def test_createIdentityIgnoresPayloadOwnerAndUsesAuthenticatedUser(self):
        self.client.force_authenticate(user=self.owner1)
        data = {
            'owner_id': self.consumer1.id,
            'gender_id': self.gender.id,
            'is_public': True,
            'names_list': [
                {
                    'name_context_id': self.name_context_work.id,
                    'name_value': 'Spoof Attempt Name',
                    'is_default': True
                }
            ]
        }

        response = self.client.post(self.buildUrl(), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['owner'], self.owner1.username)

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
        
        response = self.client.post(self.buildUrl(), data, format='json')
        self.assertEqual(response.status_code, 401)
        
    def test_correctNamesReturnedForRelatedConsumer(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 1)
        self.assertEqual(response.data['names'][0]['name_context'], self.name_context_personal.name)
        self.assertEqual(response.data['names'][0]['name_value'], "Personal Name")
        
    def test_defaultNameReturnedWhenRelatedConsumerButNoRules(self):
        self.client.force_authenticate(user=self.consumer2)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 1)
        self.assertEqual(response.data['names'][0]['name_context'], self.name_context_work.name)
        self.assertEqual(response.data['names'][0]['name_value'], "Work Name")
        
    def test_allNamesReturnedForOwner(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
      
    def test_allNamesReturnedForSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['names']), 3)
        name_contexts = [item['name_context'] for item in response.data['names']]
        self.assertIn(self.name_context_work.name, name_contexts)
        self.assertIn(self.name_context_school.name, name_contexts)
        self.assertIn(self.name_context_personal.name, name_contexts)
        
    def test_allNamesReturnedForPublicIdentity(self):
        response = self.client.get(self.buildUrl(id=self.identity3.id))
        
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
        
        response = self.client.patch(self.buildUrl(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_public'], True)
    
    def test_updateIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.buildUrl(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['is_public'], True)
        
    def test_updateIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.buildUrl(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 403)
    
    def test_updateIdentityWithoutAuthentication(self):
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.buildUrl(id=self.identity1.id), data, format='json')
        self.assertEqual(response.status_code, 401)
        
    def test_updateIdentityWithWrongId(self):
        self.client.force_authenticate(user=self.owner1)
        data = {
            'is_public': True
        }
        
        response = self.client.patch(self.buildUrl(id=9999), data, format='json')
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityAsOwner(self):
        self.client.force_authenticate(user=self.owner1)
        
        response = self.client.delete(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        
        response = self.client.delete(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 204)
        
        response = self.client.get(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 401)
        
    def test_deleteIdentityAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer1)
        
        response = self.client.delete(self.buildUrl(id=self.identity1.id))
        self.assertEqual(response.status_code, 403)
        
    def test_deleteIdentityWithWrongId(self):
        self.client.force_authenticate(user=self.owner1)
        
        response = self.client.delete(self.buildUrl(id=9999))
        self.assertEqual(response.status_code, 404)
                
class IdentityRelationshipAPIestCase(APITestCase):
    owner = None
    consumer = None
    consumer2 = None
    consumer3 = None
    superuser = None
    identity = None
    identity2 = None
    identity_name = None
    relationship_type = None
    relationship_type2 = None
    name_context = None
    name_context2 = None
    identity_relationship = None
    identity_relationship2 = None
    name_access = None
    gender = None
    
    def setUp(self):
        self.owner = UserFactory.create(username="owner", password="testpassword")
        self.consumer = UserFactory.create(username="consumer", password="testpassword")    
        self.consumer2 = UserFactory.create(username="consumer2", password="testpassword")
        self.consumer3 = UserFactory.create(username="consumer3", password="testpassword")
        self.superuser = UserFactory.create(username="superuser", password="testpassword", is_superuser=True)
        
        self.gender = GenderFactory.create(name="Male")
        self.name_context = NameContextFactory.create(name="First Name")
        self.name_context2 = NameContextFactory.create(name="Last Name")
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.relationship_type2 = RelationshipTypeFactory.create(name="Friend")
        self.name_access = IdentityNameAccessFactory.create(relationship_type=self.relationship_type, name_context=self.name_context)
        
        self.identity = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=False)
        self.identity2 = IdentityFactory.create(owner=self.owner, gender=self.gender, is_public=True)
        self.identity_name = IdentityNameFactory.create(identity=self.identity, name_context=self.name_context, name_value="John", is_default=True)
        self.identity_relationship = IdentityRelationshipFactory.create(identity=self.identity, consumer_id=self.consumer.id, relationship_type=self.relationship_type)
        self.identity_relationship2 = IdentityRelationshipFactory.create(identity=self.identity, consumer_id=self.consumer2.id, relationship_type=self.relationship_type)
        
    def tearDown(self):
        IdentityRelationship.objects.all().delete()
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        AuthUser.objects.all().delete()
        Gender.objects.all().delete()
        IdentityNameAccess.objects.all().delete()
        RelationshipType.objects.all().delete()
        NameContext.objects.all().delete()
        
        IdentityRelationshipFactory.reset_sequence()
        IdentityNameFactory.reset_sequence()
        IdentityFactory.reset_sequence()
        UserFactory.reset_sequence()
        GenderFactory.reset_sequence()
        IdentityNameAccessFactory.reset_sequence()
        RelationshipTypeFactory.reset_sequence()
        NameContextFactory.reset_sequence()
        
    def buildUrl(self, identity_pk, relationship_pk=None):
        if relationship_pk is not None:
            return reverse('identity-relationship-detail', kwargs={'identity_pk': identity_pk, 'pk': relationship_pk})
        else:
            return reverse('identity-relationship-list', kwargs={'identity_pk': identity_pk})
        
    def test_getIdentityRelationshipsAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getIdentityRelationshipsAsRegularUserWithRelationship(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipsAsRegularUserWithoutRelationship(self):
        self.client.force_authenticate(user=self.consumer3)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipsWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipsAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        
    def test_getPublicIdentityRelationshipsAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer3)
        response = self.client.get(self.buildUrl(identity_pk=self.identity2.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getPublicIdentityRelationshipsWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(identity_pk=self.identity2.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipsByWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(identity_pk=9999))
        
        self.assertEqual(response.status_code, 404)
      
    def test_getIdentityRelationshipByIdAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.identity_relationship.id)
        self.assertEqual(response.data['consumer_username'], self.consumer.username)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        
    def test_getIdentityRelationshipByIdAsRegularUserWithRelationship(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipByIdAsRegularUserWithoutRelationship(self):
        self.client.force_authenticate(user=self.consumer3)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipByIdWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipByIdAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.identity_relationship.id)
        self.assertEqual(response.data['consumer_username'], self.consumer.username)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        
    def test_getPublicIdentityRelationshipByIdAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer3)
        response = self.client.get(self.buildUrl(identity_pk=self.identity2.id, relationship_pk=self.identity_relationship2.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getPublicIdentityRelationshipByIdWithoutAuthentication(self):
        response = self.client.get(self.buildUrl(identity_pk=self.identity2.id, relationship_pk=self.identity_relationship2.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_getIdentityRelationshipByWrongId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.buildUrl(identity_pk=self.identity.id, relationship_pk=9999))
        
        self.assertEqual(response.status_code, 404)

    def test_getIdentityRelationshipByIdWithMismatchedIdentityPath(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(self.buildUrl(identity_pk=self.identity2.id, relationship_pk=self.identity_relationship.id))

        self.assertEqual(response.status_code, 404)
        
    def test_createIdentityRelationshipAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'consumer_id': self.consumer3.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(identity_pk=self.identity.id), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['consumer_username'], self.consumer3.username)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        
    def test_createIdentityRelationshipAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer)
        data = {
            'consumer_id': self.consumer3.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(identity_pk=self.identity.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createIdentityRelationshipWithoutAuthentication(self):
        data = {
            'consumer_id': self.consumer3.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(identity_pk=self.identity.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_createIdentityRelationshipAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'consumer_id': self.consumer3.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(identity_pk=self.identity.id), data, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['consumer_username'], self.consumer3.username)
        self.assertEqual(response.data['relationship_type'], self.relationship_type.name)
        
    def test_createIdentityRelationshipWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'consumer_id': self.consumer3.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(identity_pk=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)

    def test_createDuplicateIdentityRelationshipAsOwnerReturns400(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'consumer_id': self.consumer.id,
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.post(self.buildUrl(identity_pk=self.identity.id), data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('A relationship between this identity and consumer already exists.', str(response.data))

    def test_updateIdentityRelationshipAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        
    def test_updateOnlyRelationshipTypeKeepsConsumer(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        self.assertEqual(response.data['consumer_username'], self.consumer.username)

    def test_updateWithConsumerOnlyKeepsRelationshipType(self):
        self.client.force_authenticate(user=self.owner)
        original_type = self.identity_relationship.relationship_type
        data = {
            'consumer_id': self.consumer.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], original_type.name)

    def test_updateIdentityRelationshipAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_updateIdentityRelationshipWithoutAuthentication(self):
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')
        
        self.assertEqual(response.status_code, 403)
        
    def test_updateIdentityRelationshipAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id), data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['relationship_type'], self.relationship_type2.name)
        
    def test_updateIdentityRelationshipWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=9999, relationship_pk=self.identity_relationship.id), data, format='json')
        
        self.assertEqual(response.status_code, 404)
        
    def test_updateIdentityRelationshipWithWrongRelationshipId(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity.id, relationship_pk=9999), data, format='json')
        
        self.assertEqual(response.status_code, 404)

    def test_updateIdentityRelationshipWithMismatchedIdentityAndRelationshipIds(self):
        self.client.force_authenticate(user=self.superuser)
        data = {
            'relationship_type_id': self.relationship_type2.id
        }
        response = self.client.patch(self.buildUrl(identity_pk=self.identity2.id, relationship_pk=self.identity_relationship.id), data, format='json')

        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityRelationshipAsOwner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteIdentityRelationshipAsRegularUser(self):
        self.client.force_authenticate(user=self.consumer)
        response = self.client.delete(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_deleteIdentityRelationshipWithoutAuthentication(self):
        response = self.client.delete(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 403)
        
    def test_deleteIdentityRelationshipAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(identity_pk=self.identity.id, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteIdentityRelationshipWithWrongIdentityId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(identity_pk=9999, relationship_pk=self.identity_relationship.id))
        
        self.assertEqual(response.status_code, 404)
        
    def test_deleteIdentityRelationshipWithWrongRelationshipId(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.buildUrl(identity_pk=self.identity.id, relationship_pk=9999))
        
        self.assertEqual(response.status_code, 404)

    def test_deleteIdentityRelationshipWithMismatchedIdentityAndRelationshipIds(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(identity_pk=self.identity2.id, relationship_pk=self.identity_relationship.id))

        self.assertEqual(response.status_code, 404)
        