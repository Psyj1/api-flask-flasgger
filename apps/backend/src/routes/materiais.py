from flask import Blueprint, jsonify

materiais_bp = Blueprint('materiais', __name__)

MATERIAIS_DB = [
    {
        "id": 1,
        "supermercado_id": 1,
        "nome": "Plástico Comum",
        "descricao": "Aquela sacola fina que rasga no primeiro quilo",
        "resistencia": 2,
        "biodegradavel": False
    },
    {
        "id": 2,
        "supermercado_id": 1,
        "nome": "Plástico Reforçado",
        "descricao": "A sacola resistente que vira lixeira de banheiro",
        "resistencia": 8,
        "biodegradavel": False
    },
    {
        "id": 3,
        "supermercado_id": 2,
        "nome": "Papel",
        "descricao": "Ecologicamente correta, mas desmancha na chuva",
        "resistencia": 3,
        "biodegradavel": True
    },
    {
        "id": 4,
        "supermercado_id": 3,
        "nome": "TNT",
        "descricao": "A chique que você paga 2 reais e nunca usa",
        "resistencia": 9,
        "biodegradavel": False
    }
]

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
          type: object
          properties:
            id:
              type: integer
            supermercado_id:
              type: integer
            nome:
              type: string
            descricao:
              type: string
            resistencia:
              type: integer
            biodegradavel:
              type: boolean
      404:
        description: Material não encontrado
    """
    material = next((m for m in MATERIAIS_DB if m['id'] == material_id), None)
    if material:
        return jsonify(material)
    return jsonify({"error": "Material não encontrado"}), 404