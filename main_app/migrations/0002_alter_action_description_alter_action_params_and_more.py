# Generated by Django 4.0.2 on 2022-03-16 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='params',
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='parentId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.action'),
        ),
    ]
