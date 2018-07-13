# Generated by Django 2.0.6 on 2018-07-13 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0023_baselayer_opacity'),
    ]

    operations = [
        migrations.AddField(
            model_name='baselayer',
            name='overlay',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webmap.BaseLayer', verbose_name='overlay'),
        ),
    ]