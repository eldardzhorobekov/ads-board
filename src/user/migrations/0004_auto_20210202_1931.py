# Generated by Django 3.1.5 on 2021-02-02 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210202_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True, verbose_name='email address'),
        ),
    ]
