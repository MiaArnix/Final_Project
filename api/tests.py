import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory

from .model_factories import *
from identity.models import *
from .serializers import *

class SerializerTestCase(APITestCase):
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
        

class GenderTestCase(APITestCase):
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
        
    def test_deleteGenderAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteGenderAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.gender1.id))
        
        self.assertEqual(response.status_code, 403)
        
class NameContextTestCase(APITestCase):
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
        
    def test_deleteNameContextAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteNameContextAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.name_context1.id))
        
        self.assertEqual(response.status_code, 403)
        
        
class RelationshipTypeTestCase(APITestCase):
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
        
    def test_deleteRelationshipTypeAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteRelationshipTypeAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.relationship_type1.id))
        
        self.assertEqual(response.status_code, 403)
        
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
        
    def test_deleteIdentityNameAccessAsSuperuser(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 204)
        
    def test_deleteIdentityNameAccessAsRegularUser(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.buildUrl(id=self.identity_name_access.id))
        
        self.assertEqual(response.status_code, 403)
         
class IdentityTestCase(APITestCase):
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
        
    def build_url(self, id):
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
        
    def test_get_own_identity(self):
        self.client.force_authenticate(user=self.owner1)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.status_code, 200)
        
    def test_get_correct_names(self):
        self.client.force_authenticate(user=self.consumer1)
        response = self.client.get(self.build_url(id=self.identity1.id))
        
        self.assertEqual(response.data['names'][0]['name_context'], self.name_context_personal.name)
        self.assertEqual(response.data['names'][0]['name_value'], self.identity1_name_personal.name_value)
        
        