# Proposal: Implement Quiz Taking Flow

## Intent
Implementar el flujo principal de resolución: iniciar intento, responder preguntas, finalizar y corregir automáticamente sin puntaje parcial, tal como exige `requirements.md`.

## Scope
### In Scope
- Inicio de intento asociado a usuario y quiz activo.
- Captura de respuestas single/multiple choice.
- Corrección automática y cálculo de puntaje final.

### Out of Scope
- Temporizador, modo examen, randomización.
- Corrección parcial de respuestas múltiples.

## Approach
Orquestar flujo en `AttemptService`: crear `QuizAttempt`, registrar `AttemptAnswer/AttemptAnswerOption`, evaluar exact match y persistir score/total_score.

## Affected Areas
| Area | Impact | Description |
|------|--------|-------------|
| `attempts/` | New/Modified | entidades y casos de uso de resolución |
| `templates/quizzes/take_*` | New | UI para responder y finalizar |
| `quizzes/services` | Modified | validación de quiz resoluble |

## Risks
| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Errores de corrección multiple_choice | High | tests de matriz de selección |
| Estado inconsistente de intento | Med | transacción al finalizar intento |

## Rollback Plan
Deshabilitar rutas de resolución y revertir migraciones/servicios de attempts.

## Dependencies
- `implement-subjects-and-quizzes-domain`
- `implement-questions-and-options-domain`
- `implement-web-authentication-and-user-profile`
- `requirements.md` secciones 6.6, 6.7, 7.5, 7.6, 15.2, 16.5, 16.6.

## Success Criteria
- [ ] Usuario autenticado puede completar intento de quiz activo.
- [ ] Sistema corrige automáticamente con exactitud single/multiple.
- [ ] Se guarda score y total_score al finalizar.
