# Generated by Django 4.1 on 2022-09-12 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.category'),
            preserve_default=False,
        ),
    ]