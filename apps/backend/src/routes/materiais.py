from flask import Blueprint, jsonify, request
from database import db
from models import Material
from schemas.material_schema import MaterialSchema

materiais_bp = Blueprint('materiais', __name__)


@materiais_bp.route('/', methods=['GET'])
def get_all_materiais():
    """
    Lista todos os materiais disponíveis
    ---
    tags:
      - Materiais
    responses:
      200:
        description: Lista de materiais
        schema:
          type: array
          items:
            $ref: '#/definitions/Material'
    """
    materiais = Material.query.all()
    result = [MaterialSchema(**m.to_dict()).model_dump() for m in materiais]
    return jsonify(result)


@materiais_bp.route('/<int:material_id>', methods=['GET'])
def get_material_details(material_id):
    """
    Obtém detalhes de um material de sacola
    ---
    tags:
      - Materiais
    parameters:
      - name: material_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detalhes do material
        schema:
          $ref: '#/definitions/Material'
      404:
        description: Material não encontrado
    """
    material = Material.query.get(material_id)
    if material:
        result = MaterialSchema(**material.to_dict()).model_dump()
        return jsonify(result)
    return jsonify({"error": "Material não encontrado"}), 404


@materiais_bp.route('/', methods=['POST'])
def create_material():
    """
    Cadastra um novo material
    ---
    tags:
      - Materiais
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            supermercado_id:
              type: integer
            descricao:
              type: string
            resistencia:
              type: integer
            biodegradavel:
              type: boolean
    responses:
      201:
        description: Material criado com sucesso
      400:
        description: Dados invalidos
    """
    data = request.json
    novo_material = Material(
        nome=data['nome'],
        supermercado_id=data['supermercado_id'],
        descricao=data.get('descricao'),
        resistencia=data.get('resistencia'),
        biodegradavel=data.get('biodegradavel', False)
    )
    db.session.add(novo_material)
    db.session.commit()
    result = MaterialSchema(**novo_material.to_dict()).model_dump()
    return jsonify(result), 201


@materiais_bp.route('/<int:material_id>', methods=['PUT'])
def update_material(material_id):
    """
    Atualiza um material existente
    ---
    tags:
      - Materiais
    parameters:
      - name: material_id
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
            supermercado_id:
              type: integer
            descricao:
              type: string
            resistencia:
              type: integer
            biodegradavel:
              type: boolean
    responses:
      200:
        description: Material atualizado
        schema:
          $ref: '#/definitions/Material'
      404:
        description: Material nao encontrado
    """
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material nao encontrado"}), 404
    
    data = request.json
    material.nome = data.get('nome', material.nome)
    material.supermercado_id = data.get('supermercado_id', material.supermercado_id)
    material.descricao = data.get('descricao', material.descricao)
    material.resistencia = data.get('resistencia', material.resistencia)
    material.biodegradavel = data.get('biodegradavel', material.biodegradavel)
    db.session.commit()
    result = MaterialSchema(**material.to_dict()).model_dump()
    return jsonify(result), 200


@materiais_bp.route('/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    """
    Remove um material
    ---
    tags:
      - Materiais
    parameters:
      - name: material_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Material removido
      404:
        description: Material nao encontrado
    """
    material = Material.query.get(material_id)
    if not material:
        return jsonify({"error": "Material nao encontrado"}), 404
    
    db.session.delete(material)
    db.session.commit()
    return jsonify({}), 204