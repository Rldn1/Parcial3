from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator 

class UserProfile(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('pasante', 'Pasante de Psicología'),
        ('paciente', 'Paciente'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='paciente')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"
    
    # Método para verificar fácilmente el tipo de usuario
    def es_admin(self):
        return self.tipo_usuario == 'admin'
    
    def es_pasante(self):
        return self.tipo_usuario == 'pasante'
    
    def es_paciente(self):
        return self.tipo_usuario == 'paciente'

# Señales para crear el profile automáticamente
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()

# Categorías para los recursos
class CategoriaRecurso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6C63FF')
    
    def __str__(self):
        return self.nombre

class Recurso(models.Model):
    TIPO_RECURSO_CHOICES = [
        ('video', 'Video'),
        ('articulo', 'Artículo'),
        ('texto_imagen', 'Texto con Imágenes'),
        ('ejercicio', 'Ejercicio Práctico'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()  # CAMBIADO A descripcion
    tipo_recurso = models.CharField(max_length=15, choices=TIPO_RECURSO_CHOICES)
    categoria = models.ForeignKey(CategoriaRecurso, on_delete=models.CASCADE)
    enlace = models.URLField(blank=True, null=True)
    imagen_portada = models.ImageField(upload_to='portadas/', blank=True, null=True)
    archivo = models.FileField(upload_to='recursos/', blank=True, null=True)
    contenido = models.TextField(blank=True)
    duracion = models.IntegerField(
        default=0,
        verbose_name="Duración (minutos)",
        help_text="Duración del recurso en minutos"
    )
    es_embed = models.BooleanField(
        default=False,
        verbose_name="¿Es contenido embed?",
        help_text="Marcar si el contenido se puede incrustar"
    )
    es_publico = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    # Método para determinar si tiene archivo
    def tiene_archivo(self):
        return bool(self.archivo)
    
    # Método para determinar si tiene enlace
    def tiene_enlace(self):
        return bool(self.enlace)
    
    # Método para obtener tipo de archivo
    def tipo_archivo(self):
        if self.archivo:
            return self.archivo.name.split('.')[-1].lower()
        return None

# Tests psicológicos
class TestPsicologico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    instrucciones = models.TextField()
    es_activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class PreguntaTest(models.Model):
    test = models.ForeignKey(TestPsicologico, on_delete=models.CASCADE, related_name='preguntas')
    texto_pregunta = models.TextField()
    orden = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['orden']
    
    def __str__(self):
        return f"Pregunta {self.orden}: {self.texto_pregunta[:50]}..."

class OpcionRespuesta(models.Model):
    pregunta = models.ForeignKey(PreguntaTest, on_delete=models.CASCADE, related_name='opciones')
    texto_opcion = models.CharField(max_length=200)
    valor = models.IntegerField()
    categoria_recomendacion = models.ForeignKey(CategoriaRecurso, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.texto_opcion

class ResultadoTest(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(TestPsicologico, on_delete=models.CASCADE)
    puntuacion_total = models.IntegerField()
    categoria_recomendada = models.ForeignKey(CategoriaRecurso, on_delete=models.CASCADE)
    completado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Resultado de {self.usuario.username} - {self.test.nombre}"

# Formulario de contacto
class FormularioContacto(models.Model):
    TIPO_CONSULTA_CHOICES = [
        ('sugerencia', 'Sugerencia'),
        ('duda', 'Duda'),
        ('problema', 'Problema Técnico'),
        ('otros', 'Otros'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_consulta = models.CharField(max_length=20, choices=TIPO_CONSULTA_CHOICES)
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    respondido = models.BooleanField(default=False)
    respuesta = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.asunto} - {self.usuario.username}"
    
# ==================== NUEVO MODELO PARA RESPUESTAS DE CONSULTAS ====================
class RespuestaConsulta(models.Model):
    consulta = models.ForeignKey(FormularioContacto, on_delete=models.CASCADE, related_name='respuestas')
    respondido_por = models.ForeignKey(User, on_delete=models.CASCADE)
    respuesta = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Respuesta a {self.consulta.asunto} por {self.respondido_por.username}"
    
# ==================== MODELOS FORO COMUNITARIO ====================
# ==================== MODELOS FORO COMUNITARIO ====================

class CategoriaForo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6C63FF')
    orden = models.IntegerField(default=0)
    es_activa = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoría del Foro'
        verbose_name_plural = 'Categorías del Foro'
    
    def __str__(self):
        return self.nombre

class HiloForo(models.Model):
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
        ('destacado', 'Destacado'),
    ]
    
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(CategoriaForo, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hilos_creados')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='abierto')
    es_anonimo = models.BooleanField(default=False)
    votos_positivos = models.IntegerField(default=0)
    votos_negativos = models.IntegerField(default=0)
    visitas = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-actualizado_en']
        verbose_name = 'Hilo del Foro'
        verbose_name_plural = 'Hilos del Foro'
    
    def __str__(self):
        return self.titulo
    
    def total_respuestas(self):
        return self.respuestas.count()
    
    def ultima_respuesta(self):
        return self.respuestas.order_by('-creado_en').first()

class RespuestaForo(models.Model):
    hilo = models.ForeignKey(HiloForo, on_delete=models.CASCADE, related_name='respuestas')
    contenido = models.TextField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas_foro')
    es_anonimo = models.BooleanField(default=False)
    es_respuesta_oficial = models.BooleanField(default=False)
    votos_positivos = models.IntegerField(default=0)
    votos_negativos = models.IntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['creado_en']
        verbose_name = 'Respuesta del Foro'
        verbose_name_plural = 'Respuestas del Foro'
    
    def __str__(self):
        return f"Respuesta a: {self.hilo.titulo}"

class VotoHilo(models.Model):
    TIPO_VOTO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]
    
    hilo = models.ForeignKey(HiloForo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_voto = models.CharField(max_length=10, choices=TIPO_VOTO_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['hilo', 'usuario']
        verbose_name = 'Voto de Hilo'
        verbose_name_plural = 'Votos de Hilos'

class VotoRespuesta(models.Model):
    TIPO_VOTO_CHOICES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
    ]
    
    respuesta = models.ForeignKey(RespuestaForo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_voto = models.CharField(max_length=10, choices=TIPO_VOTO_CHOICES)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['respuesta', 'usuario']
        verbose_name = 'Voto de Respuesta'
        verbose_name_plural = 'Votos de Respuestas'





#====================================================================
# TEST PSICOLÓGICO PERSONALIZADO
#====================================================================
# Modelos para el Test Psicológico Personalizado
class PreguntaTestPersonalizado(models.Model):
    numero = models.IntegerField()
    texto = models.TextField()
    seccion = models.CharField(max_length=1)  # A, B, C

    def __str__(self):
        return f"{self.numero}. {self.texto[:50]}..."

class OpcionRespuestaPersonalizado(models.Model):
    pregunta = models.ForeignKey(PreguntaTestPersonalizado, on_delete=models.CASCADE)
    valor = models.CharField(max_length=50)
    texto = models.CharField(max_length=200)
    puntaje = models.IntegerField()

    def __str__(self):
        return f"{self.pregunta.numero} - {self.texto}"

class RespuestaTestPersonalizado(models.Model):
    paciente = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(PreguntaTestPersonalizado, on_delete=models.CASCADE)
    opcion_elegida = models.ForeignKey(OpcionRespuestaPersonalizado, on_delete=models.CASCADE)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

class ResultadoTestPersonalizado(models.Model):
    paciente = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    fecha_test = models.DateTimeField(auto_now_add=True)
    puntaje_total = models.IntegerField()
    diagnostico = models.TextField()

    def __str__(self):
        return f"Test de {self.paciente.username} - {self.fecha_test}"


#====================================================================
class ContenidoPersonalizado(models.Model):
    TIPO_CONTENIDO = [
        ('video', 'Video'),
        ('infografia', 'Infografía'),
        ('articulo', 'Artículo'),
        ('ejercicio', 'Ejercicio'),
    ]

    pasante = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    paciente = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='contenido_personalizado')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_contenido = models.CharField(max_length=20, choices=TIPO_CONTENIDO)
    archivo = models.FileField(
        upload_to='contenido_personalizado/%Y/%m/%d/', 
        blank=True, 
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov'])
        ]
    )
    url = models.URLField(blank=True, verbose_name="URL del contenido")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    esta_activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Contenido Personalizado'
        verbose_name_plural = 'Contenidos Personalizados'

    def __str__(self):
        return f"{self.titulo} - Para {self.paciente.username}"

    def get_tipo_icono(self):
        iconos = {
            'video': '🎬',
            'infografia': '📊',
            'articulo': '📄',
            'ejercicio': '💪'
        }
        return iconos.get(self.tipo_contenido, '📎')

    @property
    def tiene_archivo(self):
        return bool(self.archivo)

    @property
    def tiene_url(self):
        return bool(self.url)
    
#====================================================================

# kit de herramienta 
class RecursosKit(models.Model):
    TIPO_ARCHIVO_CHOICES = [
        ('pdf', 'PDF'),
        ('doc', 'Documento Word'),
        ('xls', 'Excel'),
        ('ppt', 'PowerPoint'),
        ('image', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]
    
    CATEGORIA_CHOICES = [
        ('meditacion', 'Meditación'),
        ('ansiedad', 'Manejo de Ansiedad'),
        ('sueno', 'Calidad de Sueño'),
        ('autocompasion', 'Autocompasión'),
        ('comunicacion', 'Comunicación'),
        ('planificacion', 'Planificación'),
        ('ejercicios', 'Ejercicios Prácticos'),
        ('guias', 'Guías Rápidas'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título del recurso")
    descripcion = models.TextField(verbose_name="Descripción")
    archivo = models.FileField(upload_to='recursos_kit/', verbose_name="Archivo")
    tipo_archivo = models.CharField(max_length=10, choices=TIPO_ARCHIVO_CHOICES, verbose_name="Tipo de archivo")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, verbose_name="Categoría")
    tamaño = models.CharField(max_length=20, help_text="Ej: 2.5 MB", verbose_name="Tamaño del archivo")
    icono = models.CharField(max_length=50, default='fas fa-file-pdf', verbose_name="Icono Font Awesome")
    color = models.CharField(max_length=20, default='primary', verbose_name="Color del botón")
    
    
    # Metadata
    descargas = models.PositiveIntegerField(default=0, verbose_name="Número de descargas")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    activo = models.BooleanField(default=True, verbose_name="¿Activo?")
    
    # Para control de acceso
    solo_usuarios_registrados = models.BooleanField(default=True, verbose_name="Solo para usuarios registrados")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden de visualización")
    
    class Meta:
        verbose_name = 'Recurso del Kit'
        verbose_name_plural = 'Recursos del Kit'
        ordering = ['orden', '-fecha_creacion']
        db_table = 'recursos_kit'
    
    def __str__(self):
        return self.titulo
    
    def incrementar_descargas(self):
        self.descargas += 1
        self.save()
    
    def get_icon_class(self):
        """Retorna la clase del icono para Font Awesome"""
        return self.icono
    
    def get_bootstrap_color(self):
        """Retorna la clase de color para Bootstrap"""
        return f"btn-{self.color}"

class DescargaRecursoKit(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    recurso = models.ForeignKey(RecursosKit, on_delete=models.CASCADE, verbose_name="Recurso")
    fecha_descarga = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de descarga")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    
    class Meta:
        verbose_name = 'Descarga de Recurso Kit'
        verbose_name_plural = 'Descargas de Recursos Kit'
        unique_together = ['usuario', 'recurso']
        db_table = 'descargas_recursos_kit'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.recurso.titulo}"
    

#Disponibilidad y Citas Psicológicas
class DisponibilidadPasante(models.Model):
    DIA_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
    ]
    
    pasante = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__tipo_usuario': 'pasante'})
    dia_semana = models.CharField(max_length=10, choices=DIA_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_valida = models.DateField()  # Para qué semana es válida esta disponibilidad
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ['pasante', 'dia_semana', 'hora_inicio', 'fecha_valida']
    
    def __str__(self):
        return f"{self.pasante.username} - {self.get_dia_semana_display()} {self.hora_inicio}"

class DisponibilidadPaciente(models.Model):
    DIA_SEMANA = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
    ]
    
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__tipo_usuario': 'paciente'})
    dia_semana = models.CharField(max_length=10, choices=DIA_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    fecha_valida = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        unique_together = ['paciente', 'dia_semana', 'hora_inicio', 'fecha_valida']
    
    def __str__(self):
        return f"{self.paciente.username} - {self.get_dia_semana_display()} {self.hora_inicio}"

class CitaPsicologica(models.Model):
    ESTADO_CITA = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    MODALIDAD_CITA = [
        ('virtual', 'Virtual'),
        ('presencial', 'Presencial'),
    ]
    
    pasante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas_como_pasante')
    paciente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='citas_como_paciente')
    fecha_cita = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    estado = models.CharField(max_length=15, choices=ESTADO_CITA, default='pendiente')
    modalidad = models.CharField(max_length=10, choices=MODALIDAD_CITA, default='virtual')
    enlace_llamada = models.URLField(
        blank=True, 
        null=True,
        default="https://meet.google.com/new"
    )
    ubicacion_presencial = models.TextField(blank=True, help_text="Dirección para sesión presencial")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Cita {self.paciente.username} con {self.pasante.username} - {self.fecha_cita}"
    
    def generar_enlace_meet(self):
        """Genera un enlace único de Google Meet para la cita virtual"""
        if self.modalidad == 'virtual' and (not self.enlace_llamada or self.enlace_llamada == "https://meet.google.com/new"):
            base_url = "https://meet.google.com"
            codigo_unico = f"sc-{self.pasante.id:03d}-{self.paciente.id:03d}-{self.id:04d}"
            self.enlace_llamada = f"{base_url}/{codigo_unico}"
            self.save()
        return self.enlace_llamada
    
    def puede_unirse(self):
        """Verifica si es hora de unirse a la reunión virtual"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.modalidad != 'virtual':
            return False
            
        ahora = timezone.now()
        fecha_hora_cita = timezone.make_aware(
            datetime.combine(self.fecha_cita, self.hora_inicio)
        )
        
        # Puede unirse 15 minutos antes hasta 1 hora después del inicio
        return (fecha_hora_cita - timedelta(minutes=15)) <= ahora <= (fecha_hora_cita + timedelta(hours=1))
    
    def get_ubicacion_display(self):
        """Retorna la ubicación según la modalidad"""
        if self.modalidad == 'virtual':
            return "Sesión Virtual - Google Meet"
        else:
            return self.ubicacion_presencial or "Sede Principal SoulComfort - San Miguel"