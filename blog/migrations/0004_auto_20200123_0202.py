# Generated by Django 3.0.2 on 2020-01-23 10:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200123_0159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='last_edited_on',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
