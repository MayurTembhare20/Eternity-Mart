# Generated by Django 4.2.1 on 2023-06-12 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_image_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_image',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Product_Image', to='product.products'),
        ),
    ]