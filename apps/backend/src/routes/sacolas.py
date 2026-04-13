from flask import Blueprint, jsonify, request
from database import db
from schemas.sacola_schema import SacolaSchema
from schemas.supermercado_schema import SupermercadoSchema
from models import Sacola, Supermercado

sacolas_bp = Blueprint('sacolas', __name__)

@sacolas_bp.route('/', methods=['GET'])
def get_sacolas():
    """
    Lista todas as sacolas disponíveis no acervo
    ---
    tags:
      - Sacolas
    responses:
      200:
        description: Lista de sacolas
        schema:
          type: array
          items:
            $ref: '#/definitions/Sacola'
    """
    sacolas = Sacola.query.all()
    result = [SacolaSchema(**s.to_dict()).model_dump() for s in sacolas]
    return jsonify(result)


@sacolas_bp.route('/<int:sacola_id>', methods=['GET'])
def get_sacola_by_id(sacola_id):
    """
    Obtém detalhes de uma sacola específica
    ---
    tags:
      - Sacolas
    parameters:
      - name: sacola_id
        in: path
        type: integer
        required: true
        description: ID da sacola
    responses:
      200:
        description: Detalhes da sacola
        schema:
          $ref: '#/definitions/Sacola'
      404:
        description: Sacola não encontrada
    """
    sacola = Sacola.query.get(sacola_id)
    
    if sacola:
        result = SacolaSchema(**sacola.to_dict()).model_dump()
        return jsonify(result)
    
    return jsonify({"error": "Sacola não encontrada"}), 404


@sacolas_bp.route('/<int:sacola_id>/supermercados', methods=['GET'])
def get_supermercados_by_sacola(sacola_id):
    """
    Lista supermercados que utilizam este tipo de sacola
    ---
    tags:
      - Sacolas
    parameters:
      - name: sacola_id
        in: path
        type: integer
        required: true
        description: ID da sacola para buscar os supermercados que a utilizam
    responses:
      200:
        description: Lista de supermercados que usam esta sacola
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              nota:
                type: integer
      404:
        description: Sacola não encontrada
    """
    sacola = Sacola.query.get(sacola_id)
    if not sacola:
        return jsonify({"error": "Sacola não encontrada"}), 404
        
    supermercados = Supermercado.query.filter_by(sacola_id=sacola_id).order_by(Supermercado.nome).all()

    result = [SupermercadoSchema(**s.to_dict()).model_dump() for s in supermercados]
    return jsonify(result)


@sacolas_bp.route('/', methods=['POST'])
def create_sacola():
    """
    Cadastra uma nova sacola
    ---
    tags:
      - Sacolas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            descricao:
              type: string
            cor:
              type: string
            resistencia:
              type: integer
            rasgada:
              type: boolean
    responses:
      201:
        description: Sacola criada com sucesso
      400:
        description: Dados invalidos
    """
    data = request.json
    nova_sacola = Sacola(
        nome=data['nome'],
        descricao=data.get('descricao'),
        cor=data.get('cor'),
        resistencia=data.get('resistencia'),
        rasgada=data.get('rasgada', False)
    )
    db.session.add(nova_sacola)
    db.session.commit()
    return jsonify(nova_sacola.to_dict()), 201


@sacolas_bp.route('/<int:sacola_id>', methods=['PUT'])
def update_sacola(sacola_id):
    """
    Atualiza uma sacola existente
    ---
    tags:
      - Sacolas
    parameters:
      - name: sacola_id
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
            descricao:
              type: string
            cor:
              type: string
            resistencia:
              type: integer
            rasgada:
              type: boolean
    responses:
      200:
        description: Sacola atualizada
      404:
        description: Sacola nao encontrada
    """
    sacola = Sacola.query.get(sacola_id)
    if not sacola:
        return jsonify({"error": "Sacola nao encontrada"}), 404
    
    data = request.json
    sacola.nome = data.get('nome', sacola.nome)
    sacola.descricao = data.get('descricao', sacola.descricao)
    sacola.cor = data.get('cor', sacola.cor)
    sacola.resistencia = data.get('resistencia', sacola.resistencia)
    sacola.rasgada = data.get('rasgada', sacola.rasgada)
    db.session.commit()
    return jsonify(sacola.to_dict()), 200


@sacolas_bp.route('/<int:sacola_id>', methods=['DELETE'])
def delete_sacola(sacola_id):
    """
    Remove uma sacola
    ---
    tags:
      - Sacolas
    parameters:
      - name: sacola_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Sacola removida
      404:
        description: Sacola nao encontrada
    """
    sacola = Sacola.query.get(sacola_id)
    if not sacola:
        return jsonify({"error": "Sacola nao encontrada"}), 404
    
    db.session.delete(sacola)
    db.session.commit()
    return jsonify({}), 204