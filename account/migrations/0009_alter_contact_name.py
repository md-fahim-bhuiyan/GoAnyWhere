# Generated by Django 4.1.3 on 2022-12-02 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
