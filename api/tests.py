import json
from django.urls import reverse
from rest_framework.test import APITestCase

from .model_factories import *
from identity.models import *
from .serializers import *

class GenderTestCase(APITestCase):
    def setUp(self):
        self.gender1 = GenderFactory.create(name="Male")    
        self.gender2 = GenderFactory.create(name="Female")
        
    def build_url(self):
        return reverse('gender-list')
    
    def tearDown(self):
        Gender.objects.all().delete()
        
    def test_get_genders(self):
        response = self.client.get(self.build_url())
        
        self.assertEqual(response.status_code, 200)
        
class NameContextTestCase(APITestCase):
    def setUp(self):
        self.name_context1 = NameContextFactory.create(name="First Name")    
        self.name_context2 = NameContextFactory.create(name="Last Name")
        
    def build_url(self):
        return reverse('name-context-list')
    
    def tearDown(self):
        NameContext.objects.all().delete()
        
    def test_get_name_contexts(self):
        response = self.client.get(self.build_url())
        
        self.assertEqual(response.status_code, 200)
        
class RelationshipTypeTestCase(APITestCase):
    def setUp(self):
        self.relationship_type1 = RelationshipTypeFactory.create(name="Parent")    
        self.relationship_type2 = RelationshipTypeFactory.create(name="Sibling")
        
    def build_url(self):
        return reverse('relationship-type-list')
    
    def tearDown(self):
        RelationshipType.objects.all().delete()
        
    def test_get_relationship_types(self):
        response = self.client.get(self.build_url())
        
        self.assertEqual(response.status_code, 200)
        
class IdentityNameAccessTestCase(APITestCase):
    def setUp(self):
        self.relationship_type = RelationshipTypeFactory.create(name="Parent")
        self.name_context = NameContextFactory.create(name="First Name")
        self.identity_name_access = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type,
            name_context=self.name_context
        )
        
    def build_url(self):
        return reverse('identity-name-access-list')
    
    def tearDown(self):
        IdentityNameAccess.objects.all().delete()
        RelationshipType.objects.all().delete()
        NameContext.objects.all().delete()
        
    def test_get_identity_name_accesses(self):
        response = self.client.get(self.build_url())
        
        self.assertEqual(response.status_code, 200)
        
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
        
        