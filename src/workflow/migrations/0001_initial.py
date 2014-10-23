# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Status'
        db.create_table(u'workflow_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('start', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workflow', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workflow.Workflow'])),
        ))
        db.send_create_signal(u'workflow', ['Status'])

        # Adding M2M table for field available_states on 'Status'
        m2m_table_name = db.shorten_name(u'workflow_status_available_states')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_status', models.ForeignKey(orm[u'workflow.status'], null=False)),
            ('to_status', models.ForeignKey(orm[u'workflow.status'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_status_id', 'to_status_id'])

        # Adding model 'Workflow'
        db.create_table(u'workflow_workflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'workflow', ['Workflow'])


    def backwards(self, orm):
        # Deleting model 'Status'
        db.delete_table(u'workflow_status')

        # Removing M2M table for field available_states on 'Status'
        db.delete_table(db.shorten_name(u'workflow_status_available_states'))

        # Deleting model 'Workflow'
        db.delete_table(u'workflow_workflow')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'workflow.status': {
            'Meta': {'object_name': 'Status'},
            'available_states': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'related_name': "'available_states_rel_+'", 'to': u"orm['workflow.Status']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'workflow': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workflow.Workflow']"})
        },
        u'workflow.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['workflow']