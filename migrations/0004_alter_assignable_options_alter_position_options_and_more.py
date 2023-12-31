# Generated by Django 4.2.4 on 2023-12-18 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_staff', '0003_alter_position_options_remove_assignableto_position_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assignable',
            options={'ordering': ['type', 'name'], 'verbose_name': 'assignable item'},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'ordering': ['level', 'department', 'title']},
        ),
        migrations.AlterField(
            model_name='position',
            name='reports_to',
            field=models.ForeignKey(blank=True, help_text='The position that this position reports to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reporter', to='library_staff.position', verbose_name='reports to'),
        ),
    ]
