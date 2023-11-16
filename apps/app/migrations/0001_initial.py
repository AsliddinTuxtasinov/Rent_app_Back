# Generated by Django 4.2.7 on 2023-11-15 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('passport', models.CharField(blank=True, max_length=9, null=True)),
                ('phone', models.CharField(max_length=9)),
                ('desc', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('format', models.CharField(choices=[('metr', 'metr'), ('sm', 'sm'), ('komplekt', 'komplekt'), ('dona', 'dona')], max_length=100)),
                ('price', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.product')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.CharField(blank=True, choices=[("Maxsus to'lov", "Maxsus to'lov"), ("To'liq yopish", "To'liq yopish")], max_length=30, null=True)),
                ('summa', models.FloatField()),
                ('date', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.FloatField()),
                ('price', models.PositiveBigIntegerField(blank=True, null=True)),
                ('date', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producttype')),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveBigIntegerField()),
                ('income_price', models.PositiveBigIntegerField(blank=True, null=True)),
                ('day', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producttype')),
            ],
        ),
    ]
