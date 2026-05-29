# Spec Delta: Web Authentication and User Profile

## Requirement: Autenticación web con Django
El sistema MUST usar autenticación Django para registro/login/logout y hash de contraseñas.

### Scenario: Registro exitoso
**Given** un visitante no autenticado  
**When** completa formulario de registro válido  
**Then** la cuenta SHALL crearse con contraseña hasheada y usuario autenticado.

### Scenario: Login inválido
**Given** un usuario existente  
**When** ingresa credenciales inválidas  
**Then** MUST ver error de autenticación sin iniciar sesión.

## Requirement: Protección de vistas privadas
El sistema MUST proteger vistas que requieren sesión activa.

### Scenario: Acceso anónimo a perfil
**Given** un usuario anónimo  
**When** accede a la vista de perfil  
**Then** SHALL ser redirigido a login.

### Scenario: Acceso autenticado a perfil
**Given** un usuario autenticado  
**When** abre su perfil  
**Then** MUST visualizar sus datos básicos y acciones permitidas.

## MVP Scope
- Registro/login/logout/perfil básico.

## Out of Scope
- MFA, OAuth social, recuperación de contraseña por correo.
