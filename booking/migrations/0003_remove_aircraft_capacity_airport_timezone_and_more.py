# Generated by Django 5.2.1 on 2025-05-26 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0002_airport_remove_scheduledflight_arrival_time_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="aircraft",
            name="capacity",
        ),
        migrations.AddField(
            model_name="airport",
            name="timezone",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="scheduledflight",
            name="arrival_time",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="airport",
            name="code",
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
