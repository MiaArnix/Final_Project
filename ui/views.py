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

def metadata_list(request):
    context = {
        'genders': Gender.objects.all().order_by('id'),
        'name_contexts': NameContext.objects.all().order_by('id'),
        'relationship_types': RelationshipType.objects.all().order_by('id'),
        'identity_name_access': IdentityNameAccess.objects.all().order_by('id'),
    }
    return render(request, 'ui/metadata_list.html', context)

# identity related views
def identity_list(request):
    scope = request.GET.get('scope')
    user = request.user
    consumers = None
    public_identities = Identity.objects.filter(is_public=True).order_by('id')
    identity_list = public_identities
    
    if not user.is_authenticated:
        scope = 'public'
    
    if user.is_authenticated:    
        if scope == 'owned':
            identity_list = Identity.objects.filter(owner=user).order_by('id')
            consumers = AuthUser.objects.exclude(id=user.id)
        elif scope == 'shared':
            shared_identities = Identity.objects.filter(relationships__consumer=user).order_by('id')
            identity_list = (public_identities | shared_identities).distinct()
        
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
            relationships = IdentityRelationship.objects.filter(identity=base_identity).order_by('id')
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
        'relationship_types': RelationshipType.objects.all().order_by('id'),
        'name_contexts': NameContext.objects.all().order_by('id')
    }
    
    return render(request, 'ui/identity_list.html', context)

@login_required
def create_identity(request):
    # a GET is the user opening the page from the navigation, so it has to render
    # the empty form - the template posts back to this same url
    if request.method != 'POST':
        return render(request, 'ui/create_identity.html', {'form': IdentityCreateForm()})

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
                is_default=True)
                
            messages.success(request, 'Identity created successfully!')
            return redirect(f"{reverse('ui:identity-list')}?scope=owned")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{field}: {error}')
    
    return render(request, 'ui/create_identity.html', {'form': form})

@login_required
def delete_identity(request, identity_id):
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to delete this identity.')
        return redirect_to_owned_identities()
    
    if identity.owner == request.user:
        identity.delete()
        messages.success(request, 'Identity deleted successfully!')
        
    return redirect_to_owned_identities()

@login_required
def edit_identity(request, identity_id):
    identity = Identity.objects.get(id=identity_id)

    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identities()

    if request.method == 'POST':
        form = IdentityEditForm(request.POST)
        if form.is_valid():
            identity.gender = form.cleaned_data['gender']
            identity.is_public = form.cleaned_data['is_public']
            identity.save()
            messages.success(request, 'Identity updated successfully!')
            return redirect_to_owned_identities()
    else:
        form = IdentityEditForm(initial={
            'gender': identity.gender,
            'is_public': identity.is_public,
        })

    return render(request, 'ui/edit_identity.html', {'form': form})

# relationship related views
@login_required
def add_relationship(request):
    if request.method != 'POST':
        return redirect_to_owned_identities()
    
    identity_id = request.POST.get('identity_id')
    identity = Identity.objects.get(id=identity_id)
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identities()
        
    relationship_type_id = request.POST.get('relationship_type_id')
    consumer_id = request.POST.get('consumer')

    try:
        relationship_type = RelationshipType.objects.get(id=relationship_type_id)
    except RelationshipType.DoesNotExist:
        messages.error(request, 'Invalid relationship type selected.')
        return redirect_to_owned_identities()
    
    try:        
        consumer = AuthUser.objects.get(id=consumer_id)
    except AuthUser.DoesNotExist:      
        messages.error(request, 'Invalid consumer selected.')
        return redirect_to_owned_identities()

    if not IdentityRelationship.objects.filter(identity=identity, consumer=consumer).exists():
        IdentityRelationship.objects.create(
            identity = identity,
            relationship_type = relationship_type,
            consumer = consumer
            )
        messages.success(request, 'Access added successfully!')
    else:
        messages.error(request, 'Access already exists!')
    
    return redirect_to_owned_identities()

