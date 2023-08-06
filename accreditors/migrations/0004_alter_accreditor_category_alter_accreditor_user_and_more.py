# Generated by Django 4.2.3 on 2023-08-05 10:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_user_email'),
        ('accreditors', '0003_alter_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accreditor',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='core.category'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accreditor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='application',
            name='pro_certificate',
            field=models.FileField(upload_to='media/resume', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]