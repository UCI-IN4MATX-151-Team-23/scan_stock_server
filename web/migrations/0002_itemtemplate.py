# Generated by Django 4.1.3 on 2022-11-13 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItemTemplate",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.TextField()),
                ("description", models.TextField()),
                ("attrs", models.TextField()),
            ],
        ),
    ]
