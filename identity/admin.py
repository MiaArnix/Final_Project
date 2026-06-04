from django.contrib import admin
from .models import *

class IdentityNameInline(admin.TabularInline):
    model = IdentityName
    extra = 0

class IdentityAdmin(admin.ModelAdmin):
    list_display = ('owner', 'gender', 'display_names')
    inlines = [IdentityNameInline]

    def display_names(self, obj):
        return ", ".join(
            f"{n.name_context.name}: {n.name_value}{' (default)' if n.is_default else ''}"
            for n in obj.names.all()
        )
    display_names.short_description = "Names"
    
admin.site.register(Identity, IdentityAdmin)