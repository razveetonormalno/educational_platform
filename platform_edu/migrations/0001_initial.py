# Generated by Django 4.2.1 on 2023-05-30 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('mail', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teachers_list', models.JSONField()),
                ('subject_list', models.JSONField()),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EducationalInstitution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teachers_list', models.JSONField()),
                ('admins_list', models.JSONField()),
                ('groups_list', models.JSONField()),
                ('courses_list', models.JSONField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('director', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courses_list', models.JSONField()),
                ('student_list', models.JSONField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('discipline', models.CharField(verbose_name=200)),
                ('description', models.TextField()),
                ('task', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_homework', models.JSONField()),
                ('mark', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks_list', models.JSONField()),
                ('login', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('mail', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('content', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('patronymic', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=11)),
                ('mail', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platform_edu.group')),
                ('id_homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platform_edu.homework')),
            ],
        ),
        migrations.CreateModel(
            name='GroupCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platform_edu.course')),
                ('id_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='platform_edu.group')),
            ],
        ),
    ]