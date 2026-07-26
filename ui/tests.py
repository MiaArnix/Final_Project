from django.urls import reverse
from django.test import TestCase
from identity.models import *
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

AuthUser = get_user_model()

class IndexViewTestCase(TestCase):
    def buildUrl(self):
        return reverse('ui:index')
    
    def test_indexViewReturnsSuccessfulResponse(self):
        response = self.client.get(self.buildUrl())
        self.assertEqual(response.status_code, 200)
        
    def test_indexViewUsesCorrectTemplate(self):
        response = self.client.get(self.buildUrl())
        self.assertIn('ui/index.html', [template.name for template in response.templates])

class RegisterViewTestCase(TestCase):
    user = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        
    def tearDown(self):
        self.user.delete()
        
    def buildUrl(self):
        return reverse('ui:register')
    
    def test_registerViewReturnsSuccessfulResponse(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        
    def test_registerViewUsesCorrectTemplate(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('ui/register.html', [template.name for template in response.templates])
        
    def test_registerViewContainsCsrfToken(self):
        response = self.client.get(self.buildUrl())
        
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_registerViewContainsUserCreationForm(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('form', response.context)
        
        form = response.context['form']
        
        self.assertIn('username', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)
        
    def test_registerViewRedirectsWhenUserIsAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('ui:identity-list'))
        
class MetadataListViewTestCase(TestCase):
    def buildUrl(self):
        return reverse('ui:metadata-list')
    
    def test_metadataListViewReturnsSuccessfulResponse(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)
        
    def test_metadataListViewUsesCorrectTemplate(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('ui/metadata_list.html', [template.name for template in response.templates])
        
    def test_metadataListViewContainsGendersInContext(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('genders', response.context)
        self.assertQuerySetEqual(
            response.context['genders'],
            Gender.objects.all(),
            transform=lambda x: x)
        
    def test_metadataListViewContainsNameContextsInContext(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('name_contexts', response.context)
        self.assertQuerySetEqual(
            response.context['name_contexts'],
            NameContext.objects.all(),
            transform=lambda x: x)
        
    def test_metadataListViewContainsRelationshipTypesInContext(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('relationship_types', response.context)
        self.assertQuerySetEqual(
            response.context['relationship_types'],
            RelationshipType.objects.all(),
            transform=lambda x: x)
        
    def test_metadataListViewContainsIdentityNameAccessRulesInContext(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('identity_name_access', response.context)
        self.assertQuerySetEqual(
        response.context['identity_name_access'],
        IdentityNameAccess.objects.all(),
        transform=lambda x: x)
        
class IdentityListViewTestCase(TestCase):
    user = None
    user2 = None
    user3 = None
    gender = None
    identity1 = None
    identity2 = None
    identity3 = None
    identity4 = None
    name_context1 = None
    name_context2 = None
    relationship_type1 = None
    identity_name_access1 = None
    identity_name1 = None
    identity_name2 = None
    identity_name3 = None
    identity_name4 = None
    identity_name5 = None
    identity_name6 = None
    identity_relationship1 = None
    identity_relationship2 = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.user2 = AuthUser.objects.create_user(username='testuser2', password='testpassword2')
        self.user3 = AuthUser.objects.create_user(username='testuser3', password='testpassword3')
        
        self.gender = Gender.objects.create(name='Male')
        self.name_context1 = NameContext.objects.create(name='Legal')
        self.name_context2 = NameContext.objects.create(name='Nickname')
        self.relationship_type1 = RelationshipType.objects.create(name='Friend')
        self.identity_name_access1 = IdentityNameAccess.objects.create(relationship_type=self.relationship_type1, name_context=self.name_context1)
        
        self.identity1 = Identity.objects.create(owner=self.user, gender=self.gender, is_public=False)
        self.identity2 = Identity.objects.create(owner=self.user, gender=self.gender, is_public=False)
        self.identity3 = Identity.objects.create(owner=self.user2, gender=self.gender, is_public=False)
        self.identity4 = Identity.objects.create(owner=self.user3, gender=self.gender, is_public=True)
        
        self.identity_name1 = IdentityName.objects.create(identity=self.identity1, name_context=self.name_context1, name_value='John', is_default=True)
        self.identity_name2 = IdentityName.objects.create(identity=self.identity2, name_context=self.name_context1, name_value='Doe', is_default=True)
        self.identity_name3 = IdentityName.objects.create(identity=self.identity3, name_context=self.name_context1, name_value='Alice', is_default=True)
        self.identity_name4 = IdentityName.objects.create(identity=self.identity4, name_context=self.name_context1, name_value='Bob', is_default=True)
        self.identity_name5 = IdentityName.objects.create(identity=self.identity1, name_context=self.name_context2, name_value='Robert', is_default=False)  
        self.identity_name6 = IdentityName.objects.create(identity=self.identity4, name_context=self.name_context2, name_value='Bobby', is_default=False)
        
        self.identity_relationship1 = IdentityRelationship.objects.create(consumer=self.user2, identity=self.identity1, relationship_type=self.relationship_type1)
        self.identity_relationship2 = IdentityRelationship.objects.create(consumer=self.user, identity=self.identity3, relationship_type=self.relationship_type1)
        
    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.user3.delete()
        self.gender.delete()
        self.name_context1.delete()
        self.name_context2.delete()
        self.relationship_type1.delete()
        self.identity_name_access1.delete()
        self.identity1.delete()
        self.identity2.delete()
        self.identity3.delete()
        self.identity4.delete()
        self.identity_name1.delete()
        self.identity_name2.delete()
        self.identity_name3.delete()
        self.identity_name4.delete()
        self.identity_name5.delete()
        self.identity_name6.delete()
        self.identity_relationship1.delete()
        self.identity_relationship2.delete()
        
    def buildUrl(self, scope=None):
        url = reverse('ui:identity-list')
        
        if scope is not None:
            return f"{url}?scope={scope}"
        else:
            return url
    
    def test_identityListViewReturnsSuccessfulResponse(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 200)

    def test_identityListViewUsesCorrectTemplate(self):
        response = self.client.get(self.buildUrl())
        
        self.assertIn('ui/identity_list.html', [template.name for template in response.templates])
    
    def test_identityListViewShowsOwnIdentitiesWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.buildUrl(scope='owned'))
        
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertIn(self.identity1.id, identity_ids)
        self.assertIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertNotIn(self.identity4.id, identity_ids)
        
    def test_identityListViewShowsSharedAndPublicIdentitiesWhenAuthenticated(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertIn(self.identity1.id, identity_ids)
        self.assertNotIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertIn(self.identity4.id, identity_ids)
    
    def test_identityListViewShowsPublicIdentitiesWhenAuthenticatedAndNoScope(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope=None))
                
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertNotIn(self.identity1.id, identity_ids)
        self.assertNotIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertIn(self.identity4.id, identity_ids)
    
    def test_identityListViewShowsPublicIdentitiesWhenNotAuthenticatedIrrelevantOfScope(self):
        response = self.client.get(self.buildUrl(scope=None))
        
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertNotIn(self.identity1.id, identity_ids)
        self.assertNotIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertIn(self.identity4.id, identity_ids)
        
        response = self.client.get(self.buildUrl(scope='owned'))
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertNotIn(self.identity1.id, identity_ids)
        self.assertNotIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertIn(self.identity4.id, identity_ids)
        
        response = self.client.get(self.buildUrl(scope='shared'))
        self.assertIn('identities', response.context)
        identities = response.context['identities']
        identity_ids = [identity['id'] for identity in identities]
        
        self.assertNotIn(self.identity1.id, identity_ids)
        self.assertNotIn(self.identity2.id, identity_ids)
        self.assertNotIn(self.identity3.id, identity_ids)
        self.assertIn(self.identity4.id, identity_ids)
        
    def test_identityListReturnsAllNamesForOwnedIdentities(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.buildUrl(scope='owned'))
        
        self.assertIn('identities', response.context)
        
        identities = response.context['identities']
        owned_identity = identities[0]
        
        self.assertIn('names', owned_identity)
        
        names = owned_identity['names']
        name_values = [name.name_value for name in names]
        
        self.assertIn(self.identity_name1.name_value, name_values)
        self.assertIn(self.identity_name5.name_value, name_values)
        
    def test_identityListReturnsAllNamesForPublicIdentities(self):
        response = self.client.get(self.buildUrl(scope=None))
        
        self.assertIn('identities', response.context)
        
        identities = response.context['identities']
        public_identity = identities[0]
        
        self.assertIn('names', public_identity)
        
        names = public_identity['names']
        name_values = [name.name_value for name in names]
        
        self.assertIn(self.identity_name4.name_value, name_values)
        self.assertIn(self.identity_name6.name_value, name_values)
        
    def test_identityListReturnsAccessibleNamesForSharedIdentities(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('identities', response.context)
        
        identities = response.context['identities']
        shared_identity = identities[0]
        
        self.assertIn('names', shared_identity)
        
        names = shared_identity['names']
        name_values = [name.name_value for name in names]
        
        self.assertIn(self.identity_name1.name_value, name_values)
        self.assertNotIn(self.identity_name5.name_value, name_values)
        
    def test_identityListViewContainsScopeInContext(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='owned'))
        
        self.assertIn('scope', response.context)
        self.assertEqual(response.context['scope'], 'owned')
        
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('scope', response.context)
        self.assertEqual(response.context['scope'], 'shared')
        
        response = self.client.get(self.buildUrl(scope=None))
        
        self.assertIn('scope', response.context)
        self.assertIsNone(response.context['scope'])
        
    def test_identityListViewConveysScopeToTemplateContextWhenNotAuthenticated(self):
        response = self.client.get(self.buildUrl(scope=None))
        
        self.assertIn('scope', response.context)
        self.assertEqual(response.context['scope'], 'public')
        
        response = self.client.get(self.buildUrl(scope='owned'))
        
        self.assertIn('scope', response.context)
        self.assertEqual(response.context['scope'], 'public')
        
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('scope', response.context)
        self.assertEqual(response.context['scope'], 'public')
        
    def test_identityListViewContainsConsumersInContextWhenAuthenticatedAndOwnedScope(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='owned'))
        
        self.assertIn('consumers', response.context)
        consumers = response.context['consumers']
        consumer_usernames = [consumer.username for consumer in consumers]
        
        self.assertIn(self.user.username, consumer_usernames)
        self.assertNotIn(self.user2.username, consumer_usernames)
        self.assertIn(self.user3.username, consumer_usernames)
        
    def test_identityListViewContainsRelationshipTypesInContextWhenAuthenticated(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('relationship_types', response.context)
        relationship_types = response.context['relationship_types']
        relationship_type_names = [relationship_type.name for relationship_type in relationship_types]
        
        self.assertIn(self.relationship_type1.name, relationship_type_names)
        
    def test_identityListViewContainsNameContextsInContextWhenAuthenticated(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.get(self.buildUrl(scope='shared'))
        
        self.assertIn('name_contexts', response.context)
        name_contexts = response.context['name_contexts']
        name_context_names = [name_context.name for name_context in name_contexts]
        
        self.assertIn(self.name_context1.name, name_context_names)
        self.assertIn(self.name_context2.name, name_context_names)
    
    def test_identityListViewDoesNotContainConsumersInContextWhenNotAuthenticated(self):
        response = self.client.get(self.buildUrl(scope=None))
        
        self.assertIn('consumers', response.context)
        consumers = response.context['consumers']
        
        self.assertIsNone(consumers)
        
class CreateIdentityViewTestCase(TestCase):
    user = None
    gender = None
    gender2 = None
    name_context1 = None
    name_context2 = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.gender = Gender.objects.create(name='Male')
        self.name_context1 = NameContext.objects.create(name='Legal')
        
    def tearDown(self):
        self.user.delete()
        self.name_context1.delete()
        self.name_context2.delete()
        self.gender.delete()
        self.gender2.delete()
        
    def buildUrl(self):
        return reverse('ui:create-identity')
    
    def test_createIdentityViewRedirectsWhenNotAuthenticated(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl()}")

    def test_createIdentityViewRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': self.gender.id,
            'is_public': True,
            'default_name_context': self.name_context1.id,
            'default_name_value': 'John'
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertTrue(Identity.objects.filter(owner=self.user, gender=self.gender, is_public=True).exists())
        self.assertIn('John', [name.name_value for name in IdentityName.objects.filter(identity__owner=self.user)])
        
    def test_createIdentityViewAllowsCreationWithNullGender(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': '',
            'is_public': True,
            'default_name_context': self.name_context1.id,
            'default_name_value': 'John'
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn(None, [identity.gender for identity in Identity.objects.filter(owner=self.user)])
        
    def test_createIdentityViewDoesNotAllowCreationWithInvalidGender(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': 9999,
            'is_public': True,
            'default_name_context': self.name_context1.id,
            'default_name_value': 'John'
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'gender', 'Select a valid choice. That choice is not one of the available choices.')
        
    def test_createIdentityViewDoesNotAllowCreationWithInvalidNameContext(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': self.gender.id,
            'is_public': True,
            'default_name_context': 9999,
            'default_name_value': 'John'
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'default_name_context', 'Select a valid choice. That choice is not one of the available choices.')
        
    def test_createIdentityViewDoesNotAllowCreationWithEmptyNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': self.gender.id,
            'is_public': True,
            'default_name_context': self.name_context1.id,
            'default_name_value': ''
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'default_name_value', 'This field is required.')
        
    def test_createIdentityViewDoesNotAllowCreationWithWhitespaceNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': self.gender.id,
            'is_public': True,  
            'default_name_context': self.name_context1.id,
            'default_name_value': '   '
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'default_name_value', 'This field is required.')
        
class DeleteIdentityViewTestCase(TestCase):
    user = None
    identity = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        
    def tearDown(self):
        self.user.delete()
        self.identity.delete()
        
    def buildUrl(self):
        return reverse('ui:delete-identity', args=[self.identity.id])
    
    def test_deleteIdentityViewRedirectsWhenNotAuthenticated(self):
        response = self.client.get(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl()}")
        
    def test_deleteIdentityViewRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertFalse(Identity.objects.filter(id=self.identity.id).exists())
        
    def test_deleteIdentityViewDoesNotAllowDeletionByNonOwner(self):
        other_user = AuthUser.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        response = self.client.post(self.buildUrl())
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to delete this identity.', [str(message) for message in messages])
        self.assertTrue(Identity.objects.filter(id=self.identity.id).exists())
        
class EditIdentityViewTestCase(TestCase):
    user = None
    identity = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        
    def tearDown(self):
        self.user.delete()
        self.identity.delete()
        
    def test_editIdentityViewRedirectsWhenNotAuthenticated(self):
        response = self.client.get(reverse('ui:edit-identity', args=[self.identity.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={reverse('ui:edit-identity', args=[self.identity.id])}")
        
    def test_editIdentityViewReturnsSuccessfulResponseWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ui:edit-identity', args=[self.identity.id]))
        
        self.assertEqual(response.status_code, 200)
        
    def test_editIdentityViewUsesCorrectTemplateWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ui:edit-identity', args=[self.identity.id]))
        
        self.assertIn('ui/edit_identity.html', [template.name for template in response.templates])
        
    def test_editIdentityContainsIdentityFormWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ui:edit-identity', args=[self.identity.id]))
        
        self.assertIn('form', response.context)
        form = response.context['form']
        
        self.assertIn('gender', form.fields)
        self.assertIn('is_public', form.fields)
        
    def test_editIdentityViewRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': '',
            'is_public': False
        }
        response = self.client.post(reverse('ui:edit-identity', args=[self.identity.id]), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        
    def test_editIdentityViewDoesNotAllowEditingByNonOwner(self):
        other_user = AuthUser.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        post_data = {
            'gender': '',
            'is_public': False
        }
        response = self.client.post(reverse('ui:edit-identity', args=[self.identity.id]), data=post_data)   
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        
    def test_editIdentityViewDoesNotAllowEditingWithInvalidGender(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'gender': 9999,
            'is_public': False
        }
        response = self.client.post(reverse('ui:edit-identity', args=[self.identity.id]), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'gender', 'Select a valid choice. That choice is not one of the available choices.')
        
class AddRelationshipViewTestCase(TestCase):
    user = None
    consumer = None
    identity = None
    relationship_type = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.relationship_type = RelationshipType.objects.create(name='Friend')
        self.consumer = AuthUser.objects.create_user(username='consumeruser', password='consumerpassword')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        
    def tearDown(self):
        self.user.delete()
        self.relationship_type.delete()
        self.consumer.delete()
        self.identity.delete()
        
    def buildUrl(self):
        return reverse('ui:add-relationship')
    
    def test_addRelationshipViewRedirectsWhenNotAuthenticated(self):
        response = self.client.post(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl()}")

    def test_addRelationshipRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'consumer': self.consumer.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertTrue(IdentityRelationship.objects.filter(consumer=self.consumer, identity=self.identity, relationship_type=self.relationship_type).exists())
        
    def test_addRelationshipViewDoesNotAllowAddingRelationshipByNonOwner(self):
        other_user = AuthUser.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')
        post_data = {
            'identity_id': self.identity.id,
            'consumer': self.consumer.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        self.assertFalse(IdentityRelationship.objects.filter(consumer=self.consumer, identity=self.identity, relationship_type=self.relationship_type).exists())
        
    def test_addRelationshipViewDoesNotAllowAddingRelationshipWithInvalidConsumer(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'consumer': 9999,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
                
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Invalid consumer selected.', [str(message) for message in messages])
        
    def test_addRelationshipViewDoesNotAllowAddingRelationshipWithInvalidRelationshipType(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'consumer': self.consumer.id,
            'relationship_type_id': 9999
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
                
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Invalid relationship type selected.', [str(message) for message in messages])
        
    def test_addRelationshipViewDoesNotAllowAddingDuplicateRelationship(self):
        self.client.login(username='testuser', password='testpassword')
        IdentityRelationship.objects.create(consumer=self.consumer, identity=self.identity, relationship_type=self.relationship_type)
        
        post_data = {
            'identity_id': self.identity.id,
            'consumer': self.consumer.id,
            'relationship_type_id': self.relationship_type.id
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Access already exists!', [str(message) for message in messages])

class DeleteRelationshipViewTestCase(TestCase):
    user = None
    consumer = None
    identity = None
    relationship_type = None
    identity_relationship = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.relationship_type = RelationshipType.objects.create(name='Friend')
        self.consumer = AuthUser.objects.create_user(username='consumeruser', password='consumerpassword')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        self.identity_relationship = IdentityRelationship.objects.create(consumer=self.consumer, identity=self.identity, relationship_type=self.relationship_type)
        
    def tearDown(self):
        self.user.delete()
        self.relationship_type.delete()
        self.consumer.delete()
        self.identity.delete()
        self.identity_relationship.delete()
        
    def buildUrl(self):
        return reverse('ui:delete-relationship', args=[self.identity_relationship.id])
    
    def test_deleteRelationshipViewRedirectsWhenNotAuthenticated(self):
        response = self.client.post(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl()}")

    def test_deleteRelationshipRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertFalse(IdentityRelationship.objects.filter(id=self.identity_relationship.id).exists())
        
    def test_deleteRelationshipViewDoesNotAllowDeletionByNonOwner(self):
        self.client.login(username='consumeruser', password='consumerpassword')
        response = self.client.post(self.buildUrl())
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        self.assertTrue(IdentityRelationship.objects.filter(id=self.identity_relationship.id).exists())
        
    def test_deleteRelationshipViewDoesNotAllowDeletionOfNonExistentRelationship(self):
        self.client.login(username='testuser', password='testpassword')
        non_existent_relationship_id = 9999
        url = reverse('ui:delete-relationship', args=[non_existent_relationship_id])
        response = self.client.post(url)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Relationship does not exist.', [str(message) for message in messages])
        
class AddNameViewTestCase(TestCase):
    user = None
    user2 = None
    identity = None
    name_context = None
    name_context2 = None
    identity_name = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.user2 = AuthUser.objects.create_user(username='testuser2', password='testpassword2')
        self.name_context = NameContext.objects.create(name='Legal')
        self.name_context2 = NameContext.objects.create(name='Nickname')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        self.identity_name = IdentityName.objects.create(identity=self.identity, name_context=self.name_context, name_value='John Doe', is_default=True)
        
    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.name_context.delete()
        self.name_context2.delete()
        self.identity.delete()
        self.identity_name.delete()
        
    def buildUrl(self):
        return reverse('ui:add-name')
    
    def test_addNameViewRedirectsWhenNotAuthenticated(self):
        response = self.client.post(self.buildUrl())
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl()}")
        
    def test_addNameRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context2.id,
            'name_value': 'John Doe',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertTrue(IdentityName.objects.filter(identity=self.identity, name_context=self.name_context2).exists())
        
    def test_addNameViewDoesNotAllowAddingNameByNonOwner(self):
        self.client.login(username='testuser2', password='testpassword2')
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context2.id,
            'name_value': 'John Doe',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        self.assertFalse(IdentityName.objects.filter(identity=self.identity, name_context=self.name_context2).exists())
        
    def test_addNameViewDoesNotAllowAddingNameWithInvalidNameContext(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': 9999,
            'name_value': 'John Doe',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Invalid name context selected.', [str(message) for message in messages])
        
    def test_addNameViewDoesNotAllowAddingNameWithEmptyNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context2.id,
            'name_value': '',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Name value cannot be empty.', [str(message) for message in messages])
        
    def test_addNameViewDoesNotAllowAddingNameWithWhitespaceNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context2.id,
            'name_value': '   ',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Name value cannot be empty.', [str(message) for message in messages])
        
    def test_addNameViewDoesNotAllowAddingDuplicateName(self):
        self.client.login(username='testuser', password='testpassword')
        
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context.id,
            'name_value': 'John Doe',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('A name with this context already exists for this identity.', [str(message) for message in messages])
        
    def test_addDefaultNameViewSetsOtherNamesToNonDefault(self):
        self.client.login(username='testuser', password='testpassword')
        
        post_data = {
            'identity_id': self.identity.id,
            'name_context_id': self.name_context2.id,
            'name_value': 'Johnny',
            'is_default': 'on'
        }
        response = self.client.post(self.buildUrl(), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        
        new_name = IdentityName.objects.get(identity=self.identity, name_context=self.name_context2)
        self.assertTrue(new_name.is_default)
        
        old_name = IdentityName.objects.get(identity=self.identity, name_context=self.name_context)
        self.assertFalse(old_name.is_default)
        
class DeleteNameViewTestCase(TestCase):
    user = None
    user2 = None
    identity = None
    name_context = None
    name_context2 = None
    identity_name = None
    identity_name2 = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.user2 = AuthUser.objects.create_user(username='testuser2', password='testpassword2')
        self.name_context = NameContext.objects.create(name='Legal')
        self.name_context2 = NameContext.objects.create(name='Nickname')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        self.identity_name = IdentityName.objects.create(identity=self.identity, name_context=self.name_context, name_value='John Doe', is_default=True)
        self.identity_name2 = IdentityName.objects.create(identity=self.identity, name_context=self.name_context2, name_value='Johnny', is_default=False)
        
    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.name_context.delete()
        self.name_context2.delete()
        self.identity.delete()
        self.identity_name.delete()
        self.identity_name2.delete()
        
    def buildUrl(self, name_id):
        return reverse('ui:delete-name', args=[name_id])
    
    def test_deleteNameViewRedirectsWhenNotAuthenticated(self):
        response = self.client.post(self.buildUrl(self.identity_name.id))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl(self.identity_name.id)}")
        
    def test_deleteNameRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.buildUrl(self.identity_name2.id))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertFalse(IdentityName.objects.filter(id=self.identity_name2.id).exists())
        
    def test_deleteNameViewDoesNotAllowDeletionByNonOwner(self):
        self.client.login(username='testuser2', password='testpassword2')
        response = self.client.post(self.buildUrl(self.identity_name2.id))
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        self.assertTrue(IdentityName.objects.filter(id=self.identity_name2.id).exists())
        
    def test_deleteNameViewDoesNotAllowDeletionOfNonExistentName(self):
        self.client.login(username='testuser', password='testpassword')
    
        response = self.client.post(self.buildUrl(9999))
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Name does not exist.', [str(message) for message in messages])
        
    def test_deleteNameViewDoesNotAllowDeletionOfDefaultName(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.buildUrl(self.identity_name.id))
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Cannot delete the default name. Please set another name as default before deleting this one.', [str(message) for message in messages])
        self.assertTrue(IdentityName.objects.filter(id=self.identity_name.id).exists())
        
        
    def test_deleteNameViewAllowsDeletionOfNonDefaultName(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.buildUrl(self.identity_name2.id))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertFalse(IdentityName.objects.filter(id=self.identity_name2.id).exists())
        
class EditNameViewTestCase(TestCase):
    user = None
    user2 = None
    identity = None
    name_context = None
    name_context2 = None
    name_context3 = None
    identity_name = None
    identity_name2 = None
    
    def setUp(self):
        self.user = AuthUser.objects.create_user(username='testuser', password='testpassword')
        self.user2 = AuthUser.objects.create_user(username='testuser2', password='testpassword2')
        self.name_context = NameContext.objects.create(name='Legal')
        self.name_context2 = NameContext.objects.create(name='Nickname')
        self.identity = Identity.objects.create(owner=self.user, is_public=True)
        self.identity_name = IdentityName.objects.create(identity=self.identity, name_context=self.name_context, name_value='John Doe', is_default=True)
        self.identity_name2 = IdentityName.objects.create(identity=self.identity, name_context=self.name_context2, name_value='Johnny', is_default=False)
        self.name_context3 = NameContext.objects.create(name='Alias')
        
    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.name_context.delete()
        self.name_context2.delete()
        self.identity.delete()
        self.identity_name.delete()
        self.identity_name2.delete()
        
    def buildUrl(self, name_id):
        return reverse('ui:edit-name', args=[name_id])
    
    def test_editNameViewRedirectsWhenNotAuthenticated(self):
        response = self.client.post(self.buildUrl(self.identity_name.id))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.buildUrl(self.identity_name.id)}")
        
    def test_editNameUsesCorrectTemplateWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.buildUrl(self.identity_name.id))
        
        self.assertIn('ui/edit_name.html', [template.name for template in response.templates])
        
    def test_editNameContainsIdentityNameFormWhenAuthenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.buildUrl(self.identity_name.id))
        
        self.assertIn('form', response.context)
        form = response.context['form']
        
        self.assertIn('name_context', form.fields)
        self.assertIn('name_value', form.fields)
        self.assertIn('is_default', form.fields)
        
    def test_editNameViewRedirectsToOwnedIdentityListAfterSuccessfulPost(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context3.id,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        
        updated_name = IdentityName.objects.get(id=self.identity_name.id)
        self.assertEqual(updated_name.name_context.id, self.name_context3.id)
        self.assertEqual(updated_name.name_value, 'Johnny')
        
    def test_editNameViewDoesNotAllowEditingByNonOwner(self):
        self.client.login(username='testuser2', password='testpassword2')
        post_data = {
            'name_context': self.name_context3.id,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('You do not have permission to edit this identity.', [str(message) for message in messages])
        
    def test_editNameViewValidatesNameId(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context3.id,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(9999), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Name does not exist.', [str(message) for message in messages])
        
    def test_editNameViewDoesNotAllowEditingToDuplicateNameContext(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context2.id,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('A name with this context already exists for this identity.', [str(message) for message in messages])
        
    def test_editNameViewDoesNotAllowEditingWithEmptyNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context3.id,
            'name_value': '',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name_value', 'This field is required.')
        
    def test_editNameViewDoesNotAllowEditingWithWhitespaceNameValue(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context3.id,
            'name_value': '   ',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name_value', 'This field is required.')
        
    def test_editNameViewDoesNotAllowEditingDefaultNameToNonDefault(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context.id,
            'name_value': 'John Doe',
            'is_default': False
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        self.assertIn('Cannot unset default name without setting another name as default.', [str(message) for message in messages])
        
    def test_editNameViewAllowsEditingNonDefaultNameToDefault(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': self.name_context2.id,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name2.id), data=post_data)
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('ui:identity-list')}?scope=owned")
        
        updated_name = IdentityName.objects.get(id=self.identity_name2.id)
        self.assertTrue(updated_name.is_default)
        
        old_name = IdentityName.objects.get(id=self.identity_name.id)
        self.assertFalse(old_name.is_default)
        
    def test_editNameAllowsOnlyValidNameContexts(self):
        self.client.login(username='testuser', password='testpassword')
        post_data = {
            'name_context': 9999,
            'name_value': 'Johnny',
            'is_default': True
        }
        response = self.client.post(self.buildUrl(self.identity_name.id), data=post_data)
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name_context', 'Select a valid choice. That choice is not one of the available choices.')
        
        