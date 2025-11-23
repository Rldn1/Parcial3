from django.contrib import admin
from .models import CategoriaRecurso, Recurso
from .models import RecursosKit


# Register your models here.
admin.site.register(CategoriaRecurso)
admin.site.register(Recurso)

@admin.register(RecursosKit)
class RecursosKitAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'tipo_archivo', 'activo', 'orden']
    list_filter = ['categoria', 'tipo_archivo', 'activo']
    search_fields = ['titulo', 'descripcion']
    list_editable = ['activo', 'orden']