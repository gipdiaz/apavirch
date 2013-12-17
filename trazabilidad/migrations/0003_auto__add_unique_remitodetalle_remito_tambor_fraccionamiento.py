# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'RemitoDetalle', fields ['remito', 'tambor', 'fraccionamiento']
        db.create_unique(u'trazabilidad_remitodetalle', ['remito_id', 'tambor_id', 'fraccionamiento_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'RemitoDetalle', fields ['remito', 'tambor', 'fraccionamiento']
        db.delete_unique(u'trazabilidad_remitodetalle', ['remito_id', 'tambor_id', 'fraccionamiento_id'])


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
        u'trazabilidad.activo': {
            'Meta': {'object_name': 'Activo'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.apiario': {
            'Meta': {'object_name': 'Apiario'},
            'cantidadColmenas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'nroChacra': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']"})
        },
        u'trazabilidad.ciudad': {
            'Meta': {'object_name': 'Ciudad'},
            'codigoPostal': ('django.db.models.fields.IntegerField', [], {'default': '0', 'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'trazabilidad.devuelto': {
            'Meta': {'object_name': 'Devuelto'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idLoteEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Lote']", 'null': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'trazabilidad.extraido': {
            'Meta': {'object_name': 'Extraido'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idLoteEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Lote']", 'null': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'trazabilidad.fraccionamiento': {
            'Meta': {'object_name': 'Fraccionamiento'},
            'cantidadEnvases': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idFraccionamiento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Marca']"}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'tambor': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['trazabilidad.Tambor']", 'unique': 'True'}),
            'tipoEnvase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.TipoEnvase']"})
        },
        u'trazabilidad.grupoalza': {
            'Meta': {'unique_together': "(('lote', 'tipoAlza'),)", 'object_name': 'GrupoAlza'},
            'cantidadAlzas': ('django.db.models.fields.IntegerField', [], {}),
            'idGrupoAlza': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'alza'", 'to': u"orm['trazabilidad.Lote']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tipoAlza': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.TipoAlza']"})
        },
        u'trazabilidad.inactivo': {
            'Meta': {'object_name': 'Inactivo'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.ingresado': {
            'Meta': {'object_name': 'Ingresado'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idLoteEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Lote']", 'null': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'trazabilidad.inspeccion': {
            'Meta': {'object_name': 'Inspeccion'},
            'apiario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Apiario']"}),
            'cumpleProtocolo': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fechaInspeccion': ('django.db.models.fields.DateTimeField', [], {}),
            'idInspeccion': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'tipoMarca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.TipoMarca']"})
        },
        u'trazabilidad.lote': {
            'Meta': {'object_name': 'Lote'},
            'apiario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Apiario']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'idLote': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'peso': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'})
        },
        u'trazabilidad.marca': {
            'Meta': {'unique_together': "(('descripcion', 'tipoMarca'),)", 'object_name': 'Marca'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'idMarca': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipoMarca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.TipoMarca']"})
        },
        u'trazabilidad.prueba': {
            'Meta': {'object_name': 'Prueba'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodoAPrueba': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.remito': {
            'Meta': {'object_name': 'Remito'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'idRemito': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']"})
        },
        u'trazabilidad.remitodetalle': {
            'Meta': {'unique_together': "(('remito', 'tambor', 'fraccionamiento'),)", 'object_name': 'RemitoDetalle'},
            'fraccionamiento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Fraccionamiento']", 'null': 'True', 'blank': 'True'}),
            'idRemitoDetalle': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Remito']"}),
            'tambor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Tambor']", 'null': 'True', 'blank': 'True'})
        },
        u'trazabilidad.socio': {
            'Meta': {'object_name': 'Socio'},
            'codigoUnicoIdentif': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'marcas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['trazabilidad.Marca']", 'through': u"orm['trazabilidad.SocioMarca']", 'symmetrical': 'False'}),
            'nombreYApellido': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nroDocumento': ('django.db.models.fields.IntegerField', [], {}),
            'nroRenapa': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'telefono': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tipoDocumento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.TipoDocumento']"})
        },
        u'trazabilidad.sociomarca': {
            'Meta': {'unique_together': "(('socio', 'marca'),)", 'object_name': 'SocioMarca'},
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 11, 0, 0)'}),
            'fechaValidez': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'idSocioMarca': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marca': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Marca']"}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']"})
        },
        u'trazabilidad.tambor': {
            'Meta': {'object_name': 'Tambor'},
            'fraccionado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'idTambor': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loteExtraido': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Extraido']"}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        u'trazabilidad.tipoalza': {
            'Meta': {'object_name': 'TipoAlza'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'idTipoAlza': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'trazabilidad.tipodocumento': {
            'Meta': {'object_name': 'TipoDocumento'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'idTipoDocumento': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'trazabilidad.tipoenvase': {
            'Meta': {'unique_together': "(('fabricante', 'peso'),)", 'object_name': 'TipoEnvase'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'fabricante': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'idTipoEnvase': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'peso': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'trazabilidad.tipomarca': {
            'Meta': {'object_name': 'TipoMarca'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'idTipoMarca': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['trazabilidad']