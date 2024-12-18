# Generated by Django 5.1.3 on 2024-12-18 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingAlert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_size', models.FloatField()),
                ('order_action', models.CharField(max_length=10)),
                ('order_contracts', models.FloatField()),
                ('order_price', models.FloatField()),
                ('order_id', models.CharField(max_length=100)),
                ('market_position', models.CharField(max_length=10)),
                ('market_position_size', models.FloatField()),
                ('prev_market_position', models.CharField(max_length=10)),
                ('prev_market_position_size', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AlterModelOptions(
            name='tradingviewalert',
            options={'ordering': ['-received_at']},
        ),
        migrations.AddField(
            model_name='tradingviewalert',
            name='processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tradingviewalert',
            name='strategy',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
