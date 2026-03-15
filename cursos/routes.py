from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Curso, Maestros
from forms import CursoForm
from . import cursos

@cursos.route('/')
def index():
    cursos_list = Curso.query.all()
    return render_template('cursos/listadoCursos.html', cursos=cursos_list)

@cursos.route('/crear', methods=['GET', 'POST'])
def crear():
    form = CursoForm(request.form)
    
    maestros_list = Maestros.query.all()
    
    if request.method == 'POST' and form.validate():
        maestro = Maestros.query.get(form.maestro_id.data)
        if maestro:
            curso = Curso(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data,
                maestro_id=form.maestro_id.data
            )
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('cursos.index'))
    
    return render_template('cursos/crear.html', form=form, maestros=maestros_list)

@cursos.route('/modificar', methods=['GET', 'POST'])
def modificar():
    form = CursoForm(request.form)
    
    maestros_list = Maestros.query.all()
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        
        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id
        else:
            return redirect(url_for('cursos.index'))
    
    if request.method == 'POST':
        id = form.id.data
        curso = Curso.query.get(id)
        
        if curso:
            # Verificar que el maestro existe
            maestro = Maestros.query.get(form.maestro_id.data)
            if maestro:
                curso.nombre = form.nombre.data
                curso.descripcion = form.descripcion.data
                curso.maestro_id = form.maestro_id.data
                
                db.session.add(curso)
                db.session.commit()
                return redirect(url_for('cursos.index'))
    
    return render_template('cursos/modificar.html', form=form, maestros=maestros_list)

@cursos.route('/detalles', methods=['GET'])
def detalles():
    id = request.args.get('id')
    curso = Curso.query.get(id)
    
    if not curso:
        return redirect(url_for('cursos.index'))
    
    # Obtener el nombre del maestro
    maestro = Maestros.query.get(curso.maestro_id)
    nombre_maestro = f"{maestro.nombre} {maestro.apellidos}" if maestro else "No asignado"
    
    return render_template(
        'cursos/detalles.html',
        id=curso.id,
        nombre=curso.nombre,
        descripcion=curso.descripcion,
        maestro_id=curso.maestro_id,
        nombre_maestro=nombre_maestro
    )

@cursos.route('/eliminar', methods=['GET', 'POST'])
def eliminar():
    form = CursoForm(request.form)
    
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get(id)
        
        if curso:
            form.id.data = curso.id
            form.nombre.data = curso.nombre
            form.descripcion.data = curso.descripcion
            form.maestro_id.data = curso.maestro_id
        else:
            return redirect(url_for('cursos.index'))
    
    if request.method == 'POST':
        id = form.id.data
        curso = Curso.query.get(id)
        
        # Verificar si hay alumnos inscritos (después lo manejaremos)
        if curso:
            db.session.delete(curso)
            db.session.commit()
        return redirect(url_for('cursos.index'))
    
    return render_template('cursos/eliminar.html', form=form)