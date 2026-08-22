# Reviewer API

Una API REST robusta desarrollada con **Django** y **Django REST Framework (DRF)** para la gestión y revisión de películas y géneros, optimizada y desplegada en producción.

---

## Características del Proyecto

* **Gestión de Películas y Géneros:** Endpoints completos (CRUD) para administrar películas y clasificarlas por categorías.
* **Sistema de Reseñas (Reviews):** Permite a los usuarios crear, leer, actualizar y eliminar reseñas vinculadas a las películas.
* **Autenticación Segura:** Implementación de **Simple JWT** para autenticar usuarios y proteger los endpoints de la API.
* **Filtrado Avanzado:** Integrado con `django-filters` para refinar consultas de manera eficiente.
* **Despliegue en Producción:** Configurado con **Gunicorn** y **WhiteNoise** para servir archivos estáticos, y alojado en **Render**.

---

## Tecnologías Utilizadas

* **Python** (Versión 3.14)
* **Django** (Versión 6.0.6)
* **Django REST Framework**
* **Simple JWT** (Autenticación por JSON Web Tokens)
* **Django Filters**
* **Gunicorn** (Servidor WSGI para producción)
* **WhiteNoise** (Gestión de archivos estáticos)

---

##  Estructura del Proyecto

```text
ProyectoFinal/
│
├── Reviewer/             # Configuración principal del proyecto Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── reviews/              # Aplicación principal de la API (Modelos, Vistas, Serializadores)
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── requirements.txt      # Dependencias del proyecto
├── manage.py             # Script de gestión de Django
├── build.sh              # Script de compilación para producción
└── README.md             # Documentación del proyecto
