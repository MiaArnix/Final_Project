from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django_cryptography.fields import encrypt

class Gender(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(3)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

class Identity(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE)  
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Identity {self.id} - Owner: {self.owner.username}"
    
    class Meta:
        ordering = ['id']
    
class NameContext(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, validators=[MinLengthValidator(3)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']

class IdentityName(models.Model):
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE, related_name='names')
    name_context = models.ForeignKey(NameContext, on_delete=models.CASCADE)
    name_value = encrypt(models.CharField(max_length=100, null=False, blank=False))
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.is_default:
            existing_default = IdentityName.objects.filter(identity=self.identity, is_default=True)
            if self.pk:
                existing_default = existing_default.exclude(pk=self.pk)
            if existing_default.exists():
                raise ValidationError("Only one default name is allowed per identity.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name_context} - {self.name_value}"
    
    class Meta:
        unique_together = ('identity', 'name_context')
        ordering = ['id']
        
class RelationshipType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True, validators=[MinLengthValidator(3)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']
    
class IdentityRelationship(models.Model):
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE,
                                related_name='relationships')
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='accessible_identities')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.PROTECT, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.consumer} - {self.relationship_type} - {self.identity}"
    
    class Meta:
        unique_together = ('identity', 'consumer')
        ordering = ['id']        
    
class IdentityNameAccess(models.Model):
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    name_context = models.ForeignKey(NameContext, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.relationship_type} - {self.name_context}"
    
    class Meta:
        unique_together = ('relationship_type', 'name_context')
        ordering = ['id']