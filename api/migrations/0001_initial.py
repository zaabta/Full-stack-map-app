# Generated by Django 3.2 on 2024-10-03 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_point', models.TextField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pending_order', models.IntegerField(default=0)),
                ('coordinate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.coordinate')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phone', models.IntegerField()),
                ('status', models.CharField(choices=[('RD', 'Ready'), ('PD', 'Pending'), ('DE', 'Delivered')], default='RD', max_length=2)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField()),
                ('duration', models.CharField(max_length=10)),
                ('coordinate', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.coordinate')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='api.job')),
            ],
        ),
    ]
