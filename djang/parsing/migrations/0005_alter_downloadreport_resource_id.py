# Generated by Django 4.1.5 on 2023-02-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("parsing", "0004_downloadreport"),
    ]

    operations = [
        migrations.AlterField(
            model_name="downloadreport",
            name="resource_id",
            field=models.UUIDField(db_index=True),
        ),
    ]
