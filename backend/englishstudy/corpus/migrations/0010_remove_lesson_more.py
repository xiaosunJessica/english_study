# Generated by Django 4.2.21 on 2025-06-13 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0009_delete_lessontest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='more',
        ),
    ]
