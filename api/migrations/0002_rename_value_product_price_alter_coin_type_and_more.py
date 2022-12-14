# Generated by Django 4.1.1 on 2022-09-15 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='value',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='coin',
            name='type',
            field=models.CharField(max_length=50, unique=True, verbose_name='coin type'),
        ),
        migrations.AlterField(
            model_name='coin',
            name='value',
            field=models.IntegerField(unique=True, verbose_name='coin value'),
        ),
    ]
