# Generated by Django 4.2.1 on 2023-11-06 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_useraddress"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicleregistration",
            name="bluebookimg",
            field=models.ImageField(default="1", upload_to="accounts/bluebookimg"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="citizenimg",
            field=models.ImageField(default="1", upload_to="accounts/citizenimg"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="image1",
            field=models.ImageField(default="1", upload_to="accounts/vehicle_images"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="image2",
            field=models.ImageField(default="1", upload_to="accounts/vehicle_images"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="image3",
            field=models.ImageField(default="1", upload_to="accounts/vehicle_images"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="image4",
            field=models.ImageField(default="1", upload_to="accounts/vehicle_images"),
        ),
        migrations.AlterField(
            model_name="vehicleregistration",
            name="image5",
            field=models.ImageField(default="1", upload_to="accounts/vehicle_images"),
        ),
    ]
