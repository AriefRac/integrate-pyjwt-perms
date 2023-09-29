# Generated by Django 4.2.5 on 2023-09-25 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modul',
            options={'ordering': ('-published',), 'permissions': [('can_view_frontend_modul', 'Can view FrontEnd modules'), ('can_view_backend_modul', 'Can view BackEnd modules'), ('can_view_qa_modul', 'Can view QA modules'), ('can_view_ui/ux_modul', 'Can view UI/UX modules')]},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-date',)},
        ),
    ]
