from flask import Flask, render_template_string, request, redirect
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_bGErR0V7gHaK@ep-sweet-voice-a2150cbk.eu-central-1.aws.neon.tech/neondb?sslmode=require'

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(50))

with app.app_context():
    db.create_all()

# HTML para el registro
registro_html = """
<!DOCTYPE html>
<html>
<head><title>Registro</title></head>
<body>
  <h2>Registro de usuario</h2>
  <form method="POST">
    Nombre: <input type="text" name="nombre"><br>
    Correo: <input type="email" name="correo"><br>
    Contraseña: <input type="password" name="contrasena"><br>
    <input type="submit" value="Registrar">
  </form>
  <p>¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
</body>
</html>
"""

# HTML para el login
login_html = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h2>Iniciar sesión</h2>
  {% if mensaje %}
    <p style="color:red;">{{ mensaje }}</p>
  {% endif %}
  <form method="POST">
    Correo: <input type="email" name="correo"><br>
    Contraseña: <input type="password" name="contrasena"><br>
    <input type="submit" value="Iniciar sesión">
  </form>
  <p>¿No tienes cuenta? <a href="/">Regístrate aquí</a></p>
</body>
</html>
"""

# Página de bienvenida
bienvenida_html = """
<!DOCTYPE html>
<html>
<head><title>Bienvenido</title></head>
<body>
  <h2>¡Bienvenido, {{ nombre }}!</h2>
  <p>Has iniciado sesión correctamente.</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nuevo_usuario = Usuario(
            nombre=request.form["nombre"],
            correo=request.form["correo"],
            contrasena=request.form["contrasena"]
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect("/login")
    return render_template_string(registro_html)

@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        correo = request.form["correo"]
        contrasena = request.form["contrasena"]
        usuario = Usuario.query.filter_by(correo=correo, contrasena=contrasena).first()
        if usuario:
            return render_template_string(bienvenida_html, nombre=usuario.nombre)
        else:
            mensaje = "Correo o contraseña incorrectos"
    return render_template_string(login_html, mensaje=mensaje)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)