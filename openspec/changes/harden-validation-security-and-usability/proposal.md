# Proposal: Harden Validation, Security and Usability

## Intent
Endurecer el MVP antes de cierre: reforzar validaciones, controles de seguridad y calidad de UX para cumplir requerimientos no funcionales de usabilidad y seguridad.

## Scope
### In Scope
- Revisión y cobertura de validaciones de negocio críticas.
- Refuerzo de controles de acceso, subida de imágenes y protección de formularios.
- Mejoras de usabilidad (mensajes, navegación, feedback de errores).

### Out of Scope
- Funcionalidades nuevas de negocio fuera del MVP.
- Escalado horizontal/observabilidad avanzada.

## Approach
Auditar flujos existentes por capa, cerrar huecos de validación/autorización, y estandarizar UX de formularios/errores en templates.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `*/services` | Modified | validaciones y reglas endurecidas |
| `*/views` | Modified | guardrails de acceso y manejo de errores |
| `templates/` | Modified | feedback UX consistente |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Regresión funcional por endurecimiento | Med | pruebas de regresión por escenario |
| Fricción UX por mensajes técnicos | Med | lenguaje claro y accionable |

## Rollback Plan
Aplicar rollback selectivo de cambios de hardening que introduzcan regresión, priorizando restaurar continuidad operativa.

## Dependencies
- Todas las etapas funcionales previas.
- `requirements.md` secciones 14.1, 14.4, 16.*.

## Success Criteria
- [ ] Validaciones críticas cubiertas sin brechas conocidas.
- [ ] Accesos indebidos bloqueados en vistas admin/privadas.
- [ ] UX de errores y navegación consistente en flujos principales.
