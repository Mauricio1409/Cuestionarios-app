# Tasks: Questions and Options Domain

## Fase 1 — Modelo y migraciones
1.1 [x] Crear `Question` y `QuestionOption` con campos y relaciones requeridas.  
1.2 [x] Añadir índices/constraints útiles para `quiz_id`, `question_id`, `position`.

## Fase 2 — Repositorios y servicios
2.1 [x] Implementar repositorios con consultas ordenadas por posición.  
2.2 [x] Implementar servicio de alta/edición con validación texto/imagen.  
2.3 [x] Implementar validación de correctas por tipo.

## Fase 3 — UI administrativa
3.1 [x] Formularios para pregunta (incluyendo imagen) y opciones.  
3.2 [x] Vistas/templates CRUD de preguntas y opciones dentro de quiz.  
3.3 [x] Mensajes de error claros para validaciones de negocio.

## Fase 4 — Verificación
4.1 [x] Probar casos válidos/inválidos de pregunta vacía.  
4.2 [x] Probar reglas single_choice/multiple_choice.  
4.3 [x] Probar ordenamiento por `position` en render.
