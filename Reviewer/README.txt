========================================================================
                         REVIEWER API - PROYECTO FINAL
========================================================================

Una API REST robusta desarrollada en Django y Django REST Framework (DRF) 
para la gestión de películas, géneros y reseñas de usuarios, con autenticación
segura por JSON Web Tokens (JWT) y una integración avanzada con Modelos de 
Lenguaje Grande (LLMs) ejecutados localmente mediante Ollama.

------------------------------------------------------------------------
1. REQUISITOS PREVIOS
------------------------------------------------------------------------
Para ejecutar y probar este proyecto correctamente en tu computadora, 
necesitas tener instalado lo siguiente:

- Python (versión 3.10 o superior recomendada)
- Git (opcional, para control de versiones)
- Ollama (para la funcionalidad de Inteligencia Artificial local)

------------------------------------------------------------------------
2. INSTALACIÓN Y CONFIGURACIÓN DEL ENTORNO
------------------------------------------------------------------------

1. Clonar o abrir la carpeta del proyecto en tu terminal o VS Code.

2. Crear y activar el entorno virtual:
   - En Windows (PowerShell / CMD):
     python -m venv env
     .\env\Scripts\activate

3. Instalar las dependencias necesarias:
   pip install django djangorestframework djangorestframework-simplejwt django-filter openai

4. Aplicar las migraciones de la base de datos:
   python manage.py makemigrations
   python manage.py migrate

5. Crear un superusuario para acceder al panel de administración:
   python manage.py createsuperuser

------------------------------------------------------------------------
3. EJECUCIÓN DEL SERVIDOR
------------------------------------------------------------------------

Para poner en marcha el servidor de desarrollo de Django, ejecuta:
   python manage.py runserver

El proyecto estará disponible en: http://127.0.0.1:8000/

------------------------------------------------------------------------
4. CONFIGURACIÓN DE LA INTELIGENCIA ARTIFICIAL (OLLAMA)
------------------------------------------------------------------------
Para que el endpoint de resumen por IA funcione localmente:
1. Asegúrate de tener Ollama instalado y ejecutándose en tu PC.
2. Descarga el modelo requerido abriendo una terminal externa y ejecutando:
   ollama run llama3

------------------------------------------------------------------------
5. GUÍA DE ENDPOINTS Y FUNCIONALIDADES DE LA API
------------------------------------------------------------------------

- Autenticación JWT:
  * POST /api/token/ -> Obtener token de acceso enviando credenciales (username y password).
  * POST /api/token/refresh/ -> Renovar el token de acceso usando el token de refresco.

- Géneros:
  * GET /api/genres/ -> Listar todos los géneros cinematográficos.
  * POST /api/genres/ -> Registrar un nuevo género (requiere permisos).

- Películas:
  * GET /api/movies/ -> Listar todas las películas. Soporta filtros (?genre=ID), búsquedas (?search=texto) y ordenamientos (?ordering=title).
  * POST /api/movies/ -> Registrar una nueva película.

- Resumen por IA (LLM Local):
  * GET /api/movies/{id}/summary/ -> Envía todas las reseñas de la película seleccionada a Ollama (Llama 3) y devuelve un resumen automatizado de la opinión pública.

- Reseñas:
  * GET /api/reviews/ -> Listar todas las reseñas de los usuarios.
  * POST /api/reviews/ -> Crear una nueva reseña (Obligatorio incluir la cabecera "Authorization: Bearer <tu_token>"). El sistema asigna automáticamente el usuario autenticado.