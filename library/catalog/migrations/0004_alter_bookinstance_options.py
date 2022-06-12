# Generated by Django 4.0.5 on 2022-06-12 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'), ('staff_member_required', 'Set user as library employee'))},
        ),
    ]
