from django import forms
from identity.models import *

class IdentityCreateForm(forms.Form):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=True)
    is_public = forms.BooleanField(initial=False, required=False)
    default_name_context = forms.ModelChoiceField(queryset=NameContext.objects.all(), required=True)
    default_name_value = forms.CharField(max_length=100, required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].label_from_instance = (
            lambda gender: gender.name
        )

        self.fields['default_name_context'].label_from_instance = (
            lambda context: context.name
        )
        
class IdentityEditForm(forms.Form):
    gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=True)
    is_public = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].label_from_instance = (
            lambda gender: gender.name
        )
        
class NameEditForm(forms.Form):
    name_context = forms.ModelChoiceField(queryset=NameContext.objects.all(), required=True)
    name_value = forms.CharField(max_length=100, required=True)
    is_default = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name_context'].label_from_instance = (
            lambda context: context.name
        )