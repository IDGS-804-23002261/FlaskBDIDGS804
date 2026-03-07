from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Maestros
from forms import MaestroForm

maestros = Blueprint('maestros', __name__, template_folder='templates')

@maestros.route('/')
@maestros.route('/index')
def index():
    form = MaestroForm(request.form)
    maestros_list = Maestros.query.all()
    return render_template('maestros/listadoMaes.html', form=form, maestros=maestros_list)

@maestros.route('/crear', methods=['GET', 'POST'])
def crear():
    form = MaestroForm(request.form)
    
    if request.method == 'POST' and form.validate():
        maes = Maestros(
            matricula=form.matricula.data,
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.email.data
        )
        db.session.add(maes)
        db.session.commit()
        return redirect(url_for('maestros.index'))
    
    return render_template('maestros/crear.html', form=form)

@maestros.route('/modificar', methods=['GET', 'POST'])
def modificar():
    form = MaestroForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        maes = Maestros.query.get(id)
        
        if maes:
            form.matricula.data = maes.matricula
            form.nombre.data = maes.nombre
            form.apellidos.data = maes.apellidos
            form.especialidad.data = maes.especialidad
            form.email.data = maes.email
        else:
            return redirect(url_for('maestros.index'))
    
    if request.method == 'POST':
        id = form.matricula.data
        maes = Maestros.query.get(id)
        
        if maes:
            maes.nombre = form.nombre.data
            maes.apellidos = form.apellidos.data
            maes.especialidad = form.especialidad.data
            maes.email = form.email.data
            
            db.session.add(maes)
            db.session.commit()
            return redirect(url_for('maestros.index'))
    
    return render_template('maestros/modificar.html', form=form)

@maestros.route('/detalles', methods=['GET'])
def detalles():
    id = request.args.get('id')
    maes = Maestros.query.get(id)
    
    if not maes:
        return redirect(url_for('maestros.index'))
    
    return render_template('maestros/detalles.html',
                         matricula=maes.matricula,
                         nombre=maes.nombre,
                         apellidos=maes.apellidos,
                         especialidad=maes.especialidad,
                         email=maes.email)

@maestros.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = MaestroForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        maes = Maestros.query.get(id)
        
        if maes:
            form.matricula.data = maes.matricula
            form.nombre.data = maes.nombre
            form.apellidos.data = maes.apellidos
            form.especialidad.data = maes.especialidad
            form.email.data = maes.email
        else:
            return redirect(url_for('maestros.index'))
    
    if request.method == 'POST':
        id = form.matricula.data
        maes = Maestros.query.get(id)
        
        if maes:
            db.session.delete(maes)
            db.session.commit()
        return redirect(url_for('maestros.index'))
    
    return render_template('maestros/eliminar.html', form=form)