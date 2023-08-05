from django import forms
from django.forms import ModelForm, Textarea, inlineformset_factory
from .models import Application, Accreditor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from core.models import User
from django.forms import formset_factory




# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['full_name', 'reg_body_no', 'position', 'profession', 'lasrra', 'reg_certificate', 'curr_license', 'pro_certificate']
        
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.helper = FormHelper()
#             self.helper.layout = Layout(
#                 Row(
#                     Column('full_name', css_class='form-group col-md-6'),
#                     Column('reg_body_no', css_class='form-group col-md-6'),
#                     css_class='form-row'
#                 ),
#                 'position',
#                 'profession',
#                 'lasrra',
#                 'reg_certificate',
#                 'curr_license',
#                 'pro_certificate',
#                 Submit('submit', 'Create', css_class='btn btn-primary')
#             )
        

class AccreditorForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     disable_category = kwargs.pop('disable_category', False)
    #     super(AccreditorForm, self).__init__(*args, **kwargs)
    #     if disable_category:
    #         self.fields['category'].disabled = True
            
    class Meta:
        model = Accreditor
        exclude = ['description']
        #fields = '__all__'
        fields = ['category', 'contact_number', 'contact_email', 'contact_address']
        
        widgets = {
            'expression_doc': forms.FileInput(attrs={'accept': 'application/pdf'}),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Set default value for user_type if it's not already set
            if 'user_type' not in self.initial:
                self.initial['user_type'] = 'accreditor'
        
        def __init__(self, *args, **kwargs):
            super(AccreditorForm, self).__init__(*args, **kwargs)
            if not kwargs.get('instance'):
                self.fields['accreditor_code'].widget = forms.HiddenInput()
            else:
                self.fields['accreditor_code'].disabled = True

        # def __init__(self, *args, **kwargs):
        #     super(AccreditorForm, self).__init__(*args, **kwargs)
        #     if kwargs.get('instance'):
        #         self.fields['accreditor_code', 'expression_doc'].widget.attrs['readonly'] = True


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


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        #fields = '__all__'
        fields = ['full_name', 'reg_body_no', 'position', 'profession', 'lasrra', 'reg_certificate', 'curr_license', 'pro_certificate']
        exclude = ['status']  # Exclude the 'status' field from the form
        widgets = {
            'lasrra': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'reg_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'curr_license': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'pro_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'DELETE': forms.HiddenInput()
        }
        labels = {
            'reg_certificate': 'Regulatory Body Reg. Certificate(pdf)',
            'curr_license': 'Current Practising License (pdf)',
            'pro_certificate': 'Upload Resume Card (pdf)',
            'reg_body_no': 'Regulatory Body Reg. No',
            'lasrra': 'LASRRA (pdf)',            
        }
    

AccreditorApplicationFormSet = inlineformset_factory(Accreditor, Application, form=ApplicationForm, extra=1, can_delete=False)


class ApplicationForms(forms.ModelForm):
    class Meta:
        model = Application
        # fields = '__all__'
        fields = ['full_name', 'reg_body_no', 'position', 'profession', 'lasrra', 'reg_certificate', 'curr_license', 'pro_certificate']
        exclude = ['status']  # Exclude the 'status' field from the form

        widgets = {
            'lasrra': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'reg_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'curr_license': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'pro_certificate': forms.FileInput(attrs={'accept': 'application/pdf'}),
            'DELETE': forms.HiddenInput()
        }

        labels = {
            'reg_certificate': 'Regulatory Body Reg. Certificate(pdf)',
            'curr_license': 'Current Practising License (pdf)',
            'pro_certificate': 'Upload Resume Card (pdf)',
            'reg_body_no': 'Regulatory Body Registration No',
            'lasrra': 'LASRRA (pdf)',
        }

MyApplicationFormSet = formset_factory(ApplicationForm, extra=1)

class MyApplicationForm(ApplicationForm):
    pass  # This is an empty class that inherits from ApplicationForm



class AccreditorApplicationForm(forms.ModelForm):
    class Meta:
        model = Accreditor
        fields = ['category', 'contact_number', 'contact_email', 'contact_address', 'expression_doc', 'description']

    def __init__(self, *args, accreditor=None, **kwargs):
        super(AccreditorApplicationForm, self).__init__(*args, **kwargs)
        self.accreditor = accreditor


ApplicationFormSet = inlineformset_factory(Accreditor, Application, fields=['full_name', 'reg_body_no', 'position', 'profession', 'lasrra', 'reg_certificate', 'curr_license', 'pro_certificate'], extra=1)