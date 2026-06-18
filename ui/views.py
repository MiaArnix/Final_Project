from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from identity.models import Gender, NameContext, RelationshipType, IdentityNameAccess, Identity

def index(request):
    return render(request, 'ui/index.html')

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
        'identities': Identity.objects.filter(owner=request.user)
    }
    return render(request, 'ui/identity_list.html', context)
