# Design: Subjects and Quizzes Domain

## Decisiones
1. `Subject` y `Quiz` como aggregate roots separados, unidos por FK `Quiz.subject`.
2. Reglas de activación en Service para evitar publicar quizzes inválidos.
3. Repository con métodos diferenciados: administración total vs catálogo público activo.

## Modelos afectados
- `Subject(id, name, description, created_at, updated_at)`
- `Quiz(id, subject_id, name, description, is_active, created_at, updated_at)`

## Secuencia: listado público de quizzes activos
```mermaid
sequenceDiagram
  participant U as Usuario común
  participant V as QuizCatalogView
  participant S as QuizCatalogService
  participant R as QuizRepository
  U->>V: GET /quizzes/
  V->>S: list_active(subject?)
  S->>R: fetch_active_by_subject(...)
  R-->>S: quizzes activos
  S-->>V: DTO catálogo
  V-->>U: HTML listado
```

## Dependencias
- Depende de `bootstrap-template-architecture`.

## MVP vs fuera de alcance
- MVP: CRUD y activación básica.
- Fuera de alcance: estadísticas, filtros complejos, permisos granulares.
