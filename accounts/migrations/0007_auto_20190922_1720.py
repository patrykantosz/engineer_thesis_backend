# Generated by Django 2.2.5 on 2019-09-22 15:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20190922_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='food_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.UserFoodHistory'),
        ),
        migrations.AlterField(
            model_name='userfoodhistory',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 9, 22, 15, 20, 41, 157391, tzinfo=utc), null=True),
        ),
    ]
