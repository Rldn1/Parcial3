from django.db import migrations

def cargar_preguntas_test_completo(apps, schema_editor):
    PreguntaTestPersonalizado = apps.get_model('miapp', 'PreguntaTestPersonalizado')
    OpcionRespuestaPersonalizado = apps.get_model('miapp', 'OpcionRespuestaPersonalizado')
    
    # Eliminar datos existentes primero
    PreguntaTestPersonalizado.objects.all().delete()
    
    # Crear preguntas del test completo (20 preguntas)
    preguntas = [
        # Sección A: Estado Emocional y Cognitivo
        {
            'numero': 1,
            'texto': '¿Con qué frecuencia ha sentido poco interés o placer en hacer las cosas?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('varios_dias', 'Varios días', 1),
                ('mitad_dias', 'Más de la mitad de los días', 2),
                ('casi_todos', 'Casi todos los días', 3)
            ]
        },
        {
            'numero': 2,
            'texto': '¿Se ha sentido desanimado/a, deprimido/a o sin esperanza?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('varios_dias', 'Varios días', 1),
                ('mitad_dias', 'Más de la mitad de los días', 2),
                ('casi_todos', 'Casi todos los días', 3)
            ]
        },
        {
            'numero': 3,
            'texto': '¿Con qué frecuencia se ha sentido nervioso/a, ansioso/a o con los nervios de punta?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('varios_dias', 'Varios días', 1),
                ('mitad_dias', 'Más de la mitad de los días', 2),
                ('casi_todos', 'Casi todos los días', 3)
            ]
        },
        {
            'numero': 4,
            'texto': '¿Ha tenido dificultad para relajarse o controlar las preocupaciones?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('varios_dias', 'Varios días', 1),
                ('mitad_dias', 'Más de la mitad de los días', 2),
                ('casi_todos', 'Casi todos los días', 3)
            ]
        },
        {
            'numero': 5,
            'texto': '¿Ha notado pensamientos automáticos negativos sobre usted mismo?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('ocasionalmente', 'Ocasionalmente', 1),
                ('frecuentemente', 'Frecuentemente', 2),
                ('casi_siempre', 'Casi siempre', 3)
            ]
        },
        {
            'numero': 6,
            'texto': '¿Siente que sus pensamientos interfieren con su capacidad para concentrarse o tomar decisiones?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('ocasionalmente', 'Ocasionalmente', 1),
                ('frecuentemente', 'Frecuentemente', 2),
                ('casi_siempre', 'Casi siempre', 3)
            ]
        },
        {
            'numero': 7,
            'texto': '¿Ha experimentado sentimientos de desesperanza o inutilidad últimamente?',
            'seccion': 'A',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('ocasionalmente', 'Ocasionalmente', 1),
                ('frecuentemente', 'Frecuentemente', 2),
                ('casi_siempre', 'Casi siempre', 3)
            ]
        },
        # Sección B: Funcionamiento Diario
        {
            'numero': 8,
            'texto': '¿Ha tenido problemas de sueño (dormir demasiado o muy poco)?',
            'seccion': 'B',
            'opciones': [
                ('no', 'No', 0),
                ('levemente', 'Sí, levemente', 1),
                ('moderadamente', 'Sí, moderadamente', 2),
                ('severamente', 'Sí, severamente', 3)
            ]
        },
        {
            'numero': 9,
            'texto': '¿Ha evitado actividades, lugares o personas por miedo a sentir ansiedad o incomodidad?',
            'seccion': 'B',
            'opciones': [
                ('nunca', 'Nunca', 0),
                ('rara_vez', 'Rara vez', 1),
                ('a_veces', 'A veces', 2),
                ('a_menudo', 'A menudo', 3),
                ('siempre', 'Siempre', 4)
            ]
        },
        {
            'numero': 10,
            'texto': '¿Cómo reaccionó la última vez que enfrentó una situación estresante o desafiante?',
            'seccion': 'B',
            'opciones': [
                ('muy_bien', 'Muy bien, con soluciones efectivas', 0),
                ('bien', 'Bien, aunque con algo de dificultad', 1),
                ('regular', 'Regular, con evasión ocasional', 2),
                ('mal', 'Mal, evité o me paralicé', 3),
                ('muy_mal', 'Muy mal, no supe cómo actuar', 4)
            ]
        },
        {
            'numero': 11,
            'texto': '¿Se siente capaz de afrontar los problemas que se le presentan?',
            'seccion': 'B',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        # Sección C: Recursos y Estrategias de Afrontamiento
        {
            'numero': 12,
            'texto': '¿Mantiene contacto con personas que le brindan apoyo emocional?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 13,
            'texto': '¿Expresa sus preocupaciones con personas de su confianza?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 14,
            'texto': '¿Procura tener un buen estado de ánimo la mayor parte del tiempo?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 15,
            'texto': '¿Tiene pensamientos positivos ante los problemas?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 16,
            'texto': '¿Se acepta tal como es?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 17,
            'texto': '¿Mantiene su sentido del humor en situaciones difíciles?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 18,
            'texto': '¿Piensa positivamente sobre el futuro?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 19,
            'texto': '¿Siente que su vida tiene aspectos positivos?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
        {
            'numero': 20,
            'texto': '¿Practica actividades que le ayudan a mantenerse en calma?',
            'seccion': 'C',
            'opciones': [
                ('siempre', 'Siempre', 0),
                ('casi_siempre', 'Casi siempre', 1),
                ('algunas_veces', 'Algunas veces', 2),
                ('casi_nunca', 'Casi nunca', 3),
                ('nunca', 'Nunca', 4)
            ]
        },
    ]

    # Crear preguntas y opciones
    for pregunta_data in preguntas:
        pregunta = PreguntaTestPersonalizado.objects.create(
            numero=pregunta_data['numero'],
            texto=pregunta_data['texto'],
            seccion=pregunta_data['seccion']
        )
        
        for valor, texto, puntaje in pregunta_data['opciones']:
            OpcionRespuestaPersonalizado.objects.create(
                pregunta=pregunta,
                valor=valor,
                texto=texto,
                puntaje=puntaje
            )

def borrar_preguntas_test(apps, schema_editor):
    PreguntaTestPersonalizado = apps.get_model('miapp', 'PreguntaTestPersonalizado')
    PreguntaTestPersonalizado.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('miapp', '0005_recursoskit_descargarecursokit'),  # DEPENDENCIA CORRECTA
    ]

    operations = [
        migrations.RunPython(cargar_preguntas_test_completo, borrar_preguntas_test),
    ]