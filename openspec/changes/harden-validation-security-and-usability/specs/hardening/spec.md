# Spec Delta: Validation, Security and Usability Hardening

## Requirement: Endurecimiento de validaciones de dominio
El sistema MUST reforzar validaciones de reglas críticas en servicios, evitando dependencia exclusiva de la UI.

### Scenario: Validación de opción correcta inconsistente
**Given** una operación que deja una pregunta single_choice con 0 o >1 correctas  
**When** se intenta persistir  
**Then** MUST rechazarse con error de negocio.

### Scenario: Validación de pregunta vacía
**Given** una operación de alta/edición de pregunta  
**When** no hay texto ni imagen  
**Then** SHALL rechazarse aunque la vista no lo haya prevenido.

## Requirement: Seguridad de acceso y carga de archivos
El sistema MUST bloquear accesos no autorizados y validar archivos multimedia.

### Scenario: Acceso indebido a endpoint admin
**Given** un usuario no staff  
**When** intenta invocar una operación administrativa  
**Then** MUST denegarse acceso.

### Scenario: Upload no imagen
**Given** un administrador sube archivo no imagen como pregunta  
**When** el sistema procesa la carga  
**Then** SHALL rechazar el archivo con mensaje claro.

## Requirement: Usabilidad de flujos MVP
El sistema SHOULD brindar feedback claro y navegación simple en flujos principales.

### Scenario: Error de formulario
**Given** un formulario inválido  
**When** se renderiza respuesta de error  
**Then** SHOULD mostrar mensajes accionables preservando datos ingresados.

## MVP Scope
- Hardening y UX sobre funcionalidades existentes.

## Out of Scope
- Nuevos módulos de negocio o analytics.
