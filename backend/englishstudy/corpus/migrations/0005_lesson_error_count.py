# Generated by Django 4.2.21 on 2025-06-11 05:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('corpus', '0004_rename_book_lesson_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='error_count',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
