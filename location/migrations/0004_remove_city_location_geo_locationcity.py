# Generated by Django 4.2.3 on 2023-07-17 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_city'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='location_geo',
        ),
        migrations.CreateModel(
            name='LocationCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.city')),
                ('location_geo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locat_geo', to='location.locationgeo')),
            ],
        ),
    ]