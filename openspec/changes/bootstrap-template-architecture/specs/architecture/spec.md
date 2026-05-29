# Spec Delta: Bootstrap Template Architecture

## Requirement: Baseline arquitectónico Django template-first
El sistema MUST inicializar una arquitectura Django monolítica con renderizado server-side vía templates, alineada a `requirements.md` y sin frontend desacoplado.

### Scenario: Inicialización de estructura por capas
**Given** un proyecto Django sin módulos de negocio implementados  
**When** se aplica el bootstrap arquitectónico  
**Then** cada módulo funcional SHALL exponer capa View, Service y Repository con responsabilidades separadas.

### Scenario: Base UI reutilizable
**Given** una vista web de cualquier módulo MVP  
**When** se renderiza la página  
**Then** MUST extender un `base.html` compartido con navegación y bloques de contenido.

## Requirement: Preparación para multimedia y seguridad mínima
El sistema MUST preparar carga de imágenes de preguntas y controles base de seguridad/autenticación.

### Scenario: Configuración de media para preguntas
**Given** una pregunta con imagen (texto, imagen o ambas)  
**When** el servidor guarda el archivo  
**Then** SHALL persistirlo en ruta de media local compatible con `media/questions/`.

### Scenario: Protección base de vistas
**Given** una vista restringida a usuario autenticado  
**When** un usuario anónimo intenta acceder  
**Then** MUST ser redirigido al flujo de login de Django.

## MVP Scope
- Arquitectura base, template principal, wiring transversal.

## Out of Scope
- Implementación de reglas de negocio de materias/cuestionarios/preguntas/intentos.
