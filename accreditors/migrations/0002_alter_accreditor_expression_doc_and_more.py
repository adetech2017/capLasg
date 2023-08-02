# Generated by Django 4.2.3 on 2023-08-01 20:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accreditors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accreditor',
            name='expression_doc',
            field=models.FileField(blank=True, null=True, upload_to='media/expression_doc', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
        migrations.AlterField(
            model_name='application',
            name='position',
            field=models.CharField(choices=[('member', 'Member'), ('team lead', 'Team Lead')], default='member', max_length=50),
        ),
    ]
