# Generated by Django 5.1.3 on 2024-12-29 00:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_remove_order_status_remove_order_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(
                default='Pending',
                max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='order_history',
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]