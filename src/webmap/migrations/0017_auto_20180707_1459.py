# Generated by Django 2.0.6 on 2018-07-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0016_auto_20180707_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappreset',
            name='slug',
            field=models.SlugField(default='', unique=True, verbose_name='name in URL'),
        ),
        migrations.AlterField(
            model_name='marker',
            name='maxzoom',
            field=models.PositiveIntegerField(default=10, help_text='Maximum zoom in which the POIs of this marker will be shown on the map.', verbose_name='Maximum zoom'),
        ),
    ]