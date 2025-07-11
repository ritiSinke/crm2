# Generated by Django 5.2.2 on 2025-06-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_published',
        ),
        migrations.AlterField(
            model_name='post',
            name='is_draft',
            field=models.CharField(choices=[('True', 'True'), ('False', 'False')], default='True', max_length=15),
        ),
        migrations.AlterField(
            model_name='postlike',
            name='like_count',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
