# Generated by Django 4.1.4 on 2023-01-22 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_alter_booking_check_in_alter_booking_check_out'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roomtype',
            unique_together={('room_type',)},
        ),
    ]