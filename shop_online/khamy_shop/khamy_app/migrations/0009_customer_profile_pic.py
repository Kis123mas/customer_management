# Generated by Django 4.1.3 on 2022-12-07 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('khamy_app', '0008_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
