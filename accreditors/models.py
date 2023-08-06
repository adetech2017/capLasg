from django.db import models
from core.models import User, Category, Status
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class AccreditorManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class Accreditor(models.Model):
    USER_TYPE_CHOICES = (
        ('accreditor', 'Accreditor'),
    )
    
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='accreditor')
    accreditor_code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=20)
    contact_email = models.CharField(max_length=100)
    contact_address = models.CharField(max_length=200)
    expression_doc = models.FileField(upload_to='media/expression_doc', validators=[FileExtensionValidator(['pdf'])], null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Required field for authentication using email
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

    objects = AccreditorManager()
    
    def _generate_accreditor_code(self):
        current_year = timezone.now().year % 100
        return f"CAP-{current_year:02d}"

    def save(self, *args, **kwargs):
        if not self.accreditor_code:
            base_code = self._generate_accreditor_code()
            code_suffix = "0001"

            # Find the highest existing code to get the last counter
            last_accreditor = Accreditor.objects.filter(accreditor_code__startswith=base_code).order_by('-accreditor_code').first()
            if last_accreditor:
                last_code = last_accreditor.accreditor_code[len(base_code):]
                try:
                    counter = int(last_code) + 1
                    code_suffix = f"{counter:04d}"  # Adjust the format based on your requirements
                except ValueError:
                    pass

            self.accreditor_code = f"{base_code}{code_suffix}"

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.contact_number


class Application(models.Model):
    PRO_TYPE_CHOICES = (
        ('none', 'None'),
        ('architect', 'Architect'),
        ('Town Planner', 'Town Planner'),
        ('civil/structural engineer', 'Civil/Structural Engineer'),
        ('mechanical engineer', 'Mechanical Engineer'),
        ('electrical engineer', 'Electrical Engineer'),
        ('builder', 'Builder'),
        ('geoscientist', 'Geoscientist'),
    )
    
    TEAM_TYPE_CHOICES = (
        ('member', 'Member'),
        ('team lead', 'Team Lead'),
    )
    
    accreditor = models.ForeignKey(Accreditor, related_name='applications', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100)
    reg_body_no = models.CharField(max_length=50)
    #years_of_experience = models.PositiveIntegerField(default=0)
    position = models.CharField(max_length=50, choices=TEAM_TYPE_CHOICES, default='member')
    profession = models.CharField(max_length=50, choices=PRO_TYPE_CHOICES, default='none')
    lasrra = models.FileField(upload_to='media/lasrra', validators=[FileExtensionValidator(['pdf'])])
    reg_certificate = models.FileField(upload_to='media/reg_certificate', validators=[FileExtensionValidator(['pdf'])])
    curr_license = models.FileField(upload_to='media/curr_license', validators=[FileExtensionValidator(['pdf'])])
    pro_certificate = models.FileField(upload_to='media/resume', validators=[FileExtensionValidator(['pdf'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    accreditor = models.ForeignKey(Accreditor, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer}"