# Generated by Django 2.0.1 on 2019-08-28 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_auto_20190828_0450'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE UNIQUE INDEX collection_collection_title_text_type_id_uniq ON collection_collection (title, md5(text), type_id)"),
    ]