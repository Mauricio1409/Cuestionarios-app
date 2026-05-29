# Documento de Requerimientos - Aplicación Preguntero

## 1. Nombre del proyecto

**Preguntero por Materias**

## 2. Descripción general

La aplicación será un sistema web desarrollado en **Django** para administrar y resolver cuestionarios por materia.

El objetivo principal es permitir la creación de materias, cuestionarios, preguntas y opciones de respuesta, incluyendo preguntas con texto, imagen o ambas. Además, el sistema permitirá que distintos usuarios puedan registrarse, iniciar sesión, resolver cuestionarios y consultar sus resultados.

La aplicación inicialmente estará pensada para funcionar en entorno local, aunque su estructura debe permitir una futura evolución a una aplicación online.

---

# 3. Objetivo del sistema

El sistema tiene como objetivo permitir:

* Administrar materias.
* Crear cuestionarios asociados a materias.
* Crear preguntas para cada cuestionario.
* Agregar opciones de respuesta a cada pregunta.
* Permitir preguntas de opción única y opción múltiple.
* Permitir preguntas con texto, imagen o texto e imagen.
* Marcar una o varias opciones como correctas.
* Permitir que los usuarios resuelvan cuestionarios.
* Corregir automáticamente las respuestas.
* Guardar el historial de intentos de cada usuario.
* Mostrar resultados obtenidos por cada usuario.

---

# 4. Alcance del sistema

## 4.1 Incluido en la primera versión

La primera versión del sistema incluirá:

* Gestión de usuarios.
* Login y logout.
* CRUD de materias.
* CRUD de cuestionarios.
* CRUD de preguntas.
* CRUD de opciones de respuesta.
* Carga de imágenes en preguntas.
* Resolución de cuestionarios.
* Corrección automática.
* Registro de intentos.
* Visualización de resultados.

## 4.2 Fuera del alcance inicial

Quedan fuera de la primera versión:

* Ranking entre usuarios.
* Límite de tiempo por cuestionario.
* Preguntas de desarrollo o texto libre.
* Corrección manual.
* Exportación a PDF.
* Importación masiva desde Excel o CSV.
* Sistema de permisos avanzado.
* Publicación online.
* Modo multitenant o varias instituciones.

Estas funcionalidades podrían agregarse en futuras versiones.

---

# 5. Usuarios del sistema

## 5.1 Usuario administrador

El administrador podrá:

* Crear, editar y eliminar materias.
* Crear, editar y eliminar cuestionarios.
* Crear, editar y eliminar preguntas.
* Crear, editar y eliminar opciones.
* Definir respuestas correctas.
* Ver intentos realizados por los usuarios.
* Administrar usuarios desde el panel de Django Admin.

## 5.2 Usuario común

El usuario común podrá:

* Registrarse o iniciar sesión.
* Ver materias disponibles.
* Ver cuestionarios disponibles.
* Resolver cuestionarios.
* Ver el resultado obtenido.
* Consultar su historial de intentos.

---

# 6. Módulos principales

## 6.1 Módulo de usuarios

Este módulo se encargará de la autenticación y administración de usuarios.

Funcionalidades:

* Registro de usuario.
* Inicio de sesión.
* Cierre de sesión.
* Perfil de usuario.
* Asociación de intentos a cada usuario.

Modelo principal:

```text
User
```

En Django se recomienda crear una app llamada:

```text
accounts
```

---

## 6.2 Módulo de materias

Este módulo permite administrar las materias del sistema.

Funcionalidades:

* Crear materia.
* Editar materia.
* Eliminar materia.
* Listar materias.
* Ver detalle de una materia.
* Ver cuestionarios asociados a una materia.

Modelo principal:

```text
Subject
```

Ejemplos de materias:

```text
Redes
Diseño de Sistemas
Base de Datos
Programación
```

App sugerida en Django:

```text
subjects
```

---

## 6.3 Módulo de cuestionarios

Este módulo permite administrar cuestionarios asociados a materias.

Funcionalidades:

