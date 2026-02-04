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

        # Recogemos datos del formulario
        usuario = request.form["user"]
        password = request.form["password"]

        # Conectamos a la BD
        conn = conectarCampus()
        cursor = conn.cursor()

        # Buscamos si existe un usuario con ese nombre y password
        cursor.execute(
            "SELECT * FROM users WHERE user_name = %s AND password = %s",
            (usuario, password)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Si existe, mostramos sus datos
        if user:
            return render_template(
                "user.html",
                usuario=user[1],
                password=user[2],
                email=user[3]
            )
        else:
            return "Usuario o contraseña incorrectos"

    # Si es GET, mostramos el formulario
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

        # Insertamos nuevo usuario en la BD
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
