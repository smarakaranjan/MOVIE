# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='image_url',
            field=models.URLField(blank=True, help_text="URL to the person's profile image", max_length=500),
        ),
        migrations.AddField(
            model_name='movie',
            name='image_url',
            field=models.URLField(blank=True, help_text='URL to the movie poster/image', max_length=500),
        ),
    ]

