# Generated by Django 5.1.5 on 2025-02-20 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_product_variations_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
