# Generated by Django 3.2.8 on 2021-10-11 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryapp', '0004_delivery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='type_of_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='type_of_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]