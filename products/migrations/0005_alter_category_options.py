# Generated by Django 5.1.3 on 2024-12-03 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_category_description_subcategory_description_and_more'), ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
