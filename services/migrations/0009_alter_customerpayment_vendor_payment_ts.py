# Generated by Django 4.2.1 on 2024-01-05 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "services",
            "0008_rename_payment_amount_customerpayment_total_paid_amount_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="customerpayment",
            name="vendor_payment_ts",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
