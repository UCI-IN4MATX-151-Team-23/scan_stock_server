# Generated by Django 4.1.3 on 2022-11-18 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_item_attrs_alter_tag_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='barcode',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='qrcode',
            field=models.TextField(),
        ),
    ]
