# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Status.workflow'
        db.alter_column(u'workflow_status', 'workflow_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['workflow.Workflow']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Status.workflow'
        raise RuntimeError("Cannot reverse this migration. 'Status.workflow' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Status.workflow'
        db.alter_column(u'workflow_status', 'workflow_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Workflow']))

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
            'available_states': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workflow.Status']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'states'", 'null': 'True', 'to': u"orm['workflow.Workflow']"})
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