# Generated by Django 4.1.5 on 2023-02-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parsing", "0005_alter_downloadreport_resource_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="calendar",
            name="when_created_at_source",
            field=models.DateTimeField(null=True),
        ),
    ]