* Crear cuestionario.
* Editar cuestionario.
* Eliminar cuestionario.
* Listar cuestionarios.
* Asociar cuestionario a una materia.
* Activar o desactivar cuestionario.
* Ver preguntas de un cuestionario.

Modelo principal:

```text
Quiz
```

Ejemplo:

```text
Materia: Redes
Cuestionario: Subredes y máscaras
```

App sugerida en Django:

```text
quizzes
```

---

## 6.4 Módulo de preguntas

Este módulo permite crear preguntas dentro de un cuestionario.

Funcionalidades:

* Crear pregunta.
* Editar pregunta.
* Eliminar pregunta.
* Asociar pregunta a un cuestionario.
* Definir tipo de pregunta.
* Definir puntaje.
* Agregar explicación.
* Agregar imagen opcional.
* Ordenar preguntas dentro del cuestionario.

Modelo principal:

```text
Question
```

Tipos de pregunta iniciales:

```text
single_choice
multiple_choice
```

Donde:

```text
single_choice    = opción única
multiple_choice  = opción múltiple
```

La pregunta debe aceptar:

```text
Texto solamente
Imagen solamente
Texto + imagen
```

Ejemplo:

```text
Pregunta:
Observá la imagen y respondé: ¿qué tipo de diagrama UML es?

Imagen:
uploads/questions/diagrama-clases.png
```

---

## 6.5 Módulo de opciones de respuesta

Este módulo permite administrar las opciones disponibles para cada pregunta.

Funcionalidades:

* Crear opción.
* Editar opción.
* Eliminar opción.
* Asociar opción a una pregunta.
* Marcar si la opción es correcta.
* Ordenar opciones.

Modelo principal:

```text
QuestionOption
```

Ejemplo:

```text
Pregunta:
¿Qué dispositivo divide dominios de broadcast?

Opciones:
A) Switch
B) Router
C) Hub
D) Bridge

Respuesta correcta:
B) Router
```

---

## 6.6 Módulo de intentos

Este módulo registra cada vez que un usuario resuelve un cuestionario.

Funcionalidades:

* Crear intento al iniciar un cuestionario.
* Guardar usuario que realizó el intento.
* Guardar cuestionario respondido.
* Guardar fecha y hora de inicio.
* Guardar fecha y hora de finalización.
* Guardar puntaje obtenido.
* Guardar puntaje total.
* Consultar historial de intentos.

Modelo principal:

```text
QuizAttempt
```

App sugerida en Django:

```text
attempts
```

---

## 6.7 Módulo de respuestas

Este módulo guarda las respuestas dadas por el usuario en cada intento.

Funcionalidades:

* Guardar respuesta por pregunta.
* Guardar si la respuesta fue correcta o incorrecta.
* Guardar puntaje obtenido en cada pregunta.
* Guardar opciones seleccionadas por el usuario.

Modelos principales:

```text
AttemptAnswer
AttemptAnswerOption
```

---

# 7. Reglas de negocio

## 7.1 Reglas sobre materias

* Una materia puede tener muchos cuestionarios.
* Una materia puede existir sin cuestionarios.
* Una materia debe tener nombre obligatorio.
* La descripción de la materia es opcional.

## 7.2 Reglas sobre cuestionarios

* Un cuestionario pertenece a una sola materia.
* Un cuestionario puede tener muchas preguntas.
* Un cuestionario debe tener nombre obligatorio.
* Un cuestionario puede estar activo o inactivo.
* Solo los cuestionarios activos deberían poder ser resueltos por usuarios comunes.
* Un cuestionario puede existir sin preguntas, aunque no debería poder resolverse si está vacío.

## 7.3 Reglas sobre preguntas

* Una pregunta pertenece a un solo cuestionario.
* Una pregunta puede tener texto, imagen o ambas.
* Una pregunta no puede estar completamente vacía.
* Debe tener al menos texto o imagen.
* Una pregunta debe tener un tipo definido.
* Los tipos iniciales serán:

  * opción única
  * opción múltiple
* Cada pregunta puede tener un puntaje.
* Cada pregunta puede tener una explicación opcional.
* Cada pregunta puede tener una posición para definir el orden.

## 7.4 Reglas sobre opciones

