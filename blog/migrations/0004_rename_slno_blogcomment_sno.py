# Generated by Django 5.0.7 on 2024-10-29 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogcomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogcomment',
            old_name='slno',
            new_name='Sno',
        ),
    ]
