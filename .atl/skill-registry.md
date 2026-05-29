# Skill Registry

Generated: 2026-05-28
Project: sistema-cuestionarios

## Project Conventions Sources
- Runtime instruction source: `/home/mauri/.config/opencode/AGENTS.md` (fuera del repo, aplicado en sesión)
- Project convention files in repo root: none detected (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, `copilot-instructions.md`)

## Available Skills (deduplicated)

| Skill | Source | Trigger (compact) |
|---|---|---|
| django-layered-architecture | ~/.config/opencode/skills | Backend Django/DRF con capas View -> Service -> Repository |
| go-testing | ~/.config/opencode/skills | Cuando se escriben tests en Go/Bubbletea |
| issue-creation | ~/.config/opencode/skills | Crear issue de bug/feature |
| branch-pr | ~/.config/opencode/skills | Crear/abrir pull request |
| judgment-day | ~/.config/opencode/skills | Cuando usuario pide review adversarial/judgment day |
| skill-creator | ~/.config/opencode/skills | Crear una skill nueva |
| find-skills | ~/.agents/skills | Buscar/instalar skills para nuevas capacidades |
| frontend-design | ~/.agents/skills | Diseñar/estilizar UI frontend |
| react-19 | ~/.agents/skills | Escribir componentes React 19 |
| tailwind-4 | ~/.agents/skills | Estilado con Tailwind v4 |
| typescript | ~/.agents/skills | Escribir TypeScript estricto |

## Compact Rules (auto-resolved)

- **Django backend**: aplicar `django-layered-architecture` (View coordina HTTP, Service lógica, Repository acceso a datos).
- **PRs**: aplicar `branch-pr`.
- **Issues**: aplicar `issue-creation`.
- **Go testing**: aplicar `go-testing`.
- **Revisión adversarial**: aplicar `judgment-day`.
- **Creación de skills**: aplicar `skill-creator`.
- **Frontend/UI**: si se toca diseño, usar `frontend-design`; si hay React/TS/Tailwind, combinar `react-19` + `typescript` + `tailwind-4`.
