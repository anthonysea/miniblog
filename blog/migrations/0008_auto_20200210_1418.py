# Generated by Django 3.0.2 on 2020-02-10 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20200124_0051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['posted_on']},
        ),
    ]
