# Generated by Django 5.0.4 on 2024-04-28 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estatequery', '0002_alter_realestate_area_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='no_of_bathrooms',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='no_of_bedrooms',
            field=models.PositiveIntegerField(),
        ),
    ]
