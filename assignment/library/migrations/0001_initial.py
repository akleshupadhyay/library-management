# Generated by Django 3.2.13 on 2022-05-08 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=200)),
                ('author_name', models.CharField(max_length=200)),
                ('rate', models.FloatField()),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('BORROWED', 'BORROWED')], default='AVAILABLE', max_length=10)),
                ('issued_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]