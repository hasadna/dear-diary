# Generated by Django 4.1.5 on 2023-03-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parsing", "0010_alter_event_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="calendar",
            name="package_id",
            field=models.UUIDField(null=True),
        ),
    ]
