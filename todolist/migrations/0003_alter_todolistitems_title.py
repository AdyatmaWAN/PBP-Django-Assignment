# Generated by Django 4.1 on 2022-09-29 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_alter_todolistitems_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolistitems',
            name='title',
            field=models.TextField(),
        ),
    ]