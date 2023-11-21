import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
DB_USER = 'fl0user'
DB_PASS = '4qWeDjYl1ixT'
DB_HOST = 'ep-billowing-sun-46121554.eu-central-1.aws.neon.fl0.io'
DB_NAME = 'database'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Datos
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer)

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50))

# Función para inicializar la base de datos con registros de ejemplo
def init_db():
    db.create_all()  # Crea las tablas si no existen

    # Verificar si la base de datos está vacía
    if not Persona.query.first():
        personas = [
            Persona(nombre="Carlos", edad=30),
            Persona(nombre="Lucía", edad=25)
        ]

        mascotas = [
            Mascota(nombre="Max", tipo="Perro"),
            Mascota(nombre="Mia", tipo="Gato")
        ]

        db.session.add_all(personas + mascotas)
        db.session.commit()

@app.route('/personas')
def get_personas():
    personas = Persona.query.all()
    return render_template('personas.html', personas=personas)

@app.route('/mascotas')
def get_mascotas():
    mascotas = Mascota.query.all()
    return jsonify([{'id': m.id, 'nombre': m.nombre, 'tipo': m.tipo} for m in mascotas])

port = int(os.environ.get("PORT", 5000))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

@app.route('/hola')
def hola():
   return 'Hola'

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(port=port)
