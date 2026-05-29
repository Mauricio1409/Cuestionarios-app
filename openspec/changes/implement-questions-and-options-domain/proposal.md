# Proposal: Implement Questions and Options Domain

## Intent
Implementar preguntas y opciones para que los administradores construyan cuestionarios resolubles, incluyendo texto/imagen, tipo single/multiple choice y definición de respuestas correctas.

## Scope
### In Scope
- Modelos `Question` y `QuestionOption` con orden y validaciones.
- CRUD administrativo por templates/forms con capas Service/Repository.
- Validaciones de correctas según tipo de pregunta.

### Out of Scope
- Corrección automática de intentos en runtime.
- Soporte de tipos de pregunta fuera de single/multiple.

## Approach
Separar validaciones de dominio en servicios transaccionales; repositorios manejan consultas de ordenamiento y conteo de opciones correctas.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `quizzes/questions` domain | New/Modified | entidades, servicios y repositorios |
| `templates/questions/`, `templates/options/` | New | formularios CRUD admin |
| `media/questions/` wiring | Modified | carga/validación de imágenes |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Inconsistencia en correctas por tipo | High | Validación estricta previa a guardar |
| Carga de archivo no imagen | Med | Validadores MIME/extensión y tamaño |

## Rollback Plan
Revertir migraciones de preguntas/opciones y remover vistas/templates asociados.

## Dependencies
- `bootstrap-template-architecture`
- `implement-subjects-and-quizzes-domain`
- `requirements.md` secciones 6.4, 6.5, 7.3, 7.4, 16.3, 16.4.

## Success Criteria
- [ ] Admin puede CRUD preguntas y opciones ordenadas.
- [ ] Pregunta nunca queda vacía (sin texto e imagen).
- [ ] Regla de opciones correctas se cumple por tipo.
