# Generated by Django 2.0.1 on 2018-01-16 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20170805_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='reporter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collection_items', to='user.Profile'),
        ),
    ]
