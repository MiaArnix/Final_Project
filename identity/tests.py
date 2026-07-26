from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError 
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError, transaction, connection
from time import sleep

from .models import *

AuthUser = get_user_model()

class GenderModelTestCase(TestCase):
    gender = None
    gender2 = None
    gender3 = None
    
    def setUp(self):
        self.gender = Gender.objects.create(name='Male')
        self.gender2 = Gender.objects.create(name='Female')
        self.gender3 = Gender.objects.create(name='Non-binary')
        
    def tearDown(self):
        Gender.objects.all().delete()
        
    def test_genderStrMethod(self):
        self.assertEqual(str(self.gender), self.gender.name)
        self.assertEqual(str(self.gender2), self.gender2.name)
        self.assertEqual(str(self.gender3), self.gender3.name)
    
    def test_genderOrdering(self):
        genders = Gender.objects.all()
        self.assertEqual(list(genders), [
            self.gender,
            self.gender2,
            self.gender3
        ])

    def test_genderUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Gender.objects.create(name='Male')
        
    def test_genderMaxLength(self):
        gender = Gender(name='A' * 51) 
        with self.assertRaises(ValidationError):
            gender.full_clean()
                   
    def test_genderMinLength(self):
        gender = Gender(name='AB')
        with self.assertRaises(ValidationError):
            gender.full_clean()
        
    def test_genderNotNullConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Gender.objects.create(name=None)
    
    def test_genderNotBlankConstraint(self):
        gender = Gender(name='')
        with self.assertRaises(ValidationError):
            gender.full_clean()
            
class NameContextModelTestCase(TestCase):
    name_context = None
    name_context2 = None
    name_context3 = None
    
    def setUp(self):
        self.name_context = NameContext.objects.create(name='First Name')
        self.name_context2 = NameContext.objects.create(name='Last Name')
        self.name_context3 = NameContext.objects.create(name='Nickname')
        
    def tearDown(self):
        NameContext.objects.all().delete()
        
    def test_nameContextStrMethod(self):
        self.assertEqual(str(self.name_context), self.name_context.name)
        self.assertEqual(str(self.name_context2), self.name_context2.name)
        self.assertEqual(str(self.name_context3), self.name_context3.name)
    
    def test_nameContextOrdering(self):
        name_contexts = NameContext.objects.all()
        self.assertEqual(list(name_contexts), [
            self.name_context,
            self.name_context2,
            self.name_context3
        ])
        
    def test_nameContextUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                NameContext.objects.create(name='First Name')
                
    def test_nameContextMaxLength(self):
        name_context = NameContext(name='A' * 101) 
        with self.assertRaises(ValidationError):
            name_context.full_clean()
                   
    def test_nameContextMinLength(self):
        name_context = NameContext(name='AB')
        with self.assertRaises(ValidationError):
            name_context.full_clean()
        
    def test_nameContextNotNullConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                NameContext.objects.create(name=None)
    
    def test_nameContextNotBlankConstraint(self):
        name_context = NameContext(name='')
        with self.assertRaises(ValidationError):
            name_context.full_clean()

class RelationshipTypeModelTestCase(TestCase):
    relationship_type = None
    relationship_type2 = None
    relationship_type3 = None
    
    def setUp(self):
        self.relationship_type = RelationshipType.objects.create(name='Friend')
        self.relationship_type2 = RelationshipType.objects.create(name='Family')
        self.relationship_type3 = RelationshipType.objects.create(name='Colleague')
        
    def tearDown(self):
        RelationshipType.objects.all().delete()
        
    def test_relationshipTypeStrMethod(self):
        self.assertEqual(str(self.relationship_type), self.relationship_type.name)
        self.assertEqual(str(self.relationship_type2), self.relationship_type2.name)
        self.assertEqual(str(self.relationship_type3), self.relationship_type3.name)
    
    def test_relationshipTypeOrdering(self):
        relationship_types = RelationshipType.objects.all()
        self.assertEqual(list(relationship_types), [
            self.relationship_type,
            self.relationship_type2,
            self.relationship_type3
        ])
        
    def test_relationshipTypeUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RelationshipType.objects.create(name='Friend')
                
    def test_relationshipTypeMaxLength(self):
        relationship_type = RelationshipType(name='A' * 51) 
        with self.assertRaises(ValidationError):
            relationship_type.full_clean()
                   
    def test_relationshipTypeMinLength(self):
        relationship_type = RelationshipType(name='AB')
        with self.assertRaises(ValidationError):
            relationship_type.full_clean()
        
    def test_relationshipTypeNotNullConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                RelationshipType.objects.create(name=None)
    
    def test_relationshipTypeNotBlankConstraint(self):
        relationship_type = RelationshipType(name='')
        with self.assertRaises(ValidationError):
            relationship_type.full_clean()
            
