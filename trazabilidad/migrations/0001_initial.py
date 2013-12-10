# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TipoEnvase'
        db.create_table(u'trazabilidad_tipoenvase', (
            ('idTipoEnvase', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fabricante', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('peso', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'trazabilidad', ['TipoEnvase'])

        # Adding unique constraint on 'TipoEnvase', fields ['fabricante', 'peso']
        db.create_unique(u'trazabilidad_tipoenvase', ['fabricante', 'peso'])

        # Adding model 'TipoDocumento'
        db.create_table(u'trazabilidad_tipodocumento', (
            ('idTipoDocumento', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'trazabilidad', ['TipoDocumento'])

        # Adding model 'TipoAlza'
        db.create_table(u'trazabilidad_tipoalza', (
            ('idTipoAlza', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'trazabilidad', ['TipoAlza'])

        # Adding model 'TipoMarca'
        db.create_table(u'trazabilidad_tipomarca', (
            ('idTipoMarca', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'trazabilidad', ['TipoMarca'])

        # Adding model 'Ciudad'
        db.create_table(u'trazabilidad_ciudad', (
            ('codigoPostal', self.gf('django.db.models.fields.IntegerField')(default=0, primary_key=True)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'trazabilidad', ['Ciudad'])

        # Adding model 'Marca'
        db.create_table(u'trazabilidad_marca', (
            ('idMarca', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tipoMarca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.TipoMarca'])),
        ))
        db.send_create_signal(u'trazabilidad', ['Marca'])

        # Adding unique constraint on 'Marca', fields ['descripcion', 'tipoMarca']
        db.create_unique(u'trazabilidad_marca', ['descripcion', 'tipoMarca_id'])

        # Adding model 'Socio'
        db.create_table(u'trazabilidad_socio', (
            ('codigoUnicoIdentif', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('tipoDocumento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.TipoDocumento'])),
            ('nroDocumento', self.gf('django.db.models.fields.IntegerField')()),
            ('nombreYApellido', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('direccion', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('telefono', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('fechaAlta', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('nroRenapa', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'trazabilidad', ['Socio'])

        # Adding model 'Prueba'
        db.create_table(u'trazabilidad_prueba', (
            ('idSocioEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('socio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Socio'], null=True)),
            ('periodoAPrueba', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'trazabilidad', ['Prueba'])

        # Adding model 'Activo'
        db.create_table(u'trazabilidad_activo', (
            ('idSocioEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('socio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Socio'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['Activo'])

        # Adding model 'Inactivo'
        db.create_table(u'trazabilidad_inactivo', (
            ('idSocioEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('socio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Socio'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['Inactivo'])

        # Adding model 'SocioMarca'
        db.create_table(u'trazabilidad_sociomarca', (
            ('idSocioMarca', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('socio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Socio'])),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Marca'])),
            ('fechaAlta', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('fechaValidez', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['SocioMarca'])

        # Adding unique constraint on 'SocioMarca', fields ['socio', 'marca']
        db.create_unique(u'trazabilidad_sociomarca', ['socio_id', 'marca_id'])

        # Adding model 'Apiario'
        db.create_table(u'trazabilidad_apiario', (
            ('nroChacra', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('socio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Socio'])),
            ('cantidadColmenas', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fechaAlta', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'trazabilidad', ['Apiario'])

        # Adding model 'Inspeccion'
        db.create_table(u'trazabilidad_inspeccion', (
            ('idInspeccion', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('apiario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Apiario'])),
            ('tipoMarca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.TipoMarca'])),
            ('fechaInspeccion', self.gf('django.db.models.fields.DateTimeField')()),
            ('cumpleProtocolo', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'trazabilidad', ['Inspeccion'])

        # Adding model 'Lote'
        db.create_table(u'trazabilidad_lote', (
            ('idLote', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('apiario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Apiario'])),
            ('peso', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2, blank=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'trazabilidad', ['Lote'])

        # Adding model 'Ingresado'
        db.create_table(u'trazabilidad_ingresado', (
            ('idLoteEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Lote'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['Ingresado'])

        # Adding model 'Devuelto'
        db.create_table(u'trazabilidad_devuelto', (
            ('idLoteEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Lote'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['Devuelto'])

        # Adding model 'Extraido'
        db.create_table(u'trazabilidad_extraido', (
            ('idLoteEstado', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('peso', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Lote'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['Extraido'])

        # Adding model 'Tambor'
        db.create_table(u'trazabilidad_tambor', (
            ('idTambor', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('loteExtraido', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Extraido'])),
            ('peso', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('fraccionado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'trazabilidad', ['Tambor'])

        # Adding model 'GrupoAlza'
        db.create_table(u'trazabilidad_grupoalza', (
            ('idGrupoAlza', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipoAlza', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.TipoAlza'])),
            ('lote', self.gf('django.db.models.fields.related.ForeignKey')(related_name='alza', to=orm['trazabilidad.Lote'])),
            ('cantidadAlzas', self.gf('django.db.models.fields.IntegerField')()),
            ('peso', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'trazabilidad', ['GrupoAlza'])

        # Adding unique constraint on 'GrupoAlza', fields ['lote', 'tipoAlza']
        db.create_unique(u'trazabilidad_grupoalza', ['lote_id', 'tipoAlza_id'])

        # Adding model 'Fraccionamiento'
        db.create_table(u'trazabilidad_fraccionamiento', (
            ('idFraccionamiento', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tambor', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trazabilidad.Tambor'], unique=True)),
            ('tipoEnvase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.TipoEnvase'])),
            ('marca', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Marca'])),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cantidadEnvases', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
        ))
        db.send_create_signal(u'trazabilidad', ['Fraccionamiento'])

        # Adding model 'Remito'
        db.create_table(u'trazabilidad_remito', (
            ('idRemito', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('operario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 12, 10, 0, 0))),
            ('observacion', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'trazabilidad', ['Remito'])

        # Adding model 'RemitoDetalle'
        db.create_table(u'trazabilidad_remitodetalle', (
            ('idRemitoDetalle', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('remito', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Remito'])),
            ('tambor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Tambor'], null=True)),
            ('fraccionamiento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trazabilidad.Fraccionamiento'], null=True)),
        ))
        db.send_create_signal(u'trazabilidad', ['RemitoDetalle'])


    def backwards(self, orm):
        # Removing unique constraint on 'GrupoAlza', fields ['lote', 'tipoAlza']
        db.delete_unique(u'trazabilidad_grupoalza', ['lote_id', 'tipoAlza_id'])

        # Removing unique constraint on 'SocioMarca', fields ['socio', 'marca']
        db.delete_unique(u'trazabilidad_sociomarca', ['socio_id', 'marca_id'])

        # Removing unique constraint on 'Marca', fields ['descripcion', 'tipoMarca']
        db.delete_unique(u'trazabilidad_marca', ['descripcion', 'tipoMarca_id'])

        # Removing unique constraint on 'TipoEnvase', fields ['fabricante', 'peso']
        db.delete_unique(u'trazabilidad_tipoenvase', ['fabricante', 'peso'])

        # Deleting model 'TipoEnvase'
        db.delete_table(u'trazabilidad_tipoenvase')

        # Deleting model 'TipoDocumento'
        db.delete_table(u'trazabilidad_tipodocumento')

        # Deleting model 'TipoAlza'
        db.delete_table(u'trazabilidad_tipoalza')

        # Deleting model 'TipoMarca'
        db.delete_table(u'trazabilidad_tipomarca')

        # Deleting model 'Ciudad'
        db.delete_table(u'trazabilidad_ciudad')

        # Deleting model 'Marca'
        db.delete_table(u'trazabilidad_marca')

        # Deleting model 'Socio'
        db.delete_table(u'trazabilidad_socio')

        # Deleting model 'Prueba'
        db.delete_table(u'trazabilidad_prueba')

        # Deleting model 'Activo'
        db.delete_table(u'trazabilidad_activo')

        # Deleting model 'Inactivo'
        db.delete_table(u'trazabilidad_inactivo')

        # Deleting model 'SocioMarca'
        db.delete_table(u'trazabilidad_sociomarca')

        # Deleting model 'Apiario'
        db.delete_table(u'trazabilidad_apiario')

        # Deleting model 'Inspeccion'
        db.delete_table(u'trazabilidad_inspeccion')

        # Deleting model 'Lote'
        db.delete_table(u'trazabilidad_lote')

        # Deleting model 'Ingresado'
        db.delete_table(u'trazabilidad_ingresado')

        # Deleting model 'Devuelto'
        db.delete_table(u'trazabilidad_devuelto')

        # Deleting model 'Extraido'
        db.delete_table(u'trazabilidad_extraido')

        # Deleting model 'Tambor'
        db.delete_table(u'trazabilidad_tambor')

        # Deleting model 'GrupoAlza'
        db.delete_table(u'trazabilidad_grupoalza')

        # Deleting model 'Fraccionamiento'
        db.delete_table(u'trazabilidad_fraccionamiento')

        # Deleting model 'Remito'
        db.delete_table(u'trazabilidad_remito')

        # Deleting model 'RemitoDetalle'
        db.delete_table(u'trazabilidad_remitodetalle')


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
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.apiario': {
            'Meta': {'object_name': 'Apiario'},
            'cantidadColmenas': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
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
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idLoteEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Lote']", 'null': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'trazabilidad.extraido': {
            'Meta': {'object_name': 'Extraido'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idLoteEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Lote']", 'null': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'peso': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'trazabilidad.fraccionamiento': {
            'Meta': {'object_name': 'Fraccionamiento'},
            'cantidadEnvases': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
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
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.ingresado': {
            'Meta': {'object_name': 'Ingresado'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
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
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idSocioEstado': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'periodoAPrueba': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'socio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Socio']", 'null': 'True'})
        },
        u'trazabilidad.remito': {
            'Meta': {'object_name': 'Remito'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
            'idRemito': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'operario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'trazabilidad.remitodetalle': {
            'Meta': {'object_name': 'RemitoDetalle'},
            'fraccionamiento': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Fraccionamiento']", 'null': 'True'}),
            'idRemitoDetalle': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remito': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Remito']"}),
            'tambor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trazabilidad.Tambor']", 'null': 'True'})
        },
        u'trazabilidad.socio': {
            'Meta': {'object_name': 'Socio'},
            'codigoUnicoIdentif': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'direccion': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
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
            'fechaAlta': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 12, 10, 0, 0)'}),
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