* Una opción pertenece a una sola pregunta.
* Una pregunta puede tener varias opciones.
* Una opción debe tener texto obligatorio.
* Una opción puede estar marcada como correcta o incorrecta.
* Una pregunta debe tener al menos una opción correcta.
* Una pregunta de opción única debe tener exactamente una opción correcta.
* Una pregunta de opción múltiple puede tener una o más opciones correctas.

## 7.5 Reglas sobre intentos

* Un intento pertenece a un usuario.
* Un intento pertenece a un cuestionario.
* Un usuario puede tener muchos intentos.
* Un cuestionario puede tener muchos intentos.
* Un intento debe guardar el puntaje obtenido.
* Un intento debe guardar el puntaje total.
* Un intento debe guardar la fecha de inicio.
* Un intento puede guardar la fecha de finalización.

## 7.6 Reglas sobre corrección

Para preguntas de opción única:

```text
La respuesta es correcta si el usuario selecciona exactamente la única opción correcta.
```

Para preguntas de opción múltiple:

```text
La respuesta es correcta si el usuario selecciona todas las opciones correctas y ninguna incorrecta.
```

Ejemplo:

```text
Opciones correctas: A, C

Usuario selecciona A, C:
Correcto

Usuario selecciona A:
Incorrecto

Usuario selecciona A, B, C:
Incorrecto
```

En la primera versión no se utilizará puntaje parcial.

---

# 8. Modelo de datos

## 8.1 Entidades principales

El sistema estará compuesto por las siguientes entidades:

```text
User
Subject
Quiz
Question
QuestionOption
QuizAttempt
AttemptAnswer
AttemptAnswerOption
```

---

## 8.2 Descripción de entidades

## User

Representa a los usuarios del sistema.

Sirve para identificar quién resuelve cada cuestionario.

Campos principales:

```text
id
username
email
password
first_name
last_name
avatar
is_active
is_staff
is_superuser
last_login
date_joined
```

---

## Subject

Representa una materia.

Campos principales:

```text
id
name
description
created_at
updated_at
```

Ejemplo:

```text
Redes
Diseño de Sistemas
Base de Datos
```

---

## Quiz

Representa un cuestionario o preguntero.

Campos principales:

```text
id
subject_id
name
description
is_active
created_at
updated_at
```

Relación:

```text
Una materia tiene muchos cuestionarios.
Un cuestionario pertenece a una materia.
```

---

## Question

Representa una pregunta dentro de un cuestionario.

Campos principales:

```text
id
quiz_id
statement
image_path
question_type
score
explanation
position
created_at
updated_at
```

Relación:

```text
Un cuestionario tiene muchas preguntas.
Una pregunta pertenece a un cuestionario.
```

---

## QuestionOption

Representa una opción de respuesta de una pregunta.

Campos principales:

```text
id
question_id
text
is_correct
position
created_at
updated_at
```

Relación:

```text
Una pregunta tiene muchas opciones.
Una opción pertenece a una pregunta.
```

---

## QuizAttempt

Representa un intento de resolución de un cuestionario.

Campos principales:

```text
id
user_id
quiz_id
started_at
finished_at
score
total_score
created_at
```

Relación:

```text
Un usuario tiene muchos intentos.
Un cuestionario tiene muchos intentos.
Un intento pertenece a un usuario y a un cuestionario.
```

---

## AttemptAnswer

Representa la respuesta dada por un usuario a una pregunta dentro de un intento.

Campos principales:

```text
id
attempt_id
question_id
is_correct
score_obtained
created_at
```

Relación:

```text
Un intento tiene muchas respuestas.
Una respuesta pertenece a una pregunta.
```

---

## AttemptAnswerOption

Representa cada opción seleccionada por el usuario en una respuesta.

Campos principales:

```text
id
attempt_answer_id
question_option_id
created_at
```

Relación:

```text
Una respuesta puede tener muchas opciones seleccionadas.
Una opción puede ser seleccionada en muchas respuestas.
```

Esta tabla permite soportar preguntas de opción múltiple.

---

# 9. Relaciones del sistema

Relaciones principales:

