# Generated by Django 5.0.6 on 2024-11-22 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('places', '0004_alter_place_google_place_id_alter_place_latitude_and_more'),
        ('users', '0002_alter_user_options_user_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='facebook',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='favorite_places',
            field=models.ManyToManyField(blank=True, related_name='favorited_by', to='places.place'),
        ),
        migrations.AddField(
            model_name='user',
            name='instagram',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_language',
            field=models.CharField(choices=[('en', 'English'), ('ru', 'Russian'), ('kk', 'Kazakh')], default='en', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='twitter',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
