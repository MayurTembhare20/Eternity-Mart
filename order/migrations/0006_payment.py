# Generated by Django 4.2.1 on 2023-06-16 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_razor_pay_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('Payment_status', models.CharField(blank=True, max_length=255, null=True)),
                ('Payment_method', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_order', to='order.order')),
            ],
        ),
    ]
