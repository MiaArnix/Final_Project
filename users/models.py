from django.db import models
from django.conf import settings

class Gender(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Identity(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class NameContext(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return self.name

class IdentityName(models.Model):
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE)
    name_context = models.ForeignKey(NameContext, on_delete=models.CASCADE)
    name_value = models.CharField(max_length=100, null=False, blank=False)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name_context} - {self.name_value}"
    
    class Meta:
        unique_together = ('identity', 'name_context')
        
class RelationshipType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name
    
class Relationship(models.Model):
    identity = models.ForeignKey(Identity, on_delete=models.CASCADE,
                                related_name='relationships')
    consumer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='accessible_identities')
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.consumer} - {self.relationship_type} - {self.identity}"
    
    class Meta:
        unique_together = ('identity', 'consumer')
        
    
class IdentityNameAccess(models.Model):
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    name_context = models.ForeignKey(NameContext, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.relationship_type} - {self.name_context}"
    
    class Meta:
        unique_together = ('relationship_type', 'name_context')