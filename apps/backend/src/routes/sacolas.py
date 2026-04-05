from flask import Blueprint, jsonify
from schemas.sacola_schema import CourseSchema
from schemas.supermercado_schema import LessonSchema
from models import Course, Lesson

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
def get_courses():
    """
    Lista todos os cursos disponíveis
    ---
    tags:
      - Cursos
    responses:
      200:
        description: Lista de cursos
        schema:
          type: array
          items:
            $ref: '#/definitions/Course'
    """
    courses = Course.query.all()
    result = [CourseSchema(**c.to_dict()).model_dump() for c in courses]
    return jsonify(result)

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    """
    Obtém detalhes de um curso específico
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID do curso
    responses:
      200:
        description: Detalhes do curso
        schema:
          $ref: '#/definitions/Course'
      404:
        description: Curso não encontrado
    """

    course = Course.query.get(course_id)
    
    if course:
        result = CourseSchema(**course.to_dict()).model_dump()
        return jsonify(result)
    
    return jsonify({"error": "Curso não encontrado"}), 404

@courses_bp.route('/<int:course_id>/lessons', methods=['GET'])
def get_lessons_by_course(course_id):
    """
    Lista aulas de um curso específico
    ---
    tags:
      - Cursos
    parameters:
      - name: course_id
        in: path
        type: integer
        required: true
        description: ID do curso para buscar aulas
    responses:
      200:
        description: Lista de aulas do curso
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              order:
                type: integer
      404:
        description: Curso não encontrado
    """
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Curso não encontrado"}), 404
        
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()

    result = [LessonSchema(**l.to_dict()).model_dump() for l in lessons]
    return jsonify(result)