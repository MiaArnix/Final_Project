from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Gender, NameContext, RelationshipType, IdentityNameAccess


#@login_required
def metadata_list(request):
    context = {
        'genders': Gender.objects.all(),
        'name_contexts': NameContext.objects.all(),
        'relationship_types': RelationshipType.objects.all(),
        'identity_name_access': IdentityNameAccess.objects.all(),
    }
    return render(request, 'ui/metadata_list.html', context)
