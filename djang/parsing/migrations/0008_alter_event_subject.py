# Generated by Django 4.1.5 on 2023-03-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parsing", "0007_event_end_after_start"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="subject",
            field=models.CharField(max_length=600),
        ),
    ]
