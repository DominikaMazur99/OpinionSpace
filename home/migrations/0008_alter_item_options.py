# Generated by Django 4.0.3 on 2022-03-25 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_item_image_item_updated_on'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-posted_date']},
        ),
    ]