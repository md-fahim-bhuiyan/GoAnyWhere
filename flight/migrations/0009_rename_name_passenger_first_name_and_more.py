# Generated by Django 4.1.3 on 2022-11-13 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0008_alter_flight_id_alter_passenger_id_alter_place_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='passenger',
            old_name='email',
            new_name='last_name',
        ),
    ]