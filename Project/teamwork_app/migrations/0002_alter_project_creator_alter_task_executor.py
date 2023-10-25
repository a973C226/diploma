# Generated by Django 4.2.6 on 2023-10-25 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("teamwork_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="creator",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="teamwork_app.employee",
                verbose_name="Создатель проекта",
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="executor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="teamwork_app.employee",
                verbose_name="Исполнитель",
            ),
        ),
    ]
