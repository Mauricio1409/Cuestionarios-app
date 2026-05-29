# Proposal: Implement Admin Management UI

## Intent
Consolidar una interfaz administrativa web para operar entidades del MVP (materias, quizzes, preguntas, opciones e intentos) de forma eficiente y segura.

## Scope
### In Scope
- Panel administrativo en templates para CRUD operativo.
- Integración con Django Admin para gestión de usuarios.
- Navegación administrativa consistente y guardrails de permisos.

### Out of Scope
- RBAC avanzado por permisos finos.
- Auditoría avanzada y dashboards complejos.

## Approach
Crear sección administrativa propia en templates (UX de negocio) y mantener Django Admin para administración de usuarios/staff. Services centralizan reglas de autorización.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `templates/admin_ui/` | New | vistas de gestión operativa |
| `core/navigation` | Modified | menú y breadcrumbs admin |
| `accounts/permissions` | Modified | validación staff/admin |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Usuario común accede a gestión | High | middleware/mixins de autorización |
| Duplicación con Django Admin | Med | delimitar uso: negocio vs usuarios |

## Rollback Plan
Deshabilitar rutas de admin UI custom y mantener sólo Django Admin estándar.

## Dependencies
- `implement-subjects-and-quizzes-domain`
- `implement-questions-and-options-domain`
- `implement-attempt-history-and-results`
- `requirements.md` secciones 5.1, 15.1.

## Success Criteria
- [ ] Staff opera CRUD de entidades del MVP desde UI interna.
- [ ] Gestión de usuarios queda en Django Admin.
- [ ] Usuario común no accede a secciones administrativas.
