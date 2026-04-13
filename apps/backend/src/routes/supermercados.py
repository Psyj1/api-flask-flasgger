from typing import Union, Tuple
from flask import Blueprint, jsonify, request, Response
from database import db
from models import Supermercado
from schemas.supermercado_schema import SupermercadoSchema

supermercados_bp = Blueprint('supermercados', __name__)


@supermercados_bp.route('/<int:supermercado_id>/materiais', methods=['GET'])
def get_materiais_by_supermercado(supermercado_id: int) -> Union[Response, Tuple[Response, int]]:
    """
    Lista os materiais de sacola disponíveis em um supermercado
    ---
    tags:
      - Supermercados
    parameters:
      - name: supermercado_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Lista de materiais disponíveis no supermercado
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              resistencia:
                type: integer
      404:
        description: Supermercado não encontrado
    """
    supermercado = Supermercado.query.get(supermercado_id)
    if not supermercado:
        return jsonify({"error": "Supermercado não encontrado"}), 404

    materiais = [
        {
            "id": m.id,
            "nome": m.nome,
            "resistencia": m.resistencia
        }
        for m in supermercado.materiais
    ]
    return jsonify(materiais)


@supermercados_bp.route('/', methods=['GET'])
def get_all_supermercados():
    """
    Lista todos os supermercados
    ---
    tags:
      - Supermercados
    responses:
      200:
        description: Lista de supermercados
        schema:
          type: array
          items:
            $ref: '#/definitions/Supermercado'
    """
    supermercados = Supermercado.query.all()
    result = [SupermercadoSchema(**s.to_dict()).model_dump() for s in supermercados]
    return jsonify(result)


@supermercados_bp.route('/<int:supermercado_id>', methods=['GET'])
def get_supermercado_by_id(supermercado_id):
    """
    Obtém detalhes de um supermercado específico
    ---
    tags:
      - Supermercados
    parameters:
      - name: supermercado_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do supermercado
        schema:
          $ref: '#/definitions/Supermercado'
      404:
        description: Supermercado não encontrado
    """
    supermercado = Supermercado.query.get(supermercado_id)
    if not supermercado:
        return jsonify({"error": "Supermercado não encontrado"}), 404
    
    result = SupermercadoSchema(**supermercado.to_dict()).model_dump()
    return jsonify(result)


@supermercados_bp.route('/', methods=['POST'])
def create_supermercado():
    """
    Cadastra um novo supermercado
    ---
    tags:
      - Supermercados
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            sacola_id:
              type: integer
            endereco:
              type: string
            nota:
              type: integer
            sacola_forte:
              type: boolean
    responses:
      201:
        description: Supermercado criado com sucesso
      400:
        description: Dados invalidos
    """
    data = request.json
    novo_supermercado = Supermercado(
        nome=data['nome'],
        sacola_id=data['sacola_id'],
        endereco=data.get('endereco'),
        nota=data.get('nota'),
        sacola_forte=data.get('sacola_forte', True)
    )
    db.session.add(novo_supermercado)
    db.session.commit()
    return jsonify(novo_supermercado.to_dict()), 201


@supermercados_bp.route('/<int:supermercado_id>', methods=['PUT'])
def update_supermercado(supermercado_id):
    """
    Atualiza um supermercado existente
    ---
    tags:
      - Supermercados
    parameters:
      - name: supermercado_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            sacola_id:
              type: integer
            endereco:
              type: string
            nota:
              type: integer
            sacola_forte:
              type: boolean
    responses:
      200:
        description: Supermercado atualizado
      404:
        description: Supermercado nao encontrado
    """
    supermercado = Supermercado.query.get(supermercado_id)
    if not supermercado:
        return jsonify({"error": "Supermercado nao encontrado"}), 404
    
    data = request.json
    supermercado.nome = data.get('nome', supermercado.nome)
    supermercado.sacola_id = data.get('sacola_id', supermercado.sacola_id)
    supermercado.endereco = data.get('endereco', supermercado.endereco)
    supermercado.nota = data.get('nota', supermercado.nota)
    supermercado.sacola_forte = data.get('sacola_forte', supermercado.sacola_forte)
    db.session.commit()
    return jsonify(supermercado.to_dict()), 200


@supermercados_bp.route('/<int:supermercado_id>', methods=['DELETE'])
def delete_supermercado(supermercado_id):
    """
    Remove um supermercado
    ---
    tags:
      - Supermercados
    parameters:
      - name: supermercado_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Supermercado removido
      404:
        description: Supermercado nao encontrado
    """
    supermercado = Supermercado.query.get(supermercado_id)
    if not supermercado:
        return jsonify({"error": "Supermercado nao encontrado"}), 404
    
    db.session.delete(supermercado)
    db.session.commit()
    return jsonify({}), 204