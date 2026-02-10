# 🎓 Campus - Sistema de Autenticación Web

<div align="center">

![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=flat-square&logo=flask)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-BBDD00?style=flat-square&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey?style=flat-square)

**Un sistema web de autenticación y gestión de usuarios construido con Flask**

</div>

---

## 📋 Descripción del Proyecto

Campus es una aplicación web educativa desarrollada con **Flask** que implementa un sistema completo de **autenticación y gestión de usuarios**. El proyecto demuestra cómo construir un sitio web seguro con:

- ✅ Sistema de **registro de usuarios**
- ✅ Sistema de **login con validación**
- ✅ **Gestión de sesiones** seguras
- ✅ **Encriptación de contraseñas** con Werkzeug
- ✅ Protección de rutas privadas
- ✅ Base de datos PostgreSQL
- ✅ Variables de entorno para seguridad

---

## 🏗️ Estructura del Proyecto

```
Ejercicio_Campus/
│
├── app.py                    # 🔧 Aplicación principal Flask
├── requeriments.txt          # 📦 Dependencias del proyecto
├── README.md                 # 📖 Este archivo
├── LICENSE.md                # ⚖️ Licencia CC BY-SA 4.0
│
├── static/
│   └── style.css             # 🎨 Estilos CSS
│
├── templates/                # 🎭 Plantillas HTML (Jinja2)
│   ├── base.html             # 📄 Plantilla base
│   ├── index.html            # 🏠 Página principal
│   ├── login.html            # 🔐 Formulario de login
│   ├── register.html         # 📝 Formulario de registro
│   ├── user.html             # 👤 Perfil de usuario
│   └── dashboard.html        # 📊 Panel de control
│
├── __pycache__/              # 🗑️ Caché de Python
└── desechables/              # 📚 Archivos de referencia

```

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask 3.0.0** - Framework web ligero y flexible
- **Python 3.x** - Lenguaje de programación
- **Werkzeug 3.0.1** - Utilidades de seguridad (hashing de contraseñas)
- **python-dotenv 1.0.0** - Gestión de variables de entorno

### Base de Datos
- **PostgreSQL** - Sistema de gesión de base de datos relacional
- **psycopg2-binary 2.9.9** - Driver de Python para PostgreSQL

### Frontend
- **Jinja2** - Motor de plantillas HTML (integrado en Flask)
- **HTML5** - Estructura de páginas
- **CSS3** - Estilos y diseño

---

## 📦 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Python 3.7+** ([descargar](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([descargar](https://www.postgresql.org/download/))
- **pip** (gestor de paquetes de Python, incluido con Python)

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Thibor82/campus.git
cd campus
```

### 2️⃣ Crear un entorno virtual (recomendado)

**En Windows (PowerShell):**
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Instalar todas las dependencias

```bash
pip install -r requeriments.txt
```

Este comando instala automáticamente:
- Flask
- psycopg2-binary
- python-dotenv
- Werkzeug

### 4️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Configuración Flask
SECRET_KEY=tu_clave_secreta_muy_segura

# Configuración Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_NAME=campus_db
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_postgres
```

### 5️⃣ Crear la base de datos

Conectate a PostgreSQL y ejecuta:

```sql
CREATE DATABASE campus_db;

\c campus_db

CREATE TABLE users (
    id_user SERIAL PRIMARY KEY,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ▶️ Ejecutar la Aplicación

**Paso 1:** Activa el entorno virtual (si no lo has hecho)

```bash
.\.venv\Scripts\Activate.ps1   # Windows
source .venv/bin/activate      # macOS/Linux
```

**Paso 2:** Inicia el servidor Flask

```bash
Flask --app app run
```

O alternativamente:

```bash
python -m flask run
```

**Paso 3:** Abre tu navegador

La aplicación estará disponible en: `http://127.0.0.1:5000`

---

## 🔄 Flujo de la Aplicación

```
┌─────────────────────────────────────────────────────────────┐
│                   INICIO (/)                                │
│  Sin sesión → index.html  |  Con sesión → /dashboard       │
└────────────┬──────────────────────────────┬─────────────────┘
             │                              │
        ┌────▼──────────┐         ┌─────────▼────────┐
        │ /login (POST)  │         │ /dashboard       │
        │ Usuario existe?│         │ (zona privada)   │
        │ ✓ Contraseña   │         │                  │
        │   coincide?    │         │ [Bienvenida]     │
        └────┬───────────┘         │ [Cerrar sesión]  │
             │                     └──────────────────┘
             │
        ┌────▼──────────┐
        │ Crear sesión  │
        │ redis → Flash │
        └────┬──────────┘
             │
        ┌────▼──────────┐    ┌──────────────┐
        │ /dashboard    │    │ /register    │
        │ (autenticado) │    │ (nuevo user) │
        └───────────────┘    └──────────────┘
```

---

## 🔗 Rutas Disponibles

| Ruta | Método | Descripción | Acceso |
|------|--------|-------------|--------|
| `/` | GET | Página principal | Público |
| `/login` | GET, POST | Iniciar sesión | Público |
| `/register` | GET, POST | Registrar nuevo usuario | Público |
| `/dashboard` | GET | Panel de control | Solo autenticado |
| `/logout` | GET | Cerrar sesión | Solo autenticado |

---

## 🎭 Plantillas HTML (Jinja2)

### 📄 `base.html` - Plantilla Base

