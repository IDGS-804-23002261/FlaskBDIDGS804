from flask import Blueprint, render_template, request, redirect, url_for
from models import db, Inscripcion, Alumnos, Curso, Maestros
from forms import InscripcionForm
from . import inscripciones

@inscripciones.route('/')
def index():
    inscripciones_list = db.session.query(
        Inscripcion, Alumnos, Curso, Maestros
    ).join(
        Alumnos, Inscripcion.alumno_id == Alumnos.id
    ).join(
        Curso, Inscripcion.curso_id == Curso.id
    ).join(
        Maestros, Curso.maestro_id == Maestros.matricula
    ).all()
    
    return render_template('inscripciones/listado.html', inscripciones=inscripciones_list)

@inscripciones.route('/crear', methods=['GET', 'POST'])
def crear():
    form = InscripcionForm(request.form)  
    
    if request.method == 'POST' and form.validate():
        alumno_id = form.alumno_id.data
        curso_id = form.curso_id.data
        
        existe = Inscripcion.query.filter_by(
            alumno_id=alumno_id, 
            curso_id=curso_id
        ).first()
        
        if not existe:
            inscripcion = Inscripcion(
                alumno_id=alumno_id,
                curso_id=curso_id
            )
            db.session.add(inscripcion)
            db.session.commit()
        
        return redirect(url_for('inscripciones.index'))
    
    alumnos = Alumnos.query.all()
    cursos = Curso.query.all()
    return render_template('inscripciones/crear.html', 
                         form=form,           
                         alumnos=alumnos, 
                         cursos=cursos)

@inscripciones.route('/eliminar/<int:id>')
def eliminar(id):
    inscripcion = Inscripcion.query.get(id)
    if inscripcion:
        db.session.delete(inscripcion)
        db.session.commit()
    return redirect(url_for('inscripciones.index'))

@inscripciones.route('/alumno/<int:alumno_id>')
def cursos_por_alumno(alumno_id):
    alumno = Alumnos.query.get_or_404(alumno_id)
    return render_template('inscripciones/alumno_cursos.html', alumno=alumno)

@inscripciones.route('/curso/<int:curso_id>')
def alumnos_por_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    return render_template('inscripciones/curso_alumnos.html', curso=curso)