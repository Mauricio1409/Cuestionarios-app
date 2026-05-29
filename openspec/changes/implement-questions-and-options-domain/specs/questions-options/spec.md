# Spec Delta: Questions and Options Domain

## Requirement: Preguntas con texto/imagen y tipo
El sistema MUST permitir preguntas con texto, imagen o ambas, y SHALL rechazar preguntas completamente vacías.

### Scenario: Crear pregunta con sólo imagen
**Given** un administrador autenticado y un quiz existente  
**When** crea una pregunta con `image` y sin `statement`  
**Then** la pregunta MUST persistirse como válida.

### Scenario: Rechazo de pregunta vacía
**Given** un administrador autenticado  
**When** crea pregunta sin `statement` y sin `image`  
**Then** el sistema SHALL mostrar error y no guardar.

## Requirement: Opciones correctas coherentes con tipo
El sistema MUST validar consistencia entre `question_type` y cantidad de opciones correctas.

### Scenario: Pregunta single_choice
**Given** una pregunta `single_choice`  
**When** se guardan opciones  
**Then** MUST existir exactamente una opción correcta.

### Scenario: Pregunta multiple_choice
**Given** una pregunta `multiple_choice`  
**When** se guardan opciones  
**Then** MUST existir una o más opciones correctas.

### Scenario: Orden de opciones y preguntas
**Given** una pregunta con varias opciones  
**When** se consulta para render  
**Then** SHOULD devolverse respetando `position` ascendente.

## MVP Scope
- CRUD admin de Question/QuestionOption y validaciones críticas.

## Out of Scope
- Tipos verdadero/falso y texto libre.
