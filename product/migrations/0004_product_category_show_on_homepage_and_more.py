# Generated by Django 4.2.1 on 2023-05-31 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_category',
            name='show_on_homepage',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='tags',
            field=models.ManyToManyField(blank=True, to='product.product_tag'),
        ),
        migrations.AlterField(
            model_name='products',
            name='variation',
            field=models.ManyToManyField(blank=True, to='product.product_variation'),
        ),
    ]
