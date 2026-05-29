# Design: Attempt History and Results

## Decisiones
1. Consultas de historial en `AttemptRepository` con filtro obligatorio por `user_id` para usuarios comunes.
2. Servicio separa “self history” de “admin review” para no mezclar políticas.
3. Templates muestran feedback por pregunta sin modificar resultados históricos.

## Modelos afectados
- Reutiliza `QuizAttempt`, `AttemptAnswer`, `AttemptAnswerOption`.

## Secuencia: ver detalle de intento propio
```mermaid
sequenceDiagram
  participant U as Usuario
  participant V as AttemptDetailView
  participant S as AttemptQueryService
  participant R as AttemptRepository
  U->>V: GET /attempts/{id}/
  V->>S: get_user_attempt_detail(user,id)
  S->>R: fetch_attempt_detail(user_id,id)
  R-->>S: intento + respuestas
  S-->>V: DTO de resultado
  V-->>U: HTML detalle
```

## Dependencias
- `implement-quiz-taking-flow`.

## MVP vs fuera de alcance
- MVP: historial/resultado consultable.
- Fuera: tendencias, comparativas y ranking.