Todas las páginas extienden esta plantilla, proporcionando un diseño consistente:

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Campus{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header>
        <h1>🎓 Campus</h1>
    </header>
    
    <main>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2026 Campus. Todos los derechos reservados.</p>
    </footer>
</body>
</html>
```

---

### 🔐 `login.html` - Formulario de Login

```html
{% extends "base.html" %}

{% block content %}
<h2>Iniciar Sesión</h2>

<form method="POST" action="/login">
    <label>Usuario:</label>
    <input type="text" name="user" 
           placeholder="Introduce tu usuario" 
           required autocomplete="off">
    <br><br>

    <label>Contraseña:</label>
    <input type="password" name="password" 
           placeholder="Introduce tu contraseña" 
           required autocomplete="off">
    <br><br>

    <button type="submit">Entrar</button>
    
    <a href="#" class="secondary">¿Olvidaste tu contraseña?</a>
    <a href="/register" class="secondary">Registrarse</a>
</form>
{% endblock %}
```

**Formulario enviado:**
```
POST /login
├── user: "juan_miguel"
└── password: "micontraseña123"
```

---

### 📝 `register.html` - Formulario de Registro

```html
{% extends "base.html" %}

{% block content %}
<h2>Registro de Usuario</h2>

<form method="POST" action="/register">
    <label>Usuario:</label>
    <input type="text" name="user" 
           placeholder="Elige un nombre de usuario" 
           required autocomplete="off">
    <br><br>

    <label>Contraseña:</label>
    <input type="password" name="password" 
           placeholder="Elige una contraseña segura" 
           required autocomplete="off">
    <br><br>

    <label>Email:</label>
    <input type="email" name="email" 
           placeholder="tu@email.com" 
           required autocomplete="off">
    <br><br>

    <button type="submit">Registrarse</button>
</form>
{% endblock %}
```

**Validaciones:**
- ✓ Usuario único en la BD
- ✓ Email válido y único
- ✓ Contraseña encriptada con Werkzeug

---

### 📊 `dashboard.html` - Panel de Control

```html
{% extends "base.html" %}

{% block content %}
    <h2>Bienvenido al Dashboard</h2>
    
    <p>Hola, <strong>{{ usuario }}</strong> 👋</p>
    
    <p>Esta es tu zona privada. Solo los usuarios autenticados pueden verla.</p>
    
    <a href="{{ url_for('logout') }}" class="btn btn-danger">
        Cerrar Sesión
    </a>
{% endblock %}
```

**Características:**
- 🔒 Solo accesible si hay sesión activa
- 🎯 Decorador `@login_required` protege la ruta
- 👤 Muestra el nombre del usuario en sesión

---

## 🔒 Seguridad Implementada

### 1. **Encriptación de Contraseñas**
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Al registrarse
hashed_password = generate_password_hash(password)

# Al hacer login
check_password_hash(stored_hash, user_password)
```

### 2. **Gestión de Sesiones**
```python
session["user_id"] = user[0]
session["user_name"] = user[1]
```

### 3. **Protección de Rutas**
```python
@login_required  # Decorador personalizado
def dashboard():
    return render_template("dashboard.html", usuario=session["user_name"])
```

### 4. **Variables de Entorno**
- Credenciales guardadas en `.env` (nunca en el código)
- Consultas parametrizadas contra inyección SQL

```python
cursor.execute(
    "SELECT * FROM users WHERE user_name = %s",
    (usuario,)  # Parámetro separado
)
```

---

## 📚 Estructura de Datos

### Tabla `users`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id_user` | SERIAL (PK) | Identificador único |
| `user_name` | VARCHAR(50) | Nombre de usuario (único) |
| `password` | VARCHAR(255) | Contraseña encriptada |
| `user_email` | VARCHAR(100) | Email del usuario (único) |
| `created_at` | TIMESTAMP | Fecha de registro |

---

## 🐛 Solución de Problemas

### ❌ Error: "No such module psycopg2"
**Solución:**
```bash
pip install psycopg2-binary
```

### ❌ Error: "Connection refused" (PostgreSQL)
**Solución:**
- Verifica que PostgreSQL está ejecutándose
- Comprueba las credenciales en `.env`
- Abre el puerto 5432

### ❌ Error: "SECRET_KEY missing"
**Solución:**
```bash
# Agrega SECRET_KEY a tu archivo .env
echo SECRET_KEY=tu_clave_secreta >> .env
```

---

## 📖 Referencia de Funciones Principales

### `conectarCampus()`
Crea una conexión a la base de datos PostgreSQL usando variables de entorno.

### `login_required(f)`
Decorador que protege rutas: solo usuarios autenticados pueden acceder.

### `index()`
Ruta principal que redirige según si hay sesión activa.

### `login()` / `register()`
Gestiona autenticación y registro de usuarios.

### `dashboard()`
Zona privada solo para usuarios autenticados.

### `logout()`
Limpia la sesión y desconecta al usuario.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## ⚖️ Licencia

<a href="https://github.com/Thibor82/campus">Campus_Konectia</a> © 2026 by 
<a href="https://spaceham.es/">Rubén Caballero</a> is licensed under 
<a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a>

<a href="https://creativecommons.org/licenses/by-sa/4.0/">
    <img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="CC" style="max-width: 1em;max-height:1em;margin-left: .2em;">
    <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="BY" style="max-width: 1em;max-height:1em;margin-left: .2em;">
    <img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" alt="SA" style="max-width: 1em;max-height:1em;margin-left: .2em;">
</a>

---

## 📞 Contacto

- **Autor:** Rubén Caballero
- **Website:** https://spaceham.es/
- **GitHub:** https://github.com/Thibor82/campus

---

**Última actualización:** 10 de febrero de 2026