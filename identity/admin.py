from django.contrib import admin
from .models import *

class IdentityNameInline(admin.TabularInline):
    model = IdentityName
    extra = 0

class IdentityAdmin(admin.ModelAdmin):
    list_display = ('id','owner', 'gender', 'display_names', 'is_public')
    inlines = [IdentityNameInline]

    def display_names(self, obj):
        return ", ".join(
            f"{n.name_context.name}: {n.name_value}{' (default)' if n.is_default else ''}"
            for n in obj.names.all()
        )
    display_names.short_description = "Names"
    
    def owner(self, obj):
        return obj.owner.username
    
admin.site.register(Identity, IdentityAdmin)

class NameContextAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(NameContext, NameContextAdmin)

class GenderAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Gender, GenderAdmin)

class RelationshipTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(RelationshipType, RelationshipTypeAdmin)

class IdentityNameAccessAdmin(admin.ModelAdmin):
    list_display = ('relationship_type', 'name_context')

admin.site.register(IdentityNameAccess, IdentityNameAccessAdmin)

class IdentityRelationshipAdmin(admin.ModelAdmin):
    list_display = ('consumer', 'relationship_type', 'identity', 'owner')
    
    def consumer(self, obj):
        return obj.consumer.username
    
    def owner(self, obj):
        return obj.identity.owner.username

admin.site.register(IdentityRelationship, IdentityRelationshipAdmin)

class IdentityNameAdmin(admin.ModelAdmin):
    list_display = ('identity', 'owner', 'name_context', 'name_value', 'is_default')
    
    def owner(self, obj):
        return obj.identity.owner.username

admin.site.register(IdentityName, IdentityNameAdmin)