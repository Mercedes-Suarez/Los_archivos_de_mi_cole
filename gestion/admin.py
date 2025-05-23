from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Archivo, Asignatura, Padre, Alumno, Usuario, SolicitudEliminacionBase

@admin.register(Archivo)
class ArchivoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'asignatura', 'trimestre', 'fecha_subida', ]
    list_filter = ['asignatura', 'trimestre']
    search_fields = ['archivo']

@admin.register(Asignatura)
class AsignaturaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_email', 'get_fecha_creacion')

    def get_email(self, obj):
        return obj.usuario.email
    get_email.short_description = 'Email'

    def get_fecha_creacion(self, obj):
        return obj.usuario.fecha_creacion
    get_fecha_creacion.short_description = 'Fecha de creación'

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso')
    list_filter = ('curso',)
    search_fields = ('nombre',)
    ordering = ('curso', 'nombre')

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('email',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Tipo de usuario', {'fields': ('tipo',)}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo'),
        }),
    )
    list_display = ('username', 'email', 'tipo', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)

@admin.register
class SolicitudEliminacionBase(admin.ModelAdmin):
    list_display = ('archivo', 'solicitante', 'fecha_solicitud', 'procesado')
    list_filter = ('procesado', 'fecha_solicitud')
    search_fields = ('archivo__nombre', 'solicitante__username')
    actions = ['marcar_como_procesadas']

    @admin.action(description='Marcar solicitudes seleccionadas como procesadas')
    def marcar_como_procesadas(self, request, queryset):
        queryset.update(procesado=True)



