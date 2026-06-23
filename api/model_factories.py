import factory
from django.contrib.auth import get_user_model
from identity.models import *

AuthUser = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AuthUser
        
class GenderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Gender
        
class NameContextFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NameContext
        
class IdentityNameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IdentityName
        
class RelationshipTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RelationshipType
        
class IdentityNameAccessFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IdentityNameAccess
        
class IdentityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Identity