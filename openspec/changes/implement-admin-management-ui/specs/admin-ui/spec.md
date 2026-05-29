# Spec Delta: Admin Management UI

## Requirement: Interfaz administrativa para operaciones del MVP
El sistema MUST ofrecer una UI administrativa para gestionar materias, quizzes, preguntas, opciones e intentos.

### Scenario: Acceso staff permitido
**Given** un usuario staff autenticado  
**When** ingresa a la sección administrativa interna  
**Then** SHALL poder navegar y ejecutar acciones CRUD habilitadas.

### Scenario: Acceso común denegado
**Given** un usuario no staff autenticado  
**When** intenta acceder a la sección administrativa interna  
**Then** MUST recibir denegación de acceso.

## Requirement: Administración de usuarios vía Django Admin
La gestión de cuentas de usuario MUST mantenerse en Django Admin.

### Scenario: Gestión de usuarios
**Given** un superusuario  
**When** necesita crear/editar/desactivar usuarios  
**Then** SHALL realizarlo desde `/admin/` y no desde UI operativa custom.

## MVP Scope
- UI staff para entidades funcionales + users en Django Admin.

## Out of Scope
- Workflows de aprobación, auditoría avanzada y permisos granulares.
