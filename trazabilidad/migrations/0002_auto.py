# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field marcas on 'Persona'
        m2m_table_name = db.shorten_name(u'trazabilidad_persona_marcas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('persona', models.ForeignKey(orm[u'trazabilidad.persona'], null=False)),
            ('marca', models.ForeignKey(orm[u'trazabilidad.marca'], null=False))
        ))
        db.create_unique(m2m_table_name, ['persona_id', 'marca_id'])


    def backwards(self, orm):
        # Removing M2M table for field marcas on 'Persona'
        db.delete_table(db.shorten_name(u'trazabilidad_persona_marcas'))


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trazabilidad.alza_tipo': {
            'Meta': {'object_name': 'Alza_tipo'},
            'alza_tipo_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'trazabilidad.apiario': {
            'Meta': {'object_name': 'Apiario'},
            'fecha_alta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'latitud': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '3'}),
            'longitud': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '3', 'decimal_places': '3'}),
            'nro_chacra': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'nro_colmena': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']"})
        },
        u'trazabilidad.ciudad': {
            'Meta': {'object_name': 'Ciudad'},
            'added_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'codigo_postal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'primary_key': 'True'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'trazabilidad.direccion': {
            'Meta': {'object_name': 'Direccion'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Ciudad']"}),
            'direccion_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'trazabilidad.documento_tipo': {
            'Meta': {'object_name': 'Documento_tipo'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'documento_tipo_id': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'})
        },
        u'trazabilidad.envase': {
            'Meta': {'unique_together': "(('nro_envase', 'nro_fraccionamiento'),)", 'object_name': 'Envase'},
            'envase_tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Envase_tipo']"}),
            'fecha_vencimiento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'nro_envase': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nro_fraccionamiento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Fraccionamiento']"}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Persona']"})
        },
        u'trazabilidad.envase_tipo': {
            'Meta': {'unique_together': "(('envase_tipo_id', 'marca', 'capacidad'),)", 'object_name': 'Envase_tipo'},
            'capacidad': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'envase_tipo_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'material': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'trazabilidad.extraccion': {
            'Meta': {'object_name': 'Extraccion'},
            'fecha_extraccion': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'lote': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['trazabilidad.Lote']", 'unique': 'True'}),
            'nro_extraccion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Persona']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'trazabilidad.fraccionamiento': {
            'Meta': {'unique_together': "(('nro_fraccionamiento', 'nro_tambor'),)", 'object_name': 'Fraccionamiento'},
            'cantidad_envases': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'envase_tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Envase_tipo']"}),
            'fecha_fraccionamiento': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Marca']"}),
            'nro_fraccionamiento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nro_tambor': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['trazabilidad.Tambor']", 'unique': 'True'}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Persona']"})
        },
        u'trazabilidad.grupo_alza': {
            'Meta': {'unique_together': "(('lote', 'alza_tipo'),)", 'object_name': 'Grupo_alza'},
            'alza_tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Alza_tipo']"}),
            'cantidad_alzas': ('django.db.models.fields.IntegerField', [], {}),
            'condicion': ('django.db.models.fields.CharField', [], {'default': "'LLENA'", 'max_length': '30'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alza'", 'to': u"orm['trazabilidad.Lote']"}),
            'nro_alza': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'trazabilidad.inspeccion': {
            'Meta': {'unique_together': "(('nro_inspeccion', 'apiario'),)", 'object_name': 'Inspeccion'},
            'apiario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Apiario']"}),
            'fecha_inspeccion': ('django.db.models.fields.DateTimeField', [], {}),
            'habilita': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nro_inspeccion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'trazabilidad.lote': {
            'Meta': {'unique_together': "(('nro_lote', 'apiario'),)", 'object_name': 'Lote'},
            'apiario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Apiario']"}),
            'devuelto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha_egreso': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fecha_ingreso': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'nro_lote': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'trazabilidad.marca': {
            'Meta': {'object_name': 'Marca'},
            'habilitada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        u'trazabilidad.persona': {
            'Meta': {'object_name': 'Persona'},
            'cod_unico_identif': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'documento_tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Documento_tipo']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fecha_alta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'marcas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['trazabilidad.Marca']", 'symmetrical': 'False'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nro_documento': ('django.db.models.fields.IntegerField', [], {}),
            'telefono': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'trazabilidad.remito': {
            'Meta': {'object_name': 'Remito'},
            'fecha_remito': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 8, 24, 0, 0)'}),
            'nro_remito': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Persona']"})
        },
        u'trazabilidad.remito_detalle': {
            'Meta': {'unique_together': "(('nro_remito_detalle', 'renglon', 'nro_remito'),)", 'object_name': 'Remito_detalle'},
            'nro_envase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Envase']"}),
            'nro_remito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Remito']"}),
            'nro_remito_detalle': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nro_tambor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Tambor']"}),
            'renglon': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'trazabilidad.socio': {
            'Meta': {'unique_together': "(('nro_renapa', 'persona'),)", 'object_name': 'Socio'},
            'estado': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'nro_renapa': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Persona']"})
        },
        u'trazabilidad.tambor': {
            'Meta': {'unique_together': "(('nro_tambor', 'nro_extraccion'),)", 'object_name': 'Tambor'},
            'nro_extraccion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Extraccion']"}),
            'nro_tambor': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['trazabilidad']