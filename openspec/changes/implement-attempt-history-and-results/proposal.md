# Proposal: Implement Attempt History and Results

## Intent
Permitir al usuario consultar historial de intentos y detalle de resultados, y al administrador revisar intentos, cumpliendo requerimientos de trazabilidad del aprendizaje.

## Scope
### In Scope
- Listado de intentos por usuario autenticado.
- Vista de detalle con respuestas correctas/incorrectas y puntajes.
- Vista administrativa de intentos globales.

### Out of Scope
- Estadísticas avanzadas, ranking y exportación.

## Approach
Agregar queries optimizadas en repositorios para historiales y detalle de intento; render en templates con filtros básicos y paginación simple.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `attempts/` | Modified | servicios y repositorios de consulta |
| `templates/attempts/` | New | historial y detalle de resultados |
| `admin` integration | Modified | acceso de revisión para staff |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Fuga de datos entre usuarios | High | filtrar por owner en service/repository |
| Consultas pesadas en detalle | Med | select_related/prefetch y paginación |

## Rollback Plan
Ocultar rutas de historial/resultados y conservar sólo resolución básica.

## Dependencies
- `implement-quiz-taking-flow`
- `requirements.md` secciones 6.6, 6.7, 16.6.

## Success Criteria
- [ ] Usuario ve su historial y detalle de cada intento.
- [ ] Resultado muestra score final y estado por pregunta.
- [ ] Staff puede consultar intentos en interfaz administrativa.
