# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'projects_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'projects', ['Role'])

        # Adding M2M table for field permissions on 'Role'
        m2m_table_name = db.shorten_name(u'projects_role_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('role', models.ForeignKey(orm[u'projects.role'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['role_id', 'permission_id'])

        # Adding model 'RoleMembership'
        db.create_table(u'projects_rolemembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Role'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('join_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'projects', ['RoleMembership'])

        # Deleting field 'Project.people'
        db.delete_column(u'projects_project', 'people_id')


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table(u'projects_role')

        # Removing M2M table for field permissions on 'Role'
        db.delete_table(db.shorten_name(u'projects_role_permissions'))

        # Deleting model 'RoleMembership'
        db.delete_table(u'projects_rolemembership')


        # User chose to not deal with backwards NULL issues for 'Project.people'
        raise RuntimeError("Cannot reverse this migration. 'Project.people' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Project.people'
        db.add_column(u'projects_project', 'people',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)


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
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'my_projects'", 'to': u"orm['auth.User']"})
        },
        u'projects.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Project']"}),
            'superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'projects.rolemembership': {
            'Meta': {'object_name': 'RoleMembership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Role']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['projects']