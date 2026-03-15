from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask_migrate import Migrate  # referencia de la migración
from flask import g
import forms
from models import db
from models import Alumnos, Maestros, Curso, Inscripcion
from maestros import maestros
from cursos.routes import cursos
from inscripciones.routes import inscripciones
from alumnos.routes import alumnos
from consultas import consultas

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Registrar todos los blueprints
app.register_blueprint(maestros, url_prefix='/maestros')  # todos los archivos de maestros seran con esta ruta
app.register_blueprint(cursos, url_prefix='/cursos')
app.register_blueprint(inscripciones, url_prefix='/inscripciones')
app.register_blueprint(alumnos, url_prefix='/alumnos')  # CORREGIDO: le faltaba el /
app.register_blueprint(consultas, url_prefix='/consultas')

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_fount(e):
    return render_template("404.html"), 404




"""
@app.route("/", methods=['GET','POST'])
@app.route("/index")
def index():
    create_form=forms.UserForm(request.form)
    alumno=Alumnos.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)


@app.route("/Alumnos", methods=['GET','POST'])
def alumnos():
    create_form=forms.UserForm(request.form)
    if request.method=='POST':
        alum=Alumnos(nombre=create_form.nombre.data, apellidos=create_form.apellidos.data, email=create_form.correo.data, telefono=create_form.telefono.data)
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("Alumnos.html", form=create_form)


@app.route("/modificar", methods=['GET','POST'])
def modificar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.correo.data=alum1.email
        create_form.telefono.data=alum1.telefono

    if request.method=='POST':
        id=request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum1.id=id
        alum1.nombre=create_form.nombre.data
        alum1.apellidos=create_form.apellidos.data
        alum1.email=create_form.correo.data
        alum1.telefono=create_form.telefono.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("modificar.html", form=create_form)


@app.route("/eliminar", methods=['GET','POST'])
def eliminar():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=request.args.get('id')
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.correo.data=alum1.email
        create_form.telefono.data=alum1.telefono
    
    if request.method=='POST':
        id=create_form.id.data
        alum=Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html",form=create_form)


@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
    create_form=forms.UserForm(request.form)
    if request.method=='GET':
        id=request.args.get('id')
        alum1 = db.session.query(Alumnos).filter(Alumnos.id==id).first()
        id=request.args.get('id')
        nombre=alum1.nombre
        apaterno=alum1.apellidos
        email=alum1.email
        telefono=alum1.telefono
    
    return render_template('detalles.html', id=id, nombre=nombre, apaterno=apaterno, email=email)
"""


@app.route('/')
@app.route('/index')
def home():
    """Redirige al index bienvenda"""
    return render_template('index.html')


"""
@app.route('/nuevo')
def nuevo():
    return render_template('nuevoMaes.html')
"""

if __name__ == '__main__':
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True)