# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ticket'
        db.create_table(u'issues_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('priority', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='my_tickets', to=orm['auth.User'])),
            ('assigned_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tickets', null=True, to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'issues', ['Ticket'])

        # Adding model 'TicketChange'
        db.create_table(u'issues_ticketchange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issues.Ticket'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'issues', ['TicketChange'])

        # Adding model 'TicketDisplayChange'
        db.create_table(u'issues_ticketdisplaychange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('change', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['issues.TicketChange'])),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('old_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('new_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'issues', ['TicketDisplayChange'])


    def backwards(self, orm):
        # Deleting model 'Ticket'
        db.delete_table(u'issues_ticket')

        # Deleting model 'TicketChange'
        db.delete_table(u'issues_ticketchange')

        # Deleting model 'TicketDisplayChange'
        db.delete_table(u'issues_ticketdisplaychange')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'issues.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'assigned_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tickets'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'priority': ('django.db.models.fields.IntegerField', [], {}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_tickets'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'issues.ticketchange': {
            'Meta': {'object_name': 'TicketChange'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.Ticket']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'issues.ticketdisplaychange': {
            'Meta': {'object_name': 'TicketDisplayChange'},
            'change': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['issues.TicketChange']"}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'old_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['issues']