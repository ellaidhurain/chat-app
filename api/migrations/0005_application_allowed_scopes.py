# Generated by Django 4.1.7 on 2023-03-14 07:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_chatroom_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="allowed_scopes",
            field=models.CharField(
                blank=True,
                help_text="Space separated list of allowed scopes for the application.",
                max_length=100,
            ),
        ),
    ]
