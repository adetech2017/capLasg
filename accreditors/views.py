from django.shortcuts import render, redirect
#from .models import Application, Accreditor, Status
from core.models import Category, Status
from django.contrib.auth import login, authenticate
from .forms import ApplicationForm, MyApplicationFormSet, MyApplicationForm, AccreditorForm, UserRegistrationForm, CustomLoginForm, ApplicationForms, AccreditorApplicationForm, ApplicationFormSet, formset_factory
from core.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import logout
from .models import Accreditor, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import logging
from django.contrib.auth.decorators import login_required
from .models import Application
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import traceback
from django.contrib import messages
from django.urls import reverse
import sweetify
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)





def index(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def help(request):
    return render(request, "help.html")

def policy(request):
    return render(request, "policy.html")

@login_required
def home(request):
    # Get the current authenticated Accreditor
    accreditor = Accreditor.objects.filter(user=request.user).first()

    if accreditor:
        # Get all applications related to the current authenticated Accreditor
        applications = accreditor.applications.all()
    else:
        applications = []
        
    return render(request, "dashboard/index.html", {'applications': applications})


def login_view(request):
    if request.user.is_authenticated:
        # User is already authenticated, redirect to the dashboard
        return redirect('accreditors:dashboard')
    
    
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate user and log them in
            user = form.get_user()
            login(request, user)
            return redirect('accreditors:dashboard')  # Replace 'home' with the URL to redirect after successful login
        else:
            # Display an error message for invalid credentials
            messages.error(request, 'Invalid credentials. Please try again.')
    
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                # Email already exists, show an error message
                user_form.add_error('email', 'Email already exists')
            else:
                # Save the user instance
                user = user_form.save()

                # Log in the user after successful registration
                user = authenticate(username=user.email, password=user_form.cleaned_data['password1'])
                login(request, user)

                return redirect('accreditors:dashboard')  # Replace 'home' with the URL to redirect after registration
    else:
        user_form = UserRegistrationForm()

    return render(request, 'signUp.html', {'user_form': user_form})


def logout_view(request):
    logout(request)
    return redirect('accreditors:index')

@login_required
def application_form_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('application_form')  # Redirect to the same page after form submission

    else:
        form = ApplicationForm()

    # Get the list of accreditors for the table
    accreditors = Accreditor.objects.all()

    return render(request, 'dashboard/application.html', {'form': form, 'accreditors': accreditors})

# working method
# @login_required
# def accreditor_application_create_view(request):
#     accreditor = Accreditor.objects.filter(user=request.user).first()
#     formset = ApplicationFormSet(queryset=accreditor.applications.all() if accreditor else None, prefix='application')

#     if request.method == 'POST':
#         accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor) # instance of Accreditor exists
#         formset = ApplicationFormSet(request.POST, request.FILES, queryset=accreditor.applications.all() if accreditor else None, prefix='application')
#         accreditor_form = AccreditorForm(request.POST, request.FILES)
#         formset = AccreditorApplicationFormSet(request.POST, request.FILES, prefix='application')

#         if accreditor_form.is_valid() and formset.is_valid():
#             accreditor = accreditor_form.save(commit=False)
#             accreditor.user = request.user  # Assign the authenticated user to the user field
#             accreditor.save()

#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.accreditor = accreditor
#                 instance.save()
#             return redirect('accreditors:dashboard')  # Replace 'success' with the URL name for the success page
#         else:
#             # Handle form validation errors
#             pass
#     else:
#         accreditor_form = AccreditorForm()
#         formset = AccreditorApplicationFormSet(prefix='application')

#     return render(request, 'dashboard/accreditor_application_form.html', {'accreditor_form': accreditor_form, 'formset': formset})



@login_required
def accreditor_application_create_view(request):
    accreditor = Accreditor.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if accreditor:
            accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor)
        else:
            accreditor_form = AccreditorForm(request.POST, request.FILES)

        #formset = [ApplicationForm(request.POST, request.FILES, prefix=str(i)) for i in range(3)]  # Change 3 to the number of initial forms you want
        formset = [ApplicationForm(prefix='form-0')]

        if accreditor_form.is_valid() and all(form.is_valid() for form in formset):
            accreditor = accreditor_form.save(commit=False)
            accreditor.user = request.user
            accreditor.save()

            for form in formset:
                application = form.save(commit=False)
                application.accreditor = accreditor
                application.save()

            return redirect('accreditors:dashboard')  # Replace 'success' with the URL name for the success page
    else:
        if accreditor:
            accreditor_form = AccreditorForm(instance=accreditor)
        else:
            accreditor_form = AccreditorForm()
        formset = [ApplicationForm(prefix='form-0')]
        #formset = [ApplicationForm(prefix=str(i)) for i in range(3)]  # Change 3 to the number of initial forms you want

    return render(request, 'dashboard/application_form.html', {'accreditor_form': accreditor_form, 'formset': formset})


