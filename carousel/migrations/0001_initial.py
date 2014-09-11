# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='name')),
                ('distribution', models.PositiveSmallIntegerField(default=1, verbose_name='distribution', choices=[(1, 'sequential'), (2, 'random'), (3, 'weighted random'), (4, 'cluster random')])),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'carousel',
                'verbose_name_plural': 'carousels',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarouselElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('image', models.ImageField(upload_to=b'carousel_uploads', verbose_name='image')),
                ('url', models.URLField(verbose_name='URL', blank=True)),
                ('position', models.PositiveIntegerField(default=1, help_text="The position of the element in the sequence or the weight of the element in the randomization process (depending on the carousel's distribution).", verbose_name='position')),
                ('published', models.BooleanField(default=1, verbose_name='published')),
                ('start_date', models.DateTimeField(help_text='If this field is filled show starts with a specified date', null=True, verbose_name='start date', blank=True)),
                ('end_date', models.DateTimeField(help_text='If this field is filled show ending with a specified date', null=True, verbose_name='end date', blank=True)),
                ('carousel', models.ForeignKey(related_name=b'elements', verbose_name='carousel', to='carousel.Carousel')),
            ],
            options={
                'ordering': ('position', 'name'),
                'verbose_name': 'carousel element',
                'verbose_name_plural': 'carousel elements',
            },
            bases=(models.Model,),
        ),
    ]
