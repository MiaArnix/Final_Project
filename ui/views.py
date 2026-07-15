from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from identity.models import *
from .forms import *

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

# identity related views
def identity_list(request):
    scope = request.GET.get('scope', None)
    user = request.user
    consumers = None
    public_identities = Identity.objects.filter(is_public=True)
    identity_list = []
    
    if user.is_authenticated:    
        if scope == 'owned':
            identity_list = Identity.objects.filter(owner=user)
            consumers = AuthUser.objects.exclude(id=user.id)
        elif scope == 'shared':
            shared_identities = Identity.objects.filter(relationships__consumer=user)
            identity_list = (public_identities | shared_identities).distinct()
    else:
        identity_list = public_identities
        
    final_identities = []
    for base_identity in identity_list:
        visible_names = filter_names_by_access(base_identity, user, scope)

        identity = {
            'id': base_identity.id,
            'owner': base_identity.owner,
            'gender': base_identity.gender,
            'is_public': base_identity.is_public,
            'names': visible_names,
            'relationships': []
        }
        
        if scope == 'owned':
            relationships = IdentityRelationship.objects.filter(identity=base_identity)
            for relationship in relationships:
                identity['relationships'].append({
                    'id': relationship.id,
                    'relationship_type': relationship.relationship_type.name,
                    'consumer': relationship.consumer.username
                })
        
        final_identities.append(identity)
        
    context = {
        'identities': final_identities,
        'scope': scope,
        'consumers': consumers, 
        'relationship_types': RelationshipType.objects.all(),
        'name_contexts': NameContext.objects.all()
    }
    
    return render(request, 'ui/identity_list.html', context)

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
                return redirect('ui:identity-list?scope=owned')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = IdentityCreateForm()
    
    return render(request, 'ui/create_identity.html', {'form': form})

@login_required
def delete_identity(request, identity_id):
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to delete this identity.')
    
    if identity.owner == request.user:
        identity.delete()
        messages.success(request, 'Identity deleted successfully!')
        
    return redirect_to_owned_identites()

@login_required
def edit_identity(request, identity_id):
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identites()
    
    if request.method == 'POST':
        form = IdentityEditForm(request.POST)
        if form.is_valid():
            identity.gender = form.cleaned_data['gender']
            identity.is_public = form.cleaned_data['is_public']
            identity.save()
              
            messages.success(request, 'Identity updated successfully!')
            return redirect_to_owned_identites()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = IdentityEditForm(initial={
            'gender': identity.gender,
            'is_public': identity.is_public,
        })

    return render(request, 'ui/edit_identity.html', {'form': form})

# relationship related views
@login_required
def add_relationship(request):
    identity_id = request.POST.get('identity_id')
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
    
    if request.method == 'POST':
        relationship_type_id = request.POST.get('relationship_type_id')
        consumer_id = request.POST.get('consumer')

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

        messages.success(request, 'Access added successfully!')
    
    return redirect_to_owned_identites()

@login_required
def delete_relationship(request, relationship_id):
    relationship = IdentityRelationship.objects.get(id=relationship_id)
    identity = Identity.objects.get(id=relationship.identity.id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
    
    if relationship.identity.owner == request.user:
        relationship.delete()
        messages.success(request, 'Access deleted successfully!')
        
    return redirect_to_owned_identites()

# name related views
@login_required
def add_name(request):
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        
    if request.method == 'POST':
        identity_id = request.POST.get('identity_id')
        name_context_id = request.POST.get('name_context_id')
        name_value = request.POST.get('name_value')
        is_default = request.POST.get('is_default') == 'on'

        name_context = NameContext.objects.get(id=name_context_id)

        if is_default:
            IdentityName.objects.filter(identity=identity, is_default=True).update(is_default=False)

        IdentityName.objects.create(
            identity=identity,
            name_context=name_context,
            name_value=name_value,
            is_default=is_default
        )

        messages.success(request, 'Name added successfully!')
    return redirect_to_owned_identites()
    
@login_required
def delete_name(request, name_id):
    name = IdentityName.objects.get(id=name_id)
    identity = Identity.objects.get(id=name.identity.id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
    
    if identity.owner == request.user:
        name.delete()
        messages.success(request, 'Name deleted successfully!')
        
    return redirect_to_owned_identites()

@login_required
def edit_name(request, name_id):
    name = IdentityName.objects.get(id=name_id)
    identity = Identity.objects.get(id=name.identity.id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identites()
    
    if request.method == 'POST':
        form = NameEditForm(request.POST)
        
        if form.is_valid():
            if name.is_default and form.cleaned_data['is_default'] == False:
                messages.error(request, 'Cannot unset default name without setting another name as default.')
                return redirect_to_owned_identites()
            
            name.name_context = form.cleaned_data['name_context']
            name.name_value = form.cleaned_data['name_value']
            name.is_default = form.cleaned_data['is_default']
            
            if name.is_default:
                IdentityName.objects.filter(identity=identity, is_default=True).exclude(id=name.id).update(is_default=False)
            
            name.save()
              
            messages.success(request, 'Name updated successfully!')
            return redirect_to_owned_identites()
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = NameEditForm(initial={
            'name_context': name.name_context,
            'name_value': name.name_value,
            'is_default': name.is_default,
        })
    
    return render(request, 'ui/edit_name.html', {'form': form})

# helper functions
def filter_names_by_access(identity, user, scope):
    accessible_names = []
    if scope in ('owned','public'):
            accessible_names = identity.names.all()
    elif scope == 'shared':
        if identity.is_public:
            accessible_names = identity.names.all()
        else:
            # find relationship between user and identity
            relationship_type = (RelationshipType.objects.filter(identityrelationship__identity=identity, identityrelationship__consumer=user).first())
            
            print(relationship_type)
        
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

def redirect_to_owned_identites():
    url = reverse('ui:identity-list')
    return redirect(f'{url}?scope=owned')