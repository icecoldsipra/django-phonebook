# Generated by Django 3.0.1 on 2019-12-21 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Registered User', 'verbose_name_plural': 'Registered Users'},
        ),
    ]
