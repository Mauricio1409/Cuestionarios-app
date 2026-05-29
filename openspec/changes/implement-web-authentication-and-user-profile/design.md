# Design: Web Authentication and User Profile

## Decisiones
1. Reutilizar backend de autenticación Django para minimizar riesgo de seguridad.
2. Encapsular reglas de creación de cuenta/perfil en `AccountService`.
3. Restricción de vistas privadas por mixins/decorators estándar.

## Modelos afectados
- `User` (modelo Django o custom según setup), con perfil básico y asociación futura a intentos.

## Secuencia: login y acceso a perfil
```mermaid
sequenceDiagram
  participant U as Usuario
  participant V as LoginView/ProfileView
  participant S as AccountService
  participant R as UserRepository
  U->>V: POST credenciales
  V->>S: authenticate(credentials)
  S->>R: get_by_username/email
  R-->>S: user
  S-->>V: auth result
  V-->>U: sesión iniciada
  U->>V: GET /accounts/profile/
  V-->>U: HTML perfil
```

## Dependencias
- `bootstrap-template-architecture`.

## MVP vs fuera de alcance
- MVP: autenticación clásica web.
- Fuera: IAM avanzado y proveedores externos.
