# Proposal: Bootstrap Template Architecture

## Intent
Definir la base técnica del MVP en Django monolítico con templates server-rendered, formularios, y patrón por capas (View → Service → Repository), para evitar deuda al implementar los 7 cambios funcionales siguientes.

## Scope
### In Scope
- Estructura de apps (`core`, `accounts`, `subjects`, `quizzes`, `attempts`) y layout base de templates.
- Convenciones de capas, naming, routing y formularios.
- Configuración inicial de media para imágenes de preguntas y base de seguridad web.

### Out of Scope
- CRUD funcional completo de dominios.
- Lógica de corrección de intentos y reportes.

## Approach
Crear baseline técnico reusable: base template, partials, estilos iniciales, mixins/helpers de vistas y contratos de servicios/repositorios. Mantener UI 100% Django templates, sin SPA ni API-first.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `config/settings*.py` | Modified | settings base para templates/media/auth/security |
| `core/` | New/Modified | layout, navegación, utilidades transversales |
| `templates/` | New | base, partials y páginas base |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Convenciones ambiguas de capas | Med | Documentar contratos por capa en design |
| UI base insuficiente para usabilidad | Med | Definir design tokens y componentes mínimos |

## Rollback Plan
Revertir configuración y estructura a estado previo eliminando apps/paths nuevos y restaurando settings/templates desde git.

## Dependencies
- `requirements.md` (secciones 12, 13, 14).

## Success Criteria
- [ ] Convenciones View/Service/Repository definidas y trazables.
- [ ] Base template + navegación lista para módulos MVP.
- [ ] Config media y seguridad mínima alineadas a requerimientos.
