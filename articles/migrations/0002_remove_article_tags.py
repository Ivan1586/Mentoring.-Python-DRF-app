# Generated by Django 4.2.2 on 2024-01-03 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
    ]