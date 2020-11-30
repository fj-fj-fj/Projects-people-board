# Generated by Django 3.1.3 on 2020-11-29 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boss',
            options={'verbose_name': 'Руководитель', 'verbose_name_plural': 'Руководители'},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='employee',
            name='level',
            field=models.CharField(choices=[('T', 'Thainee'), ('J', 'Jinior'), ('M', 'Middle'), ('S', 'Senior')], default='T', max_length=1),
        ),
        migrations.AlterField(
            model_name='boss',
            name='project_completed',
            field=models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Успешно завершенные проекты'),
        ),
        migrations.AlterField(
            model_name='boss',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subordinates', to='users.boss', verbose_name='Руководители'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='users.project', verbose_name='Учавствует в проекте'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователяА'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='project',
            name='heads',
            field=models.ManyToManyField(blank=True, related_name='projects', through='users.Employee', to='users.Boss', verbose_name='Руководители проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Название'),
        ),
    ]
