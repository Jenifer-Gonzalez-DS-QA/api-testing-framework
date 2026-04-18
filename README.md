# 🧪 API Testing Framework

Framework de automatización de pruebas para APIs REST usando *Python + pytest + requests*.
Cubre operaciones CRUD completas sobre usuarios, posts, comentarios y todos con reportes HTML automáticos.

> *API usada:* [JSONPlaceholder](https://jsonplaceholder.typicode.com) — gratuita, sin registro, sin API key, disponible 24/7.

-----

## 📌 Tabla de Contenidos

- [¿Qué hace este proyecto?](#qué-hace-este-proyecto)
- [Tecnologías](#tecnologías)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Cómo Ejecutar las Pruebas](#cómo-ejecutar-las-pruebas)
- [Casos de Prueba](#casos-de-prueba)
- [Cómo leer el reporte HTML](#cómo-leer-el-reporte-html)
- [Autora](#autora)

-----

## ¿Qué hace este proyecto?

Automatiza pruebas sobre una API REST real verificando que cada endpoint responda correctamente:
el status code esperado, la estructura del JSON y los datos devueltos. Cubre los 5 métodos HTTP
principales: *GET, POST, PUT, PATCH y DELETE*.

-----

## 🛠 Tecnologías

|Herramienta|Versión|Uso                        |
|-----------|-------|---------------------------|
|Python     |3.11+  |Lenguaje base              |
|pytest     |7.4.3  |Framework de pruebas       |
|requests   |2.31.0 |Cliente HTTP               |
|pytest-html|4.1.1  |Generación de reportes HTML|

-----

## 📁 Estructura del Proyecto


api-testing-framework/
│
├── tests/
│   ├── __init__.py
│   ├── test_posts.py       # Pruebas CRUD sobre /posts
│   ├── test_users.py       # Pruebas CRUD sobre /users
│   └── test_comments.py    # Pruebas sobre /comments y /todos
│
├── utils/
│   ├── __init__.py
│   └── api_client.py       # Cliente HTTP reutilizable con logging
│
├── reports/                # Reportes HTML generados (ignorados en git)
│   └── report.html
│
├── pytest.ini              # Configuración de pytest
├── requirements.txt        # Dependencias
├── .gitignore
└── README.md


-----

## ⚙️ Instalación

# 1. Clonar el repositorio
git clone https://github.com/Jenifer-Gonzalez-DS-QA/api-testing-framework.git
cd api-testing-framework

# 2. Crear entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt


-----

## ▶️ Cómo Ejecutar las Pruebas

# Toda la suite
pytest

# Un archivo específico
pytest tests/test_posts.py
pytest tests/test_users.py
pytest tests/test_comments.py

# Una prueba específica
pytest tests/test_posts.py::TestGetPosts::test_get_posts_status_200

# Con más detalle en consola
pytest -v

# Sin generar reporte HTML
pytest --no-header -q


> El reporte HTML se genera automáticamente en reports/report.html.
> Ábrelo en cualquier navegador haciendo doble clic.

-----

## ✅ Casos de Prueba

### 📝 Posts (test_posts.py) — 16 pruebas

|# |Caso de Prueba               |Método             |Resultado Esperado     |
|--|-----------------------------|-------------------|-----------------------|
|1 |Listado completo de posts    |GET /posts         |200 + lista            |
|2 |La respuesta es una lista    |GET /posts         |isinstance(list)       |
|3 |Total de posts = 100         |GET /posts         |len == 100             |
|4 |Post por ID devuelve 200     |GET /posts/1       |200                    |
|5 |Campos del post presentes    |GET /posts/1       |userId, id, title, body|
|6 |ID correcto en respuesta     |GET /posts/1       |id == 1                |
|7 |Post inexistente devuelve 404|GET /posts/9999    |404                    |
|8 |Filtrar posts por userId     |GET /posts?userId=1|200 + todos userId=1   |
|9 |Crear post devuelve 201      |POST /posts        |201                    |
|10|Post creado tiene ID         |POST /posts        |“id” en respuesta      |
|11|Datos del post coinciden     |POST /posts        |title y body correctos |
|12|PUT devuelve 200             |PUT /posts/1       |200                    |
|13|PUT actualiza datos          |PUT /posts/1       |título actualizado     |
|14|PATCH devuelve 200           |PATCH /posts/1     |200                    |
|15|PATCH actualiza campo        |PATCH /posts/1     |campo correcto         |
|16|DELETE devuelve 200          |DELETE /posts/1    |200 + {}               |

### 👤 Usuarios (test_users.py) — 11 pruebas

|# |Caso de Prueba           |Método            |Resultado Esperado       |
|--|-------------------------|------------------|-------------------------|
|1 |Listado de usuarios      |GET /users        |200                      |
|2 |Total de usuarios = 10   |GET /users        |len == 10                |
|3 |Usuario por ID           |GET /users/1      |200                      |
|4 |Campos del usuario       |GET /users/1      |id, name, username, email|
|5 |ID correcto              |GET /users/1      |id == 1                  |
|6 |Usuario inexistente      |GET /users/9999   |404                      |
|7 |Posts del usuario        |GET /users/1/posts|200 + lista              |
|8 |Crear usuario            |POST /users       |201                      |
|9 |Usuario creado tiene ID  |POST /users       |“id” presente            |
|10|Datos coinciden          |POST /users       |name y email correctos   |
|11|PUT y PATCH devuelven 200|PUT/PATCH /users/1|200                      |

### 💬 Comentarios y Todos (test_comments.py) — 13 pruebas

|#    |Caso de Prueba            |Método                |Resultado Esperado  |
|-----|--------------------------|----------------------|--------------------|
|1-4  |CRUD básico de comentarios|GET /comments         |200                 |
|5    |Email con formato válido  |GET /comments/1       |“@” en email        |
|6    |Filtrar por postId        |GET /comments?postId=1|todos postId=1      |
|7    |Comentario inexistente    |GET /comments/9999    |404                 |
|8-9  |Crear comentario          |POST /comments        |201                 |
|10-13|Todos: campos y filtros   |GET /todos            |200 + bool completed|

-----

## 📊 Cómo leer el reporte HTML

Abre reports/report.html en tu navegador. Verás:

*Encabezado:* resumen total — cuántas pasaron, cuántas fallaron, tiempo total.

*Tabla de resultados:* cada fila es una prueba.

- 🟢 *PASSED* — el endpoint respondió exactamente como se esperaba
- 🔴 *FAILED* — algo no coincidió; haz clic en la fila para ver el error

*Detalle de error (cuando hay FAILED):*


AssertionError: assert 404 == 200


Significa: esperabas 200 pero obtuviste 404. Eso te dice exactamente qué endpoint falló y con qué status real.

*Duration:* tiempo en segundos que tomó cada prueba. Útil para detectar endpoints lentos.

-----

## 👩‍💻 Autora

*Jenifer Gonzalez*

Data Science | QA Engineer | Scrum Master  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://linkedin.com/in/jenifer-paola-gonzalez-peñuela)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/Jenifer-Gonzalez-DS-QA/)

-----

> 💡 *Este proyecto es parte de un portafolio de 3 proyectos de automatización QA.
> Ver también: [QA Dashboard](https://github.com/Jenifer-Gonzalez-DS-QA/qa-dashboard) y [QA CI/CD Pipeline](https://github.com/Jenifer-Gonzalez-DS-QA/qa-cicd-pipeline)*
