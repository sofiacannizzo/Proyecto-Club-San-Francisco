# Generated by Django 4.0.5 on 2022-07-18 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FinalCoderApp', '0003_remove_order_customer_remove_order_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='FinalCoder\\media\\avatar'),
        ),
    ]