@login_required
def delete_relationship(request, relationship_id):
    if request.method != 'POST':
        return redirect_to_owned_identities()
    
    try:
        relationship = IdentityRelationship.objects.get(id=relationship_id)
    except IdentityRelationship.DoesNotExist:
        messages.error(request, 'Relationship does not exist.')
        return redirect_to_owned_identities()
    
    identity_id = relationship.identity.id
    
    try:
        identity = Identity.objects.get(id=identity_id)
    except Identity.DoesNotExist:
        messages.error(request, 'Identity does not exist.')
        return redirect_to_owned_identities()
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identities()
    
    if relationship.identity.owner == request.user:
        relationship.delete()
        messages.success(request, 'Access deleted successfully!')
        
    return redirect_to_owned_identities()

# name related views
@login_required
def add_name(request):
    if request.method == 'POST':
        identity_id = request.POST.get('identity_id')
        name_context_id = request.POST.get('name_context_id')
        name_value = request.POST.get('name_value')
        is_default = request.POST.get('is_default') == 'on'

        identity = Identity.objects.get(id=identity_id)
        
        if identity.owner != request.user:
            messages.error(request, 'You do not have permission to edit this identity.')
            return redirect_to_owned_identities()
        
        try:
            name_context = NameContext.objects.get(id=name_context_id)
        except NameContext.DoesNotExist:
            messages.error(request, 'Invalid name context selected.')
            return redirect_to_owned_identities()
        
        if name_value.strip() == '':
            messages.error(request, 'Name value cannot be empty.')
            return redirect_to_owned_identities()

        if is_default:
            IdentityName.objects.filter(identity=identity, is_default=True).update(is_default=False)

        if IdentityName.objects.filter(identity=identity, name_context=name_context).exists():
            messages.error(request, 'A name with this context already exists for this identity.')
            return redirect_to_owned_identities()
        
        IdentityName.objects.create(
            identity=identity,
            name_context=name_context,
            name_value=name_value,
            is_default=is_default
        )

        messages.success(request, 'Name added successfully!')
    return redirect_to_owned_identities()
    
@login_required
def delete_name(request, name_id):
    try:
        name = IdentityName.objects.get(id=name_id)
    except IdentityName.DoesNotExist:
        messages.error(request, 'Name does not exist.')
        return redirect_to_owned_identities()
    
    identity = Identity.objects.get(id=name.identity.id)
    
    if name.is_default == True:
        messages.error(request, 'Cannot delete the default name. Please set another name as default before deleting this one.')
        return redirect_to_owned_identities()
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identities()
    
    if identity.owner == request.user:
        name.delete()
        messages.success(request, 'Name deleted successfully!')
        
    return redirect_to_owned_identities()

@login_required
def edit_name(request, name_id):
    try:
        name = IdentityName.objects.get(id=name_id)
    except IdentityName.DoesNotExist:
        messages.error(request, 'Name does not exist.')
        return redirect_to_owned_identities()
    
    identity = Identity.objects.get(id=name.identity.id)  
    
    if identity.owner != request.user:
        messages.error(request, 'You do not have permission to edit this identity.')
        return redirect_to_owned_identities()
    
    if request.method == 'POST':
        form = NameEditForm(request.POST)
               
        if form.is_valid():
            if name.is_default and form.cleaned_data['is_default'] == False:
                messages.error(request, 'Cannot unset default name without setting another name as default.')
                return redirect_to_owned_identities()
            
            name.name_context = form.cleaned_data['name_context']
            name.name_value = form.cleaned_data['name_value']
            name.is_default = form.cleaned_data['is_default']
            
            if IdentityName.objects.filter(identity=identity, name_context=name.name_context).exclude(id=name.id).exists():
                messages.error(request, 'A name with this context already exists for this identity.')
                return redirect_to_owned_identities()         
                      
            if name.is_default:
                IdentityName.objects.filter(identity=identity, is_default=True).exclude(id=name.id).update(is_default=False)
            
            name.save()
              
            messages.success(request, 'Name updated successfully!')
            return redirect_to_owned_identities()
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
    if scope in ('owned', 'public', None):
            accessible_names = identity.names.all()
    elif scope == 'shared':
        if identity.is_public:
            accessible_names = identity.names.all().order_by('id')
        else:
            # find relationship between user and identity
            relationship_type = (RelationshipType.objects.filter(identityrelationship__identity=identity, identityrelationship__consumer=user).first())
            
            if relationship_type is None:
                return []
            
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

def redirect_to_owned_identities():
    url = reverse('ui:identity-list')
    return redirect(f'{url}?scope=owned')