def download_document(request):
    document_path = os.path.join(settings.STATICFILES_DIRS[0], 'cap-lag.pdf')
    if os.path.exists(document_path):
        with open(document_path, 'rb') as document_file:
            response = HttpResponse(document_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="cap-lag.pdf"'
            return response
    else:
        return HttpResponse('Document not found', status=404)
    

class MyFormView(View):
    def get(self, request):
        user = request.user
        accreditor = Accreditor.objects.filter(user=user).first()

        accreditor_form = AccreditorForm(instance=accreditor) if accreditor else AccreditorForm()
        application_formset = MyApplicationFormSet()

        return render(request, 'dashboard/my_template.html', {
            'accreditor_form': accreditor_form,
            'application_formset': application_formset,
            'accreditor_id': accreditor.id if accreditor else None,  # Include the accreditor_id in the context
        })

    def post(self, request):
        try:
            user = request.user
            #accreditor = None
            accreditor_form = AccreditorForm(request.POST, request.FILES)
            application_formset = MyApplicationFormSet(request.POST, request.FILES)

            accreditor_id = request.POST.get('accreditor_id', None)  # Get the accreditor_id from the POST data

            if 'save' in request.POST and accreditor_form.is_valid() and application_formset.is_valid():
                if accreditor_id:
                    # Fetch the Accreditor object based on the accreditor_id (primary key)
                    accreditor = get_object_or_404(Accreditor, pk=accreditor_id)
                else:
                    # If accreditor_id does not exist, create a new Accreditor
                    accreditor = accreditor_form.save(commit=False)
                    accreditor.user = user
                    accreditor.created_at = accreditor_form.cleaned_data.get('created_at') or timezone.now()
                    accreditor.updated_at = timezone.now()
                    accreditor.save()

                for application_form in application_formset:
                    if application_form.is_valid():
                        application = application_form.save(commit=False)

                        # Link the application to the corresponding accreditor using accreditor_id
                        application.accreditor_id = accreditor.id

                        if accreditor_id:
                            application.existing_accreditor_id = accreditor_id

                        application.created_at = application_form.cleaned_data.get('created_at') or timezone.now()
                        application.updated_at = timezone.now()
                        application.save()
                
                # Set the success message
                messages.success(request, "Application submitted successfully!")

                return redirect('accreditors:dashboard')  # Replace 'success_page' with the actual URL name for the success page
            
            elif 'add_application' in request.POST:
                if accreditor_id:
                    accreditor = get_object_or_404(Accreditor, pk=accreditor_id)
                else:
                    accreditor = accreditor_form.save(commit=False)
                    accreditor.user = user
                    accreditor.created_at = accreditor_form.cleaned_data.get('created_at') or timezone.now()
                    accreditor.updated_at = timezone.now()
                    accreditor.save()

                # Add another empty application form to the formset
                application_formset.forms.append(MyApplicationForm())

            else:
                # Handle other cases (e.g., 'save_and_continue' button)
                pass

            context = {
                'accreditor_form': accreditor_form,
                'application_formset': application_formset,
                'accreditor_id': accreditor.id,
            }

            return render(request, 'dashboard/my_template.html', context)
        except Exception as e:
            # Get the traceback information
            trace = traceback.format_exc()
            # Print the traceback to the console (for debugging purposes)
            print(trace)
            # Pass the traceback to the template for displaying the error
            return render(request, 'dashboard/error_template.html', {'traceback': trace})

    # def post(self, request):
    #     user = request.user
        
    #     accreditor_form = AccreditorForm(request.POST, request.FILES)
    #     application_formset = MyApplicationFormSet(request.POST, request.FILES)

    #     if 'save' in request.POST and accreditor_form.is_valid() and application_formset.is_valid():
    #         user_id = request.POST.get('user_id', None)
    #         accreditor_id = request.POST.get('accreditor_id', None)

    #         # Check if user_id exists to update the AccreditorForm
    #         if user_id:
    #             accreditor = Accreditor.objects.get(pk=user_id)
    #             accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor)
    #         else:
    #             accreditor = accreditor_form.save(commit=False)

    #         # Add user to the Accreditor object
    #         accreditor.user = user

    #         accreditor_form.save()

    #         for application_form in application_formset:
    #             if application_form.is_valid():
    #                 application = application_form.save(commit=False)
    #                 application.accreditor = accreditor  # Link the application to the corresponding accreditor
    #                 application.save()

    #         # Redirect to a success page or do something else after saving

    #     elif 'add_application' in request.POST:  # Handle adding a new application form
    #         # Save the existing accreditor data (if applicable)
    #         user_id = request.POST.get('user_id', None)
    #         accreditor_id = request.POST.get('accreditor_id', None)
    #         if user_id:
    #             accreditor = Accreditor.objects.get(pk=user_id)
    #             accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor)
    #             accreditor_form.save()
    #         else:
    #             accreditor = accreditor_form.save()

    #         # Add another empty application form to the formset
    #         application_formset = MyApplicationFormSet(request.POST, request.FILES)

    #         # Check if the formset is valid, and if so, add the form to the formset
    #         if application_formset.is_valid():
    #             application_formset.forms.append(MyApplicationForm())
    #     else:
    #         # Handle other cases (e.g., 'save_and_continue' button)
    #         pass

        








# class MyFormView(View):
#     def get(self, request):
#         accreditor = Accreditor.objects.filter(user=request.user).first()
#         applications = Application.objects.filter(accreditor=accreditor) if accreditor else None
#         form = AccreditorForm(accreditor=accreditor)
#         #formset = ApplicationFormSet(queryset=applications)
#         context = {'form': form}
#         return render(request, 'dashboard/my_template.html', context)
    
#     # def get(self, request):
#     #     category_name = request.GET.get('category', None)
#     #     accreditor = Accreditor.objects.filter(user=request.user).first()

#     #     if request.user.is_authenticated:
#     #         try:
#     #             category = Category.objects.get(category=category_name)
#     #             accreditor = Accreditor.objects.get(user=request.user, category=category)
#     #             accreditor_form = AccreditorForm(instance=accreditor)
#     #         except (Category.DoesNotExist, Accreditor.DoesNotExist):
#     #             accreditor = None
#     #             accreditor_form = AccreditorForm(initial={'category': category_name})
#     #     else:
#     #         accreditor = None
#     #         accreditor_form = AccreditorForm(initial={'category': category_name})

#     #     application_formset = MyApplicationFormSet()
#     #     return render(request, 'dashboard/my_template.html', {'accreditor_form': accreditor_form, 'application_formset': application_formset})

#     def post(self, request):
#         if not request.user.is_authenticated:
#             return redirect('login')  # Redirect to the login page if the user is not authenticated

#         category_name = request.POST.get('category', None)
#         try:
#             category = Category.objects.get(category=category_name)
#             accreditor = Accreditor.objects.get(user=request.user, category=category)
#         except (Category.DoesNotExist, Accreditor.DoesNotExist):
#             accreditor = None

#         if accreditor:
#             # Disable the category field in the form to prevent updating
#             accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor, disable_category=True)
#         else:
#             # Create a new form with the category_name provided
#             accreditor_form = AccreditorForm(request.POST, request.FILES)

#         application_formset = MyApplicationFormSet(request.POST, request.FILES)

#         if 'save' in request.POST and accreditor_form.is_valid() and application_formset.is_valid():
#             if not accreditor:
#                 accreditor = accreditor_form.save(commit=False)
#                 accreditor.user = request.user
#                 accreditor.category = category
#                 accreditor.save()

#             for application_form in application_formset:
#                 if application_form.is_valid() and not application_form.cleaned_data.get('DELETE'):
#                     application = application_form.save(commit=False)
#                     application.accreditor = accreditor
#                     application.save()

#             # Check if "Save and Continue" button is clicked
#             if 'save_and_continue' in request.POST:
#                 # Create a new formset with an empty form for the next entry
#                 application_formset = MyApplicationFormSet()
#             else:
#                 # Redirect to a success page or do something else after saving
#                 return redirect('success_page')  # Replace 'success_page' with your desired URL name

#         return render(request, 'dashboard/my_template.html', {'accreditor_form': accreditor_form, 'application_formset': application_formset})
    
    
    
    



class AddAccreditorApplicationView(LoginRequiredMixin, View):
    def get(self, request):
        accreditor = Accreditor.objects.filter(user=request.user).first()
        applications = Application.objects.filter(accreditor=accreditor) if accreditor else None

        # Pass instance to AccreditorApplicationForm to display existing details
        form = AccreditorApplicationForm(accreditor=accreditor)
        formset = ApplicationFormSet(queryset=applications)
        context = {'form': form, 'formset': formset}
        return render(request, 'dashboard/add_accreditor_application.html', context)

    def post(self, request):
        accreditor = Accreditor.objects.filter(user=request.user).first()
        form = AccreditorApplicationForm(request.POST, request.FILES, accreditor=accreditor)
        formset = ApplicationFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            if not accreditor:
                accreditor = form.save(commit=False)
                accreditor.user = request.user
                accreditor.save()

            form.save()  # Save accreditor details

            for form in formset:
                application = form.save(commit=False)
                application.accreditor = accreditor
                application.save()

            return redirect('applications_list')  # Redirect to a list view of applications

        context = {'form': form, 'formset': formset}
        return render(request, 'dashboard/add_accreditor_application.html', context)
    
    
    
    
    
    
    
    
    
    

def create_accreditor_and_applications(request):
    user = request.user
    accreditor = Accreditor.objects.filter(user=user).first()
    accreditor_form = AccreditorForm(instance=accreditor)

    ApplicationFormSet = formset_factory(ApplicationForms, extra=1)
    application_formset = ApplicationFormSet(form_kwargs={'user': user})

    if request.method == 'POST':
        accreditor_form = AccreditorForm(request.POST, request.FILES, instance=accreditor)
        application_formset = ApplicationFormSet(request.POST, request.FILES, form_kwargs={'user': user})

        if accreditor_form.is_valid() and application_formset.is_valid():
            if not accreditor:
                accreditor = accreditor_form.save(commit=False)
                accreditor.user = user
                accreditor.save()

            for form in application_formset:
                if form.is_valid():
                    application = form.save(commit=False)
                    application.accreditor = accreditor
                    application.save()
            
            messages.success(request, 'Accreditor and applications saved successfully.')
            return redirect('accreditors:create_accreditor_application') 

        else:
            messages.error(request, 'Error in form submission. Please check the data.')
            
    context = {
        'accreditor_form': accreditor_form,
        'application_formset': application_formset,
    }
    return render(request, 'dashboard/create_accreditor.html', context)



