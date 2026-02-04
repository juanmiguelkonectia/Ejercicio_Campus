from flask import Flask, render_template, request
import psycopg2 

app = Flask(__name__)

# Función para conectar con la base de datos Campus
def conectarCampus():
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="campus",
        user="postgres",
        password="admin"
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
        password = request.form["password"]

        conn = conectarCampus()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE user_name = %s AND password = %s",
            (usuario, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Si el usuario existe
        if user:
            return render_template(
                "user.html",
                usuario=user[1],
                password=user[2],
                email=user[3]
            )
        else:
            # ❌ Login incorrecto → volvemos al login con mensaje
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
        password = request.form["password"]
        email = request.form["email"]

        conn = conectarCampus()
        cursor = conn.cursor()

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

            # ❌ Registro incorrecto → volvemos al formulario
            return render_template(
                "register.html",
                error="El usuario o el email ya existen",
                usuario=usuario,
                email=email
            )

        cursor.execute(
            "INSERT INTO users (user_name, password, user_email) VALUES (%s, %s, %s)",
            (usuario, password, email)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return render_template(
            "user.html",
            usuario=usuario,
            password=password,
            email=email
        )

    return render_template("register.html")

