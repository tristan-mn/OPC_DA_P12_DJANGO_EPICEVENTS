# Generated by Django 4.1.4 on 2023-03-18 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event", name="attendees", field=models.IntegerField(),
        ),
    ]
