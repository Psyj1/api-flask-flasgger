from typing import Union, Tuple
from flask import Blueprint, jsonify, request, Response
from pydantic import ValidationError
from database import db
from models import Material, ResgateRegistro, ProgressoSupermercado, Usuario
from schemas.resgate_schema import (
    RegistrarResgateSchema,
    ResultadoResgateSchema,
    ResetarProgressoSchema,
)

resgates_bp = Blueprint('resgates', __name__)


@resgates_bp.route('/', methods=['GET'])
def get_all_resgates():
    """
    Lista todos os registros de resgate
    ---
    tags:
      - Resgates
    responses:
      200:
        description: Lista de resgates
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              usuario_id:
                type: integer
              material_id:
                type: integer
              foi_resgatado:
                type: boolean
              timestamp:
                type: string
    """
    resgates = ResgateRegistro.query.all()
    return jsonify([r.to_dict() for r in resgates])


@resgates_bp.route('/<int:resgate_id>', methods=['GET'])
def get_resgate_by_id(resgate_id):
    """
    Obtém detalhes de um resgate específico
    ---
    tags:
      - Resgates
    parameters:
      - name: resgate_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do resgate
        schema:
          type: object
          properties:
            id:
              type: integer
            usuario_id:
              type: integer
            material_id:
              type: integer
            foi_resgatado:
              type: boolean
            timestamp:
              type: string
      404:
        description: Resgate nao encontrado
    """
    resgate = ResgateRegistro.query.get(resgate_id)
    if not resgate:
        return jsonify({"error": "Resgate nao encontrado"}), 404
    return jsonify(resgate.to_dict())


@resgates_bp.route('/', methods=['POST'])
def registrar_resgate() -> Union[Response, Tuple[Response, int]]:
    """
    Registra o resgate de uma sacola
    ---
    tags:
      - Resgates
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/RegistrarResgate'
    responses:
      200:
        description: Resultado do resgate
        schema:
          $ref: '#/definitions/ResultadoResgate'
      400:
        description: Dados invalidos
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Material ou usuario nao encontrado
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        data = RegistrarResgateSchema(**request.json)
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    usuario_id = data.usuario_id
    material_id = data.material_id
    foi_resgatado = data.foi_resgatado

    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material nao encontrado"}), 404

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify({"error": "Usuario nao encontrado"}), 404

    registro = ResgateRegistro(
        usuario_id=usuario_id,
        material_id=material_id,
        foi_resgatado=foi_resgatado
    )
    db.session.add(registro)
    db.session.commit()

    supermercado_id = material.supermercado_id
    materiais_supermercado = Material.query.filter_by(supermercado_id=supermercado_id).all()

    todos_resgatados = True
    for m in materiais_supermercado:
        tem_resgate = ResgateRegistro.query.filter_by(
            usuario_id=usuario_id,
            material_id=m.id,
            foi_resgatado=True,
        ).first() is not None

        if not tem_resgate:
            todos_resgatados = False
            break

    if todos_resgatados:
        progresso = ProgressoSupermercado.query.filter_by(
            usuario_id=usuario_id, supermercado_id=supermercado_id
        ).first()

        if not progresso:
            progresso = ProgressoSupermercado(
                usuario_id=usuario_id,
                supermercado_id=supermercado_id,
                is_completed=True,
                completed_at=db.func.now(),
            )
            db.session.add(progresso)
        else:
            if not progresso.is_completed:
                progresso.is_completed = True
                progresso.completed_at = db.func.now()

        db.session.commit()

    result = ResultadoResgateSchema(
        foi_resgatado=foi_resgatado,
        message="Sacola resgatada!" if foi_resgatado else "Sacola nao resgatada.",
    ).model_dump()

    return jsonify(result)


@resgates_bp.route('/<int:resgate_id>', methods=['PUT'])
def update_resgate(resgate_id):
    """
    Atualiza um registro de resgate
    ---
    tags:
      - Resgates
    parameters:
      - name: resgate_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/RegistrarResgate'
    responses:
      200:
        description: Resgate atualizado
        schema:
          type: object
          properties:
            id:
              type: integer
            usuario_id:
              type: integer
            material_id:
              type: integer
            foi_resgatado:
              type: boolean
            timestamp:
              type: string
      404:
        description: Resgate nao encontrado
    """
    resgate = ResgateRegistro.query.get(resgate_id)
    if not resgate:
        return jsonify({"error": "Resgate nao encontrado"}), 404
    
    data = request.json
    resgate.usuario_id = data.get('usuario_id', resgate.usuario_id)
    resgate.material_id = data.get('material_id', resgate.material_id)
    resgate.foi_resgatado = data.get('foi_resgatado', resgate.foi_resgatado)
    db.session.commit()
    return jsonify(resgate.to_dict()), 200


@resgates_bp.route('/<int:resgate_id>', methods=['DELETE'])
def delete_resgate(resgate_id):
    """
    Remove um registro de resgate
    ---
    tags:
      - Resgates
    parameters:
      - name: resgate_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Resgate removido
      404:
        description: Resgate nao encontrado
    """
    resgate = ResgateRegistro.query.get(resgate_id)
    if not resgate:
        return jsonify({"error": "Resgate nao encontrado"}), 404
    
    db.session.delete(resgate)
    db.session.commit()
    return jsonify({}), 204


@resgates_bp.route('/reset', methods=['POST'])
def reset_progresso() -> Union[Response, Tuple[Response, int]]:
    """
    Reseta o progresso de um supermercado
    ---
    tags:
      - Resgates
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/ResetarProgresso'
    responses:
      200:
        description: Progresso resetado com sucesso
      400:
        description: Dados invalidos
        schema:
          $ref: '#/definitions/Error'
    """
    try:
        data = ResetarProgressoSchema(**request.json)
    except ValidationError as err:
        return jsonify({"errors": err.errors()}), 400

    usuario_id = data.usuario_id
    supermercado_id = data.supermercado_id

    materiais = Material.query.filter_by(supermercado_id=supermercado_id).all()
    material_ids = [m.id for m in materiais]

    if material_ids:
        ResgateRegistro.query.filter(
            ResgateRegistro.usuario_id == usuario_id,
            ResgateRegistro.material_id.in_(material_ids),
        ).delete(synchronize_session=False)

    ProgressoSupermercado.query.filter_by(
        usuario_id=usuario_id, supermercado_id=supermercado_id
    ).delete()

    db.session.commit()

    return jsonify({"message": "Progresso resetado com sucesso!"})