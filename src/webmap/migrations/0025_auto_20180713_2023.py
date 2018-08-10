# Generated by Django 2.0.6 on 2018-07-13 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmap', '0024_baselayer_overlay'),
    ]

    operations = [
        migrations.AddField(
            model_name='baselayer',
            name='className',
            field=models.CharField(blank=True, default='', help_text='name of CSS class to apply to layer', max_length=255, null=True, verbose_name='Class name'),
        ),
        migrations.AlterField(
            model_name='baselayer',
            name='overlay',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='webmap.BaseLayer', verbose_name='overlay'),
        ),
    ]