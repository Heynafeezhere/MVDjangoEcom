# Generated by Django 5.1.3 on 2024-11-30 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_product_image_product_slug_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='demoLink',
            field=models.URLField(blank=True, null=True),
        ),
    ]
