# Proposal: Implement Subjects and Quizzes Domain

## Intent
Implementar el dominio de materias y cuestionarios para cubrir CRUD administrativo y listado público de cuestionarios activos, base del flujo de resolución definido en `requirements.md`.

## Scope
### In Scope
- Modelos `Subject` y `Quiz` con reglas de negocio clave.
- CRUD vía templates/forms con capas View/Service/Repository.
- Listado para usuario común: materias y quizzes activos.

### Out of Scope
- Preguntas/opciones y corrección de intentos.
- Permisos avanzados más allá de admin vs usuario autenticado.

## Approach
Construir casos de uso por servicio (crear/editar/eliminar/listar), repositorios con consultas explícitas y vistas basadas en CBV/FBV simples con formularios Django.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `subjects/` | New/Modified | dominio Subject + UI CRUD |
| `quizzes/` | New/Modified | dominio Quiz + activación/desactivación |
| `templates/subjects/`, `templates/quizzes/` | New | pantallas CRUD/listados |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Mezcla de reglas en View | Med | Reforzar validaciones en Service |
| Quizzes inactivos visibles por error | Med | Query repository separada para público |

## Rollback Plan
Revertir migraciones y rutas del dominio; restaurar navegación sin módulos de materias/cuestionarios.

## Dependencies
- `bootstrap-template-architecture`.
- `requirements.md` secciones 6.2, 6.3, 7.1, 7.2, 16.1, 16.2.

## Success Criteria
- [ ] Admin puede CRUD Subject y Quiz.
- [ ] Usuario común sólo ve quizzes activos.
- [ ] Quiz sin preguntas no queda disponible para resolver.
