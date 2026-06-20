from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity, IdentityRelationship

AuthUser = get_user_model()

def register(request):
    if request.user.is_authenticated:
        return redirect('ui:identity-list')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    return render(request, 'ui/register.html', {'form': form})


@login_required
def metadata_list(request):
    context = {
        'genders': Gender.objects.all(),
        'name_contexts': NameContext.objects.all(),
        'relationship_types': RelationshipType.objects.all(),
        'identity_name_access': IdentityNameAccess.objects.all(),
    }
    return render(request, 'ui/metadata_list.html', context)

@login_required
def identity_list(request):
    context = {
        'identities': Identity.objects.filter(owner=request.user),
        'relationship_types': RelationshipType.objects.all(),
        'consumers': AuthUser.objects.exclude(id=request.user.id),
    }
    
    for identity in context['identities']:
        print(f'Identity {identity.id} has {identity.names.count()} names')
    return render(request, 'ui/identity_list.html', context)

@login_required
def add_relationship(request):
    if request.method == 'POST':
        identity_id = request.POST.get('identity_id')
        relationship_type_id = request.POST.get('relationship_type_id')
        consumer_id = request.POST.get('consumer')

        identity = Identity.objects.get(id=identity_id)
        relationship_type = RelationshipType.objects.get(id=relationship_type_id)
        consumer= AuthUser.objects.get(id=consumer_id)

        IdentityRelationship.objects.create(
            identity = identity,
            relationship_type = relationship_type,
            consumer = consumer
            )

        messages.success(request, 'Access added successfully!')
        return redirect('ui:identity-list')