from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from identity.models import *
from .forms import IdentityCreateForm

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

def index(request):
    return render(request, 'ui/index.html')

@login_required
def metadata_list(request):
    context = {
        'genders': Gender.objects.all(),
        'name_contexts': NameContext.objects.all(),
        'relationship_types': RelationshipType.objects.all(),
        'identity_name_access': IdentityNameAccess.objects.all(),
    }
    return render(request, 'ui/metadata_list.html', context)

def identity_list(request):
    scope = request.GET.get('scope', None)
    
    if scope == 'owned' and request.user.is_authenticated:
        identities = Identity.objects.filter(owner=request.user)
        consumers = AuthUser.objects.exclude(id=request.user.id)
    elif scope == 'shared' and request.user.is_authenticated:
        identities = Identity.objects.filter(relationships__consumer=request.user).distinct()
        
        for identity in identities:
            identity.names = filter_names_by_access(identity, request.user)
            
        public_identities = Identity.objects.filter(is_public=True).exclude(id__in=identities)
        identities = identities | public_identities
        
        consumers = None
    else: 
        identities = Identity.objects.filter(is_public=True)
        consumers = None
    
    context = {
        'identities': identities,
        'relationship_types': RelationshipType.objects.all(),
        'consumers': consumers,
    }
    return render(request, 'ui/identity_list.html', context)

def filter_names_by_access(identity, consumer):
    accessible_names = []
    
    # find relationship between consumers and identity
    relationship_type = IdentityRelationship.objects.filter(identity=identity, consumer=consumer).first().relationship_type
    
    # identify allowed name contexts based on identity name access rules for the relationship type
    allowed_contexts = IdentityNameAccess.objects.filter(relationship_type=relationship_type).values_list('name_context', flat=True)
    
    # find matching names
    for name in identity.names.all():
        if name.name_context.id in allowed_contexts:
            accessible_names.append(name)
            
    # if no names match the allowed contexts, return the default name
    if accessible_names == []:
        accessible_names = identity.names.filter(is_default=True)
        
    return accessible_names
    

@login_required
def add_relationship(request):
    if request.method == 'POST':
        identity_id = request.POST.get('identity_id')
        relationship_type_id = request.POST.get('relationship_type_id')
        consumer_id = request.POST.get('consumer')

        identity = Identity.objects.get(id=identity_id)
        relationship_type = RelationshipType.objects.get(id=relationship_type_id)
        consumer= AuthUser.objects.get(id=consumer_id)

        if not IdentityRelationship.objects.filter(identity=identity, consumer=consumer).exists():
            IdentityRelationship.objects.create(
                identity = identity,
                relationship_type = relationship_type,
                consumer = consumer
                )
        else:
            messages.error(request, 'Access already exists!')
            return redirect('ui:identity-list')

        messages.success(request, 'Access added successfully!')
        return redirect('ui:identity-list')
    
@login_required
def delete_relationship(request, relationship_id):
    relationship = IdentityRelationship.objects.get(id=relationship_id)
    
    if relationship.identity.owner == request.user:
        relationship.delete()
        messages.success(request, 'Access deleted successfully!')
        
    return redirect('ui:identity-list')

@login_required
def create_identity(request):
    
    if request.method == 'POST':
        form = IdentityCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                identity = Identity.objects.create(
                    owner=request.user,
                    gender=form.cleaned_data['gender'],
                    is_public=form.cleaned_data['is_public']
                )
                
                IdentityName.objects.create(
                    identity=identity,
                    name_context=form.cleaned_data['default_name_context'],
                    name_value=form.cleaned_data['default_name_value'],
                    is_default=form.cleaned_data['is_default'])
                
                messages.success(request, 'Identity created successfully!')
                return redirect('ui:identity-list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = IdentityCreateForm()
    
    return render(request, 'ui/create_identity.html', {'form': form})