# Generated by Django 4.2.1 on 2024-01-05 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0006_bookinstantly_booking_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookinstantly",
            name="total_price",
            field=models.IntegerField(default=0),
        ),
    ]
