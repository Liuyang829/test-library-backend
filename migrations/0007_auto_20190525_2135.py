# Generated by Django 2.1.7 on 2019-05-25 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_library', '0006_auto_20190525_1916'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
        migrations.RemoveField(
            model_name='question',
            name='formula',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option1',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option2',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option3',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option4',
        ),
        migrations.RemoveField(
            model_name='question',
            name='photo',
        ),
    ]
