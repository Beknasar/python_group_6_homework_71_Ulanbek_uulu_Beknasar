# Generated by Django 2.2 on 2020-09-20 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('webapp', '0010_order_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket', to='sessions.Session'),
        ),
    ]
