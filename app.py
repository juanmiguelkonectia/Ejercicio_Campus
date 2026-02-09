from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request
import psycopg2 
from dotenv import load_dotenv
import os


#Cargar variables de entorno desde archivo.env
load_dotenv()

app = Flask(__name__)

# Función para conectar con la base de datos Campus
def conectarCampus():
    
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conexion

# Ruta principal
@app.route("/")
def index():
    # Mostramos la página inicial con login / registro
    
    return render_template("index.html")


# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        usuario = request.form["user"]
        password_plana = request.form["password"]

        conn = conectarCampus()
        cursor = conn.cursor()

        # Buscamos el usuario SOLO por nombre
        cursor.execute(
            "SELECT * FROM users WHERE user_name = %s",
            (usuario,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Si el usuario existe y la contraseña coincide
        if user and check_password_hash(user[2], password_plana):
            return render_template(
                "user.html",
                usuario=user[1],
                password="(oculta por seguridad)",
                email=user[3]
            )
        else:
            return render_template(
                "login.html",
                error="Usuario o contraseña incorrectos"
            )

    return render_template("login.html")



# -------- REGISTRO --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        usuario = request.form["user"]
        password_plana = request.form["password"]
        email = request.form["email"]

        conn = conectarCampus()
        cursor = conn.cursor()

        # Comprobamos si ya existe usuario o email
        cursor.execute(
            """
            SELECT * FROM users 
            WHERE user_name = %s 
            OR user_email = %s
            """,
            (usuario, email)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()
            return render_template(
                "register.html",
                error="El usuario o el email ya existen",
                usuario=usuario,
                email=email
            )

        # 🔐 Hasheamos la contraseña
        password_hash = generate_password_hash(password_plana)

        # Insertamos el usuario con la contraseña hasheada
        cursor.execute(
            "INSERT INTO users (user_name, password, user_email) VALUES (%s, %s, %s)",
            (usuario, password_hash, email)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            "user.html",
            usuario=usuario,
            password="(oculta por seguridad)",
            email=email
        )

    return render_template("register.html")


