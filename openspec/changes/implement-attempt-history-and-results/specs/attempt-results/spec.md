# Spec Delta: Attempt History and Results

## Requirement: Historial propio de intentos
El sistema MUST permitir a cada usuario autenticado consultar únicamente sus intentos.

### Scenario: Historial personal
**Given** un usuario con múltiples intentos  
**When** abre su historial  
**Then** SHALL visualizar sólo intentos asociados a su cuenta.

### Scenario: Aislamiento entre usuarios
**Given** un usuario autenticado  
**When** intenta acceder al detalle de intento ajeno  
**Then** MUST recibir denegación (404/403 según política).

## Requirement: Detalle de resultado por intento
El sistema MUST mostrar score final y estado por pregunta.

### Scenario: Resultado de intento finalizado
**Given** un intento finalizado  
**When** el usuario abre el detalle  
**Then** SHALL ver `score`, `total_score` y qué preguntas fueron correctas/incorrectas.

### Scenario: Revisión administrativa
**Given** un usuario staff autenticado  
**When** consulta listado de intentos  
**Then** SHOULD poder filtrar por usuario y quiz.

## MVP Scope
- Historial personal y detalle de resultados.

## Out of Scope
- Dashboards analíticos y exportación.
