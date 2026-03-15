from wtforms import Form
from flask_wtf import FlaskForm

from wtforms import StringField, IntegerField, TextAreaField
from wtforms import EmailField
from wtforms import validators

class UserForm(FlaskForm):
    id = IntegerField("id", [
        validators.optional(),
        validators.number_range(min=1, max=20, message='valor no valido')
    ])
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=20, message='requiere min=4 max=20')
    ])
    apellidos = StringField("apellidos", [
        validators.DataRequired(message="El apellido es requerido")
    ])
    correo = EmailField("correo", [
    validators.DataRequired(message="El correo es requerido"),  # ✅ CORREGIDO
    validators.Email(message='Ingrese un correo valido')
])
    telefono = StringField("telefono", [
        validators.DataRequired(message="El telefono es requerido")
    ])

class MaestroForm(FlaskForm):
    matricula = IntegerField('Matrícula', [
        validators.optional()
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es requerido")
    ])
    apellidos = StringField('Apellidos', [
        validators.DataRequired(message="Los apellidos son requeridos")
    ])
    especialidad = StringField('Especialidad', [
        validators.DataRequired(message="La especialidad es requerida")
    ])
    email = EmailField('Correo', [
        validators.DataRequired(message="El correo es requerido"),
        validators.Email(message='Ingrese un correo valido')
    ])


class CursoForm(FlaskForm):
    id = IntegerField('ID')
    nombre = StringField('Nombre del Curso', [
        validators.DataRequired(message="El nombre es requerido"),
        validators.length(min=4, max=150, message='requiere min=4 max=150')
    ])
    descripcion = TextAreaField('Descripción', [
        validators.DataRequired(message="La descripción es requerida")
    ])
    maestro_id = IntegerField('ID del Maestro', [
        validators.DataRequired(message="El ID del maestro es requerido")
    ])


class InscripcionForm(FlaskForm):
    alumno_id = IntegerField('ID del Alumno', [
        validators.DataRequired(message="El ID del alumno es requerido")
    ])
    curso_id = IntegerField('ID del Curso', [
        validators.DataRequired(message="El ID del curso es requerido")
    ])