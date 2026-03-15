from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Alumnos
from forms import UserForm
from . import alumnos

@alumnos.route('/')
def index():
    form = UserForm(request.form)
    alumnos_list = Alumnos.query.all()
    return render_template('alumnos/listado.html', form=form, alumno=alumnos_list)

@alumnos.route('/crear', methods=['GET', 'POST'])
def crear():
    form = UserForm(request.form)
    
    if request.method == 'POST' and form.validate():
        alum = Alumnos(
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            email=form.correo.data,
            telefono=form.telefono.data
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('alumnos.index'))
    
    return render_template('alumnos/crear.html', form=form)

@alumnos.route('/modificar', methods=['GET', 'POST'])
def modificar():
    form = UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum = Alumnos.query.get(id)
        
        if alum:
            form.id.data = alum.id
            form.nombre.data = alum.nombre
            form.apellidos.data = alum.apellidos
            form.correo.data = alum.email
            form.telefono.data = alum.telefono
        else:
            return redirect(url_for('alumnos.index'))
    
    if request.method == 'POST':
        id = form.id.data
        alum = Alumnos.query.get(id)
        
        if alum:
            alum.nombre = form.nombre.data
            alum.apellidos = form.apellidos.data
            alum.email = form.correo.data
            alum.telefono = form.telefono.data
            
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('alumnos.index'))
    
    return render_template('alumnos/modificar.html', form=form)

@alumnos.route('/detalles', methods=['GET'])
def detalles():
    id = request.args.get('id')
    alum = Alumnos.query.get(id)
    
    if not alum:
        return redirect(url_for('alumnos.index'))
    
    # Obtener los cursos del alumno
    cursos_alumno = alum.cursos if alum.cursos else []
    
    return render_template('alumnos/detalles.html',
                         id=alum.id,
                         nombre=alum.nombre,
                         apellidos=alum.apellidos,
                         email=alum.email,
                         telefono=alum.telefono,
                         cursos=cursos_alumno)

@alumnos.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = UserForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        alum = Alumnos.query.get(id)
        
        if alum:
            form.id.data = alum.id
            form.nombre.data = alum.nombre
            form.apellidos.data = alum.apellidos
            form.correo.data = alum.email
            form.telefono.data = alum.telefono
        else:
            return redirect(url_for('alumnos.index'))
    
    if request.method == 'POST':
        id = form.id.data
        alum = Alumnos.query.get(id)
        
        # Verificar si tiene inscripciones
        if alum and alum.cursos:
            # Tiene cursos inscritos, no se puede eliminar
            return redirect(url_for('alumnos.index'))
        
        if alum:
            db.session.delete(alum)
            db.session.commit()
        return redirect(url_for('alumnos.index'))
    
    return render_template('alumnos/eliminar.html', form=form)