# Generated by Django 5.1.1 on 2024-09-17 12:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("problem", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="problem",
            name="status",
            field=models.CharField(
                choices=[
                    ("RIGHT", "맞은 문제"),
                    ("WRONG", "틀린 문제"),
                    ("YET", "아직 안 푼 문제"),
                ],
                default="YET",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="UserProblem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RIGHT", "맞은 문제"),
                            ("WRONG", "틀린 문제"),
                            ("YET", "아직 안 푼 문제"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "problem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="problem.problem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