class IdentityNameAccessModelTestCase(TestCase):
    name_context = None
    name_context2 = None
    relationship_type = None
    relationship_type2 = None
    identity_name_access = None
    identity_name_access2 = None
    
    def setUp(self):
        self.name_context = NameContext.objects.create(name='First Name')
        self.name_context2 = NameContext.objects.create(name='Last Name')
        self.relationship_type = RelationshipType.objects.create(name='Friend')
        self.relationship_type2 = RelationshipType.objects.create(name='Family')
        self.identity_name_access = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type,
            name_context=self.name_context
        )
        self.identity_name_access2 = IdentityNameAccess.objects.create(
            relationship_type=self.relationship_type2,
            name_context=self.name_context2
        )
        
    def tearDown(self):
        IdentityNameAccess.objects.all().delete()
        NameContext.objects.all().delete()
        RelationshipType.objects.all().delete()
        
    def test_identityNameAccessStrMethod(self):
        self.assertEqual(str(self.identity_name_access), f"{self.relationship_type} - {self.name_context}")
        self.assertEqual(str(self.identity_name_access2), f"{self.relationship_type2} - {self.name_context2}")
        
    def test_identityNameAccessOrdering(self):
        identity_name_accesses = IdentityNameAccess.objects.all()
        self.assertEqual(list(identity_name_accesses), [
            self.identity_name_access,
            self.identity_name_access2
        ])
    
    def test_identityNameAccessUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityNameAccess.objects.create(
                    relationship_type=self.relationship_type,
                    name_context=self.name_context
                )
                
    def test_identityNameAccessNotNullConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityNameAccess.objects.create(
                    relationship_type=None,
                    name_context=self.name_context
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityNameAccess.objects.create(
                    relationship_type=self.relationship_type,
                    name_context=None
                )
                
    def test_onDeleteCascade(self):
        self.relationship_type.delete()
        self.assertFalse(IdentityNameAccess.objects.filter(pk=self.identity_name_access.pk).exists())
        
        self.name_context2.delete()
        self.assertFalse(IdentityNameAccess.objects.filter(pk=self.identity_name_access2.pk).exists())
        
class IdentityModelTestCase(TestCase):
    owner = None
    owner2 = None
    gender = None
    identity = None
    identity2 = None
    
    def setUp(self):
        self.owner = AuthUser.objects.create_user(
            username='owner',
            password='testpassword123'
        )
        self.owner2 = AuthUser.objects.create_user(
            username='owner2',
            password='testpassword123'
        )
        self.gender = Gender.objects.create(name='Female')
        self.identity = Identity.objects.create(
            owner=self.owner,
            gender=self.gender,
            is_public=False
        )
        self.identity2 = Identity.objects.create(
            owner=self.owner2,
            gender=self.gender,
            is_public=True
        )
        
    def tearDown(self):
        Identity.objects.all().delete()
        Gender.objects.all().delete()
        AuthUser.objects.all().delete()
        
    def test_identityStrMethod(self):
        self.assertEqual(str(self.identity), f"Identity {self.identity.id} - Owner: {self.owner.username}")
        self.assertEqual(str(self.identity2), f"Identity {self.identity2.id} - Owner: {self.owner2.username}")
        
    def test_identityOrdering(self):
        identities = Identity.objects.all()
        self.assertEqual(list(identities), [
            self.identity,
            self.identity2
        ])
        
    def test_identityNotNullConstraints(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Identity.objects.create(
                    owner=None,
                    gender=self.gender,
                    is_public=False
                )
                
    def test_identityCanHaveNullGender(self):
        identity = Identity.objects.create(
            owner=self.owner,
            gender=None,
            is_public=False
        )
        self.assertIsNone(identity.gender)
                
    def test_identityOnDeleteCascade(self):
        self.owner.delete()
        self.assertFalse(Identity.objects.filter(pk=self.identity.pk).exists())
        
        self.owner2.delete()
        self.assertFalse(Identity.objects.filter(pk=self.identity2.pk).exists())
        
    def test_identityGenderOnDeleteSetNull(self):
        self.gender.delete()
        self.assertIsNone(Identity.objects.get(pk=self.identity.pk).gender)
        
    def test_identityIsPublicDefaultValue(self):
        identity = Identity.objects.create(
            owner=self.owner,
            gender=self.gender
        )
        self.assertFalse(identity.is_public)
        
    def test_identityAutoSetFields(self):
        identity = Identity.objects.create(
            owner=self.owner,
            gender=self.gender
        )
        self.assertIsNotNone(identity.created_at)
        self.assertIsNotNone(identity.updated_at)
        
        created_at_create = identity.created_at
        updated_at_create = identity.updated_at
        
        sleep(1)
        identity.is_public = True
        identity.save()
        identity.refresh_from_db()
        
        created_at_update = identity.created_at
        self.assertEqual(created_at_create, created_at_update)
        
        updated_at_update = identity.updated_at
        self.assertNotEqual(updated_at_create, updated_at_update)   
        
class IdentityNameModelTestCase(TestCase):
    owner = None
    gender = None
    name_context = None
    name_context2 = None
    name_context3 = None
    identity_name = None
    identity_name2 = None
    identity = None

    def setUp(self):
        self.owner = AuthUser.objects.create_user(
            username='owner',
            password='testpassword123'
        )
        self.gender = Gender.objects.create(name='Female')
        self.name_context = NameContext.objects.create(name='Last Name')
        self.name_context2 = NameContext.objects.create(name='First Name')
        self.name_context3 = NameContext.objects.create(name='Nickname')
        self.identity = Identity.objects.create(
            owner=self.owner,
            gender=self.gender,
            is_public=False
        )
        self.identity_name = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context,
            name_value='Smith',
            is_default=True
        )
        self.identity_name2 = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context2,
            name_value='Alice',
            is_default=False
        )
        
    def tearDown(self):
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        NameContext.objects.all().delete()
        Gender.objects.all().delete()
        AuthUser.objects.all().delete()
        
    def test_identityNameStrMethod(self):
        self.assertEqual(str(self.identity_name), f"{self.name_context} - {self.identity_name.name_value}")
        self.assertEqual(str(self.identity_name2), f"{self.name_context2} - {self.identity_name2.name_value}")
        
    def test_identityNameOrdering(self):
        identity_names = IdentityName.objects.all()
        self.assertEqual(list(identity_names), [
            self.identity_name,
            self.identity_name2
        ])
        
    def test_identityNameUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityName.objects.create(
                    identity=self.identity,
                    name_context=self.name_context,
                    name_value='Johnson',
                    is_default=False
                )
            
    def test_identityNameOnIdentityDeleteCascade(self):
        self.identity.delete()
        self.assertFalse(IdentityName.objects.filter(pk=self.identity_name.pk).exists())
        self.assertFalse(IdentityName.objects.filter(pk=self.identity_name2.pk).exists())
        
    def test_identityNameOnNameContextDeleteCascade(self):
        self.name_context.delete()
        self.assertFalse(IdentityName.objects.filter(pk=self.identity_name.pk).exists())
        
        self.name_context2.delete()
        self.assertFalse(IdentityName.objects.filter(pk=self.identity_name2.pk).exists())
        
    def test_identityNameMaxLength(self):
        identity_name = IdentityName(
            identity=self.identity,
            name_context=self.name_context2,
            name_value='A' * 101,
            is_default=False
        )
        with self.assertRaises(ValidationError):
            identity_name.full_clean()
            
    def test_identityNameNotNullConstraints(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityName.objects.create(
                    identity=None,
                    name_context=self.name_context3,
                    name_value='Johnson',
                    is_default=False
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityName.objects.create(
                    identity=self.identity,
                    name_context=None,
                    name_value='Johnson',
                    is_default=False
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityName.objects.create(
                    identity=self.identity,
                    name_context=self.name_context3,
                    name_value=None,
                    is_default=False
                )
                
    def test_identityNameNotBlankConstraint(self):
        identity_name = IdentityName(
            identity=self.identity,
            name_context=self.name_context,
            name_value='',
            is_default=False
        )
        with self.assertRaises(ValidationError):
            identity_name.full_clean()
            
    def test_identityNameIsDefaultSetToFalse(self):
        identity_name = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context3,
            name_value='Johnson'
        )
        self.assertFalse(identity_name.is_default)
        
    def test_identityNameIsDefaultConstraint(self):
        with self.assertRaises(ValidationError):
            IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context3,
            name_value='Johnson',
            is_default=True
            )
            
    def test_identityNameCanUpdateExistingDefaultName(self):
        self.identity_name.name_value = 'Smith Updated'
        self.identity_name.name_context = self.name_context3
        self.identity_name.save()
        self.identity_name.refresh_from_db()
        self.assertEqual(self.identity_name.name_value, 'Smith Updated')
        self.assertEqual(self.identity_name.name_context, self.name_context3)
        
    def test_identityNameAutoSetFields(self):
        identity_name = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context3,
            name_value='Johnson'
        )
        self.assertIsNotNone(identity_name.created_at)
        self.assertIsNotNone(identity_name.updated_at)
        
        created_at_create = identity_name.created_at
        updated_at_create = identity_name.updated_at
        
        sleep(1)
        identity_name.name_value = 'Johnson Updated'
        identity_name.save()
        identity_name.refresh_from_db()
        
        created_at_update = identity_name.created_at
        self.assertEqual(created_at_create, created_at_update)
        
        updated_at_update = identity_name.updated_at
        self.assertNotEqual(updated_at_create, updated_at_update)
        
    def test_identityNameIsStoredEncrypted(self):
        name_value_plaintext = 'Alice'

        identity_name = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context3,
            name_value=name_value_plaintext,
            is_default=False
        )

        self.assertEqual(identity_name.name_value, name_value_plaintext)
        identity_name.refresh_from_db()
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT name_value FROM identity_identityname WHERE id = %s",
                [identity_name.id]
            )
            stored_name_value = cursor.fetchone()[0]

        self.assertNotEqual(stored_name_value, name_value_plaintext)
         
