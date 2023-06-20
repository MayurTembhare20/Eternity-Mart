# Generated by Django 4.2.1 on 2023-06-07 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_category_show_on_homepage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductImage', to='product.products'),
        ),
    ]