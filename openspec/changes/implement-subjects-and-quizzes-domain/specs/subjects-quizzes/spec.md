# Spec Delta: Subjects and Quizzes Domain

## Requirement: Gestión de materias
El sistema MUST permitir al administrador gestionar materias con nombre obligatorio y descripción opcional.

### Scenario: Crear materia válida
**Given** un administrador autenticado  
**When** envía formulario con `name` no vacío  
**Then** la materia SHALL persistirse y mostrarse en listado.

### Scenario: Rechazo de materia inválida
**Given** un administrador autenticado  
**When** intenta crear materia sin `name`  
**Then** MUST recibir error de validación y no persistir cambios.

## Requirement: Gestión de cuestionarios por materia
El sistema MUST permitir CRUD de cuestionarios asociados a una única materia, con estado activo/inactivo.

### Scenario: Asociar quiz a materia
**Given** una materia existente  
**When** el administrador crea un quiz para esa materia  
**Then** el quiz SHALL quedar vinculado a esa materia exactamente una vez.

### Scenario: Visibilidad pública restringida
**Given** quizzes activos e inactivos  
**When** un usuario común lista quizzes  
**Then** MUST visualizar sólo quizzes activos.

### Scenario: Bloqueo de quiz vacío
**Given** un quiz activo sin preguntas  
**When** un usuario intenta resolverlo  
**Then** el sistema SHOULD impedir inicio y mostrar mensaje informativo.

## MVP Scope
- CRUD de Subject/Quiz + listados públicos de quizzes activos.

## Out of Scope
- Autoría avanzada, ranking, randomización o temporizador.
