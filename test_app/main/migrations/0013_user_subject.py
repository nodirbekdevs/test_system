# Generated by Django 4.2.3 on 2023-08-13 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_advertising_file_alter_advertising_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subject'),
        ),
    ]