```text
User 1 ──── N QuizAttempt

Subject 1 ──── N Quiz

Quiz 1 ──── N Question

Question 1 ──── N QuestionOption

Quiz 1 ──── N QuizAttempt

QuizAttempt 1 ──── N AttemptAnswer

AttemptAnswer 1 ──── N AttemptAnswerOption

QuestionOption 1 ──── N AttemptAnswerOption
```

---

# 10. DBML del modelo de datos

```dbml
Table users {
  id integer [primary key, increment]
  username varchar(150) [not null, unique]
  email varchar(254) [unique]
  password varchar(128) [not null]
  first_name varchar(150)
  last_name varchar(150)
  avatar varchar(255)
  is_active boolean [default: true]
  is_staff boolean [default: false]
  is_superuser boolean [default: false]
  last_login timestamp
  date_joined timestamp
}

Table subjects {
  id integer [primary key, increment]
  name varchar(150) [not null]
  description text
  created_at timestamp
  updated_at timestamp
}

Table quizzes {
  id integer [primary key, increment]
  subject_id integer [not null]
  name varchar(150) [not null]
  description text
  is_active boolean [default: true]
  created_at timestamp
  updated_at timestamp
}

Table questions {
  id integer [primary key, increment]
  quiz_id integer [not null]

  statement text [note: 'Texto de la pregunta. Puede ser null si la pregunta es solo imagen']
  image_path varchar(255) [note: 'Ruta local o URL de la imagen de la pregunta. Puede ser null si la pregunta es solo texto']

  question_type varchar(50) [not null, note: 'single_choice | multiple_choice']
  score decimal(5,2) [default: 1.00]
  explanation text
  position integer
  created_at timestamp
  updated_at timestamp
}

Table question_options {
  id integer [primary key, increment]
  question_id integer [not null]
  text text [not null]
  is_correct boolean [default: false]
  position integer
  created_at timestamp
  updated_at timestamp
}

Table quiz_attempts {
  id integer [primary key, increment]
  user_id integer [not null]
  quiz_id integer [not null]
  started_at timestamp
  finished_at timestamp
  score decimal(6,2)
  total_score decimal(6,2)
  created_at timestamp
}

Table attempt_answers {
  id integer [primary key, increment]
  attempt_id integer [not null]
  question_id integer [not null]
  is_correct boolean
  score_obtained decimal(5,2) [default: 0.00]
  created_at timestamp
}

Table attempt_answer_options {
  id integer [primary key, increment]
  attempt_answer_id integer [not null]
  question_option_id integer [not null]
  created_at timestamp
}

Ref: quizzes.subject_id > subjects.id

Ref: questions.quiz_id > quizzes.id

Ref: question_options.question_id > questions.id

Ref: quiz_attempts.user_id > users.id

Ref: quiz_attempts.quiz_id > quizzes.id

Ref: attempt_answers.attempt_id > quiz_attempts.id

Ref: attempt_answers.question_id > questions.id

Ref: attempt_answer_options.attempt_answer_id > attempt_answers.id

Ref: attempt_answer_options.question_option_id > question_options.id
```

---

# 12. Estructura recomendada del proyecto Django
Debe ser utilizando la skill de django layers

---

# 13. Requerimientos técnicos

## 13.1 Backend

El backend será desarrollado con:

```text
Python
Django
PostgreSQL
```

## 13.2 Base de datos

Se utilizará PostgreSQL como motor de base de datos.

Librería recomendada para conectar Django con PostgreSQL:

```text
psycopg2-binary
```

## 13.3 Archivos multimedia

Las imágenes de las preguntas se guardarán como archivos en el sistema local.

Ruta sugerida:

```text
media/questions/
```

En la base de datos se guardará la ruta de la imagen.

Ejemplo:

```text
media/questions/diagrama-clases.png
```

---

# 14. Requerimientos no funcionales

## 14.1 Usabilidad

La aplicación debe ser simple y clara.

El usuario debe poder:

* Encontrar materias fácilmente.
* Entrar a un cuestionario sin dificultad.
* Responder preguntas de forma intuitiva.
* Ver su resultado al finalizar.


