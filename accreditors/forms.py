from django import forms
from django.forms import ModelForm, Textarea, inlineformset_factory
from .models import Application, Accreditor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import User
from django.forms import formset_factory




class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the password1 field's help_text
        self.fields['password1'].help_text = ''
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_accreditor = True
        if commit:
            user.save()
        return user
    

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)

######################## Processing form method #########################
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        #fields = '__all__'
        fields = ['full_name', 'position', 'profession', 'passport_photo', 'means_of_identity', 'reg_certificate', 'curr_license', 'resume']
        exclude = ['status']  # Exclude the 'status' field from the form
        widgets = {
            'reg_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'curr_license': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'resume': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'DELETE': forms.HiddenInput()
        }
        labels = {
            'reg_certificate': 'Regulatory Body Reg. Certificate(pdf)',
            'curr_license': 'Current Practising License (pdf)',
            'resume': 'Upload Resume (pdf)',
            'means_of_identity': 'Means of Identity',
        }
        
    def clean(self):
        cleaned_data = super().clean()
        accreditor = cleaned_data.get('accreditor')
        position = cleaned_data.get('position')

        # Check if an application with the same accreditor and position already exists
        if accreditor and position == 'team lead':
            existing_team_lead_applications = Application.objects.filter(accreditor=accreditor, position='team lead')
            if self.instance:  # Exclude the current instance during edit
                existing_team_lead_applications = existing_team_lead_applications.exclude(pk=self.instance.pk)

            if existing_team_lead_applications.exists():
                raise forms.ValidationError("An application with the same accreditor already has a Team lead.")

        return cleaned_data


AccreditorApplicationFormSet = inlineformset_factory(Accreditor, Application, form=ApplicationForm, extra=1, can_delete=False)


class ApplicationForms(forms.ModelForm):
    class Meta:
        model = Application
        # fields = '__all__'
        fields = ['full_name', 'position', 'profession', 'passport_photo', 'means_of_identity', 'reg_certificate', 'curr_license', 'resume']
        exclude = ['status']  # Exclude the 'status' field from the form

        widgets = {
            'reg_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'curr_license': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'resume': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'DELETE': forms.HiddenInput()
        }

        labels = {
            'reg_certificate': 'Regulatory Body Reg. Certificate(pdf)',
            'curr_license': 'Current Practising License (pdf)',
            'resume': 'Upload Resume(pdf)',
            'means_of_identity': 'LASRRA Number',
        }
        

################ working section #################
MyApplicationFormSet = formset_factory(ApplicationForm, extra=1)

class MyApplicationForm(ApplicationForm):
    pass  # This is an empty class that inherits from ApplicationForm



class AccreditorApplicationForm(forms.ModelForm):
    class Meta:
        model = Accreditor
        fields = ['category', 'contact_number', 'contact_email', 'contact_address', 'expression_doc']

    def __init__(self, *args, accreditor=None, **kwargs):
        super(AccreditorApplicationForm, self).__init__(*args, **kwargs)
        self.accreditor = accreditor













class AccreditorForm(forms.ModelForm):
    class Meta:
        model = Accreditor
        fields = ['category', 'contact_number', 'contact_email', 'contact_address', 'expression_doc']

    def __init__(self, *args, **kwargs):
        super(AccreditorForm, self).__init__(*args, **kwargs)
        self.user = kwargs.get('instance', None)
        if self.user:
            self.fields['category'].widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        instance = super(AccreditorForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    
    
    
    
class ApplicationForms(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name',  'position', 'profession', 'means_of_identity', 'reg_certificate', 'curr_license', 'resume', 'passport_photo']
        
        widgets = {
            'reg_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'curr_license': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'resume': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'DELETE': forms.HiddenInput()
        }

        labels = {
            'reg_certificate': 'Regulatory Body Reg. Certificate(pdf)',
            'curr_license': 'Current Practising License (pdf)',
            'resume': 'Upload Resume(pdf)',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ApplicationForms, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ApplicationForms, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    
    
ApplicationFormSet = inlineformset_factory(Accreditor, Application, fields=['full_name', 'position', 'profession', 'means_of_identity', 'passport_photo', 'reg_certificate', 'curr_license', 'resume'], extra=1)
