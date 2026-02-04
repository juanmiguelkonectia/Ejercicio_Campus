from flask import Flask, render_template, request
import psycopg2 

app = Flask(__name__)

#Vamos a enseñar a python a leer sql
def conectarCampus():
    conexion = psycopg2.connect(
        host="localhost",
        port="5432",
        database="campus",
        user="postgres",
        password="admin"
    )
    return conexion



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
      usuario = request.form["user"]
      password = request.form["password"]
      email = request.form["email"]


      #conn es una variable
      conn = conectarCampus()
      cursor = conn.cursor()
      cursor.execute("INSERT INTO users (user_name, password, user_email) VALUES (%s, %s, %s)", (usuario, password, email))

      conn.commit()
      cursor.close()
      conn.close()


      print("Usuario ingresado:", usuario)
      print("Password ingresado:", password)


      # Enviamos las variables al nuevo template HTML
      return render_template("user.html", usuario=usuario, password=password, email=email )
    
        
      #return f"Usuario {usuario} ha intentado iniciar sesión."



    return render_template("login.html") 

