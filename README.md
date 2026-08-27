# Reviewer API

<<<<<<< HEAD
Una API REST robusta desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión y revisión de películas y géneros, potenciada con inteligencia artificial local y herramientas de moderación, optimizada y desplegada en producción.
=======
Una API REST robusta desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión y revisión de películas y géneros, optimizada con herramientas de moderación y desplegada en producción.
>>>>>>> 748738d (Actualizacion del README)

---

## Características del Proyecto
* **Gestión de Películas y Géneros:** Endpoints completos (CRUD) para administrar películas y clasificarlas por categorías. Lectura pública y escritura restringida a administradores (`is_staff`).
* **Sistema de Reseñas (Reviews):** Permite a los usuarios registrados crear, actualizar y eliminar sus propias reseñas vinculadas a las películas.
<<<<<<< HEAD
* **Reseñas Asistidas por IA (Ollama):** Endpoint personalizado en películas que procesa y resume las reseñas de los usuarios mediante un modelo local (`llama3` a través de Ollama).
=======
>>>>>>> 748738d (Actualizacion del README)
* **Sistema de Moderación y Reportes:** Los usuarios autenticados pueden reportar reseñas directamente desde su endpoint específico. Los administradores disponen de herramientas para gestionar reportes, borrar contenido y banear o reactivar cuentas de usuario.
* **Autenticación Segura:** Implementación de **Simple JWT** para autenticar usuarios y proteger los endpoints de la API.
* **Filtrado Avanzado:** Integrado con `django-filters`, búsqueda de texto (`SearchFilter`) y ordenamiento (`OrderingFilter`).
* **Despliegue en Producción:** Configurado con **Gunicorn** y **WhiteNoise** para servir archivos estáticos, y alojado en **Render**.

---

## Tecnologías Utilizadas
* **Python** 
* **Django** 
* **Django REST Framework**
* **Simple JWT** (Autenticación por JSON Web Tokens)
* **Django Filters**
* **OpenAI SDK / Ollama** (Integración de IA local para resúmenes)
* **Gunicorn** (Servidor WSGI para producción)
* **WhiteNoise** (Gestión de archivos estáticos)

---

## Endpoints Principales y Guía de Uso
Puedes interactuar con los siguientes recursos (Base URL en producción: `https://reviewer-api-495d.onrender.com/` o en local `http://127.0.0.1:8000/`):

| Endpoint | Método | Permisos | Descripción |
| :--- | :--- | :--- | :--- |
| `/api/` | `GET` | Público (`AllowAny`) | Raíz personalizada de la API con enlaces directos a todos los recursos. |
| `/api/auth/register/` | `POST` | Público (`AllowAny`) | Registro de nuevos usuarios en el sistema. |
| `/api/auth/token/` | `POST` | Público (`AllowAny`) | Obtención de tokens JWT (Access / Refresh) para autenticación. |
| `/api/genres/` | `GET` / `POST` | Público / Solo Admin | Listar géneros o crear nuevos (escritura exclusiva para administradores). |
| `/api/movies/` | `GET` / `POST` | Público / Solo Admin | Listar, filtrar, buscar películas o crear una nueva. |
<<<<<<< HEAD
| `/api/movies/{id}/summary/` | `GET` | Público | Genera un resumen automatizado mediante IA (Ollama/Llama3) de todas las reseñas de una película. |
=======
>>>>>>> 748738d (Actualizacion del README)
| `/api/reviews/` | `GET` / `POST` | Público / Autenticado | Listar reseñas o crear una nueva (asociada automáticamente al usuario autenticado). |
| `/api/reviews/{id}/report/` | `POST` | Autenticado | Permite reportar una reseña específica indicando un motivo. |
| `/api/reports/` | `GET` / `POST` | Solo Admin | Gestión y listado completo de los reportes del sistema. |
| `/api/reports/{id}/delete_review/` | `POST` | Solo Admin | Acción de moderación para resolver el reporte, eliminar la reseña y opcionalmente banear al usuario autor. |
| `/api/users-admin/` | `GET` | Solo Admin | Listado de usuarios registrados en el sistema para control administrativo. |
| `/api/users-admin/{username}/unban_user/` | `POST` | Solo Admin | Reactiva (desbanea) una cuenta de usuario desactivada previamente. |

---

## Estructura del Proyecto
```text
ProyectoFinal/
│
├── Reviewer/             # Configuración principal del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── reviews/              # Aplicación principal (Modelos, Vistas, Serializadores)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── requirements.txt      # Dependencias
├── manage.py             # Script de gestión de Django
├── build.sh              # Script de compilación
└── README.md             # Documentación