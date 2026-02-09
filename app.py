# ===============================
# IMPORTS
# ===============================

from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import os

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


# ===============================
# CARGA VARIABLES DE ENTORNO
# ===============================

# Carga el archivo .env
load_dotenv()


# ===============================
# CONFIGURACIÓN FLASK
# ===============================

app = Flask(__name__)

# Clave secreta necesaria para manejar sesiones
# ⚠️ Debe venir del .env
app.secret_key = os.getenv("SECRET_KEY")


# ===============================
# CONEXIÓN A LA BASE DE DATOS
# ===============================

def conectarCampus():
    """
    Crea y devuelve una conexión a PostgreSQL usando
    variables de entorno (más seguro)
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


# ===============================
# DECORADOR LOGIN REQUIRED
# ===============================

def login_required(f):
    """
    Decorador que protege rutas:
    si no hay usuario en sesión → redirige a login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


# ===============================
# RUTA PRINCIPAL
# ===============================

@app.route("/")
def index():
    """
    Página principal pública:
    - Si hay sesión activa → dashboard
    - Si no hay sesión → mostrar index.html con login y registro
    """
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    
    # Mostramos la página principal
    return render_template("index.html")




# ===============================
# LOGIN
# ===============================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]

        conn = conectarCampus()
        cursor = conn.cursor()

        # Buscamos el usuario en la BD
        cursor.execute(
            "SELECT id_user, user_name, password FROM users WHERE user_name = %s",
            (usuario,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Si el usuario existe y la contraseña coincide
        if user and check_password_hash(user[2], password):

            # Guardamos datos en sesión
            session["user_id"] = user[0]
            session["user_name"] = user[1]

            return redirect(url_for("dashboard"))

        # Si falla el login
        flash("Usuario o contraseña incorrectos")

    return render_template("login.html")


# ===============================
# REGISTRO
# ===============================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        usuario = request.form["user"]
        password = request.form["password"]
        email = request.form["email"]

        # Hasheamos la contraseña
        hashed_password = generate_password_hash(password)

        conn = conectarCampus()
        cursor = conn.cursor()

        # Comprobamos si el usuario o email ya existen
        cursor.execute(
            "SELECT id_user FROM users WHERE user_name = %s OR user_email = %s",
            (usuario, email)
        )

        if cursor.fetchone():
            flash("El usuario o el email ya existen")
            cursor.close()
            conn.close()
            return render_template("register.html")

        # Insertamos el nuevo usuario
        cursor.execute(
            """
            INSERT INTO users (user_name, password, user_email)
            VALUES (%s, %s, %s)
            """,
            (usuario, hashed_password, email)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Registro correcto. Ya puedes iniciar sesión")
        return redirect(url_for("login"))

    return render_template("register.html")


# ===============================
# DASHBOARD (ZONA PRIVADA)
# ===============================

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        usuario=session["user_name"]
    )


# ===============================
# LOGOUT
# ===============================

@app.route("/logout")
@login_required
def logout():
    # Eliminamos toda la sesión
    session.clear()
    return redirect(url_for("login"))


# ===============================
# ARRANQUE APP
# ===============================

if __name__ == "__main__":
    app.run(debug=True)
