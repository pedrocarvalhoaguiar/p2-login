# Generated by Django 4.2.1 on 2023-05-29 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_birthday_paidbill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]