# Risks / Gaps no bloqueantes

- **Static files warning en tests**: al correr `python manage.py test` aparece warning por ausencia de `/staticfiles/`. No rompe tests ni flujo MVP, pero conviene crear/ajustar configuración de estáticos para evitar ruido en CI.
