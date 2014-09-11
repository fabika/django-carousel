# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CarouselElement.published'
        db.add_column(u'carousel_carouselelement', 'published',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'CarouselElement.start_date'
        db.add_column(u'carousel_carouselelement', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'CarouselElement.end_date'
        db.add_column(u'carousel_carouselelement', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CarouselElement.published'
        db.delete_column(u'carousel_carouselelement', 'published')

        # Deleting field 'CarouselElement.start_date'
        db.delete_column(u'carousel_carouselelement', 'start_date')

        # Deleting field 'CarouselElement.end_date'
        db.delete_column(u'carousel_carouselelement', 'end_date')


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
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['carousel']