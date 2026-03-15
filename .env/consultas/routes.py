from flask import redirect, render_template, request, url_for
import maestros
from models import db, Curso, Alumnos, Maestros
from . import consultas
from flask_wtf.csrf import CSRFProtect  # Si necesitas

@consultas.route('/')
def index():
    cursos = Curso.query.all()
    alumnos = Alumnos.query.all()
    maestros = Maestros.query.all()

    return render_template(
        'consultas/index.html',
        cursos=cursos,
        alumnos=alumnos,
        maestros=maestros
    )

@consultas.route('/por-curso', methods=['POST'])
def por_curso():
    curso_id = request.form.get('curso_id')
    curso = Curso.query.get(curso_id)
    
    if not curso:
        return redirect(url_for('consultas.index'))
    
    maestro = curso.maestro
    alumnos = curso.alumnos
    
    return render_template('consultas/por_curso.html',
                         curso=curso,
                         maestro=maestro,
                         alumnos=alumnos)

@consultas.route('/por-alumno', methods=['POST'])
def por_alumno():
    alumno_id = request.form.get('alumno_id')
    alumno = Alumnos.query.get(alumno_id)
    
    if not alumno:
        return redirect(url_for('consultas.index'))
    
    cursos = alumno.cursos
    
    return render_template('consultas/por_alumno.html',
                         alumno=alumno,
                         cursos=cursos)

@consultas.route('/por-maestro', methods=['POST'])
def por_maestro():

    maestro_id = int(request.form.get('maestro_id'))

    maestro = Maestros.query.filter_by(matricula=maestro_id).first()

    cursos = maestro.cursos

    return render_template(
        'consultas/por_maestro.html',
        maestro=maestro,
        cursos=cursos
    )