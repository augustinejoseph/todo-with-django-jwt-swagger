# Generated by Django 4.2.5 on 2023-09-28 01:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("todo_list_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="todotask",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]