# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Carousel'
        db.create_table(u'carousel_carousel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('distribution', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal(u'carousel', ['Carousel'])

        # Adding model 'CarouselElement'
        db.create_table(u'carousel_carouselelement', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('carousel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='elements', to=orm['carousel.Carousel'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'carousel', ['CarouselElement'])


    def backwards(self, orm):
        # Deleting model 'Carousel'
        db.delete_table(u'carousel_carousel')

        # Deleting model 'CarouselElement'
        db.delete_table(u'carousel_carouselelement')


    models = {
        u'carousel.carousel': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Carousel'},
            'distribution': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'carousel.carouselelement': {
            'Meta': {'ordering': "('position', 'name')", 'object_name': 'CarouselElement'},
            'carousel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elements'", 'to': u"orm['carousel.Carousel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['carousel']