# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Status.start'
        db.delete_column(u'workflow_status', 'start')

        # Adding field 'Status.type'
        db.add_column(u'workflow_status', 'type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Status.start'
        db.add_column(u'workflow_status', 'start',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Status.type'
        db.delete_column(u'workflow_status', 'type')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'workflow.status': {
            'Meta': {'object_name': 'Status'},
            'available_states': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'available_states_rel_+'", 'blank': 'True', 'to': u"orm['workflow.Status']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'states'", 'to': u"orm['workflow.Workflow']"})
        },
        u'workflow.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['workflow']