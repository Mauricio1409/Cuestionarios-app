# Proposal: Implement Web Authentication and User Profile

## Intent
Habilitar registro/login/logout/perfil para usuarios comunes usando autenticación nativa de Django, requisito para asociar intentos y proteger funcionalidades privadas.

## Scope
### In Scope
- Flujos web de registro, inicio y cierre de sesión.
- Perfil básico de usuario autenticado.
- Protección de vistas privadas con controles de acceso.

### Out of Scope
- Permisos avanzados por rol granular.
- Recuperación de contraseña por email en MVP local.

## Approach
Extender `User` según necesidad mínima, utilizar formularios Django auth/custom y encapsular reglas de registro/perfil en servicios.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `accounts/` | New/Modified | views/forms/services/repositories de auth |
| `templates/accounts/` | New | login, signup, profile |
| `core/navigation` | Modified | estado autenticado en menú |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Exposición de vistas privadas | Med | `LoginRequiredMixin` + pruebas |
| UX confusa en errores auth | Med | mensajes de formulario consistentes |

## Rollback Plan
Revertir rutas/accounts templates y volver a auth mínima sin registro custom.

## Dependencies
- `bootstrap-template-architecture`
- `requirements.md` secciones 6.1, 14.4, 15.2.

## Success Criteria
- [ ] Usuario puede registrarse y autenticarse.
- [ ] Usuario puede cerrar sesión y ver perfil.
- [ ] Vistas privadas bloquean acceso anónimo.
