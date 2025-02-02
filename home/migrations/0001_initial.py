# Generated by Django 5.1.3 on 2024-11-24 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(
                    blank=True,
                    null=True)),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='subcategories',
                    to='home.category'
                )),
            ],
        ),
    ]
