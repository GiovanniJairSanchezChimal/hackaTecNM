# Generated by Django 4.2.13 on 2024-06-05 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.TextField(max_length=100)),
                ('question2', models.TextField(max_length=100)),
                ('question3', models.TextField(max_length=100)),
                ('question4', models.TextField(max_length=100)),
                ('question5', models.TextField(max_length=100)),
            ],
        ),
    ]