class IdentityRelationshipModelTestCase(TestCase):
    owner = None
    consumer = None
    consumer2 = None
    gender = None
    identity = None
    relationship_type = None
    relationship_type2 = None
    name_context = None
    name_context2 = None
    identity_name = None
    identity_name2 = None
    identity_relationship = None
    identity_relationship2 = None
    
    def setUp(self):
        self.owner = AuthUser.objects.create_user(
            username='owner',
            password='ownerpassword'
        )
        self.consumer = AuthUser.objects.create_user(
            username='consumer',
            password='consumerpassword'
        )
        self.consumer2 = AuthUser.objects.create_user(
            username='consumer2',
            password='consumerpassword2'
        )
        self.gender = Gender.objects.create(name='Male')
        self.identity = Identity.objects.create(
            owner=self.owner,
            gender=self.gender,
            is_public=False
        )
        self.relationship_type = RelationshipType.objects.create(name='Family')
        self.relationship_type2 = RelationshipType.objects.create(name='Friend')
        self.name_context = NameContext.objects.create(name='Last Name')
        self.name_context2 = NameContext.objects.create(name='First Name')
        self.identity_name = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context,
            name_value='Smith',
            is_default=True
        )
        self.identity_name2 = IdentityName.objects.create(
            identity=self.identity,
            name_context=self.name_context2,
            name_value='Alice',
            is_default=False
        )
        self.identity_relationship = IdentityRelationship.objects.create(
            identity=self.identity,
            consumer=self.consumer,
            relationship_type=self.relationship_type
        )
        self.identity_relationship2 = IdentityRelationship.objects.create(
            identity=self.identity,
            consumer=self.consumer2,
            relationship_type=self.relationship_type2
        )
        
    def tearDown(self):
        IdentityRelationship.objects.all().delete()
        IdentityName.objects.all().delete()
        Identity.objects.all().delete()
        NameContext.objects.all().delete()
        RelationshipType.objects.all().delete()
        Gender.objects.all().delete()
        AuthUser.objects.all().delete()
        
    def test_identityRelationshipStrMethod(self):
        self.assertEqual(str(self.identity_relationship), f"{self.consumer} - {self.relationship_type} - {self.identity}")
        self.assertEqual(str(self.identity_relationship2), f"{self.consumer2} - {self.relationship_type2} - {self.identity}")
        
    def test_identityRelationshipOrdering(self):
        identity_relationships = IdentityRelationship.objects.all()
        self.assertEqual(list(identity_relationships), [
            self.identity_relationship,
            self.identity_relationship2
        ])
        
    def test_identityRelationshipUniqueConstraint(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityRelationship.objects.create(
                    identity=self.identity,
                    consumer=self.consumer,
                    relationship_type=self.relationship_type2
                )
                
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityRelationship.objects.create(
                    identity=self.identity,
                    consumer=self.consumer2,
                    relationship_type=self.relationship_type
                )
                
    def test_identityRelationshipNotNullConstraints(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityRelationship.objects.create(
                    identity=None,
                    consumer=self.consumer,
                    relationship_type=self.relationship_type
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityRelationship.objects.create(
                    identity=self.identity,
                    consumer=None,
                    relationship_type=self.relationship_type
                )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                IdentityRelationship.objects.create(
                    identity=self.identity,
                    consumer=self.consumer,
                    relationship_type=None
                )
                
    def test_identityRelationshipOnIdentityDeleteCascade(self):
        self.identity.delete()
        self.assertFalse(IdentityRelationship.objects.filter(pk=self.identity_relationship.pk).exists())
        self.assertFalse(IdentityRelationship.objects.filter(pk=self.identity_relationship2.pk).exists())
        
    def test_identityRelationshipOnConsumerDeleteCascade(self):
        self.consumer.delete()
        self.assertFalse(IdentityRelationship.objects.filter(pk=self.identity_relationship.pk).exists())
        
        self.consumer2.delete()
        self.assertFalse(IdentityRelationship.objects.filter(pk=self.identity_relationship2.pk).exists())
        
    def test_identityRelationshipOnRelationshipTypeDeleteProtect(self):
        with self.assertRaises(ProtectedError):
            with transaction.atomic():
                self.relationship_type.delete()
        
        with self.assertRaises(ProtectedError):
            with transaction.atomic():
                self.relationship_type2.delete()
                
    def test_identityRelationshipAutoSetFields(self):
        created_at_create = self.identity_relationship.created_at
        updated_at_create = self.identity_relationship.updated_at
        
        sleep(1)
        self.identity_relationship.relationship_type = self.relationship_type2
        self.identity_relationship.save()
        self.identity_relationship.refresh_from_db()
        
        created_at_update = self.identity_relationship.created_at
        self.assertEqual(created_at_create, created_at_update)
        
        updated_at_update = self.identity_relationship.updated_at
        self.assertNotEqual(updated_at_create, updated_at_update)