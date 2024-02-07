# Generated by Django 4.2.1 on 2024-02-07 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0010_paymentrequest"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentrequest",
            name="request_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Paid", "Paid"),
                    ("Decline", "Decline"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]
