# Generated by Django 3.2.23 on 2023-12-05 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
    ]