# Generated by Django 4.1.1 on 2022-10-19 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("twitter", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="ratings", name="negative", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="ratings", name="neutral", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="ratings", name="positive", field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="ratings", name="rating", field=models.IntegerField(default=0),
        ),
    ]