## 14.3 Escalabilidad

Aunque inicialmente será local, el diseño debe permitir:

* Agregar más usuarios.
* Agregar más tipos de preguntas.
* Agregar estadísticas.
* Publicar la aplicación en un servidor en el futuro.

## 14.4 Seguridad

El sistema debe:

* Usar autenticación de Django.
* Proteger las vistas que requieren usuario logueado.
* Evitar que usuarios comunes modifiquen cuestionarios.
* Guardar contraseñas usando el sistema de hashing de Django.
* Validar archivos subidos como imágenes.

---

# 15. Flujo principal de uso

## 15.1 Flujo de administración

```text
Administrador inicia sesión
↓
Crea una materia
↓
Crea un cuestionario para esa materia
↓
Crea preguntas para el cuestionario
↓
Agrega opciones a cada pregunta
↓
Marca las opciones correctas
↓
Activa el cuestionario
```

## 15.2 Flujo de usuario

```text
Usuario inicia sesión
↓
Selecciona una materia
↓
Selecciona un cuestionario
↓
Responde las preguntas
↓
Finaliza el intento
↓
El sistema corrige automáticamente
↓
El usuario ve el resultado
```

---

# 16. Criterios de aceptación

## 16.1 Materias

* El administrador puede crear una materia.
* El administrador puede editar una materia.
* El administrador puede eliminar una materia.
* El usuario puede listar materias disponibles.

## 16.2 Cuestionarios

* El administrador puede crear cuestionarios asociados a materias.
* El administrador puede editar cuestionarios.
* El administrador puede eliminar cuestionarios.
* El usuario puede ver cuestionarios activos.
* El usuario no debería resolver cuestionarios inactivos.

## 16.3 Preguntas

* El administrador puede crear preguntas.
* Una pregunta puede tener texto.
* Una pregunta puede tener imagen.
* Una pregunta puede tener texto e imagen.
* Una pregunta debe estar asociada a un cuestionario.
* Una pregunta debe tener tipo.

## 16.4 Opciones

* El administrador puede crear opciones para una pregunta.
* El administrador puede marcar opciones correctas.
* Una pregunta de opción única debe tener una única respuesta correcta.
* Una pregunta de opción múltiple puede tener varias respuestas correctas.

## 16.5 Resolución

* El usuario puede iniciar un cuestionario.
* El usuario puede seleccionar una opción en preguntas de opción única.
* El usuario puede seleccionar varias opciones en preguntas de opción múltiple.
* El usuario puede finalizar el cuestionario.
* El sistema debe guardar el intento.

## 16.6 Corrección

* El sistema debe corregir automáticamente las respuestas.
* El sistema debe calcular el puntaje obtenido.
* El sistema debe mostrar el puntaje final.
* El sistema debe indicar qué preguntas fueron correctas o incorrectas.

---

# 17. Futuras mejoras

Posibles mejoras para próximas versiones:

* Temporizador por cuestionario.
* Preguntas verdadero/falso.
* Preguntas de texto libre.
* Corrección parcial en opción múltiple.
* Estadísticas por materia.
* Estadísticas por cuestionario.
* Ranking de usuarios.
* Exportación de resultados.
* Importación masiva de preguntas.
* Modo repaso.
* Modo examen.
* Etiquetas para preguntas.
* Dificultad de preguntas.
* Randomización de preguntas.
* Randomización de opciones.
* Compartir cuestionarios entre usuarios.
* Panel de progreso personal.

---

# 18. Resumen final

La aplicación será un sistema de preguntero desarrollado en Django, orientado a organizar cuestionarios por materias.

El sistema permitirá administrar materias, cuestionarios, preguntas y opciones, incluyendo soporte para imágenes en las preguntas. Además, contará con usuarios, intentos, respuestas y corrección automática.

La arquitectura estará organizada en apps de Django separadas por responsabilidad:

```text
accounts
subjects
quizzes
attempts
core
```

El modelo de datos permitirá que cada usuario resuelva cuestionarios y conserve su historial de resultados.

La primera versión estará pensada para uso local, pero con una estructura preparada para crecer en el futuro.
