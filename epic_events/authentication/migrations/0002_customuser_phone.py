# Generated by Django 4.1.4 on 2022-12-26 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="phone",
            field=models.CharField(max_length=100, null=True),
        ),
    ]