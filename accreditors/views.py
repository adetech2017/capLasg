from django.shortcuts import render, redirect
#from .models import Application, Accreditor, Status
from .forms import AccreditorForm, ApplicationForm, AccreditorApplicationFormSet
from core.models import Category, Status
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, CustomLoginForm
from core.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import logout
from .models import Accreditor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import logging
from django.contrib.auth.decorators import login_required
from .models import Application

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

def help(request):
    return render(request, "help.html")

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

                return redirect('home')  # Replace 'home' with the URL to redirect after registration
    else:
        user_form = UserRegistrationForm()

    return render(request, 'signUp.html', {'user_form': user_form})


def logout_view(request):
    logout(request)
    return redirect('accreditors:index')



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

        formset = [ApplicationForm(request.POST, request.FILES, prefix=str(i)) for i in range(3)]  # Change 3 to the number of initial forms you want

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
        formset = [ApplicationForm(prefix=str(i)) for i in range(3)]  # Change 3 to the number of initial forms you want

    return render(request, 'dashboard/application_form.html', {'accreditor_form': accreditor_form, 'formset': formset})