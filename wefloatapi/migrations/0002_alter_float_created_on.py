# Generated by Django 4.1.3 on 2025-03-05 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wefloatapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='float',
            name='created_on',
            field=models.DateField(auto_now_add=True),
        ),
    ]
