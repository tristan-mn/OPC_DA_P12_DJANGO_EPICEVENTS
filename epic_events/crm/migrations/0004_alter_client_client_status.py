# Generated by Django 4.1.4 on 2023-03-19 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_alter_event_event_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="client_status",
            field=models.CharField(
                choices=[
                    ("Existing client", "Existing Client"),
                    ("Potential client", "Potential Client"),
                ],
                max_length=64,
                verbose_name="client_status",
            ),
        ),
    ]