# Spec Delta: Quiz Taking Flow

## Requirement: Inicio y finalización de intento
El sistema MUST crear un `QuizAttempt` al iniciar resolución y SHALL registrar finalización con puntajes.

### Scenario: Iniciar intento válido
**Given** un usuario autenticado y un quiz activo con preguntas  
**When** inicia resolución  
**Then** MUST crearse un intento con `started_at` y asociación usuario/quiz.

### Scenario: Intento bloqueado para quiz no resoluble
**Given** un quiz inactivo o sin preguntas  
**When** un usuario intenta iniciarlo  
**Then** SHALL rechazarse el inicio con mensaje de negocio.

## Requirement: Corrección automática exacta
El sistema MUST corregir sin puntaje parcial.

### Scenario: single_choice correcta
**Given** una pregunta `single_choice` con una opción correcta  
**When** el usuario selecciona exactamente esa opción  
**Then** la respuesta SHALL marcarse correcta y sumar puntaje de la pregunta.

### Scenario: multiple_choice incorrecta por selección incompleta
**Given** una pregunta `multiple_choice` con correctas A y C  
**When** el usuario selecciona sólo A  
**Then** MUST marcarse incorrecta y sumar 0.

### Scenario: multiple_choice incorrecta por opción extra
**Given** una pregunta `multiple_choice` con correctas A y C  
**When** el usuario selecciona A, B y C  
**Then** MUST marcarse incorrecta y sumar 0.

## MVP Scope
- Flujo web completo de toma y corrección automática.

## Out of Scope
- Corrección parcial y temporizador.
