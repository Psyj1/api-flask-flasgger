from typing import Union, Tuple
from flask import Blueprint, jsonify, Response
from routes.materiais import MATERIAIS_DB

supermercados_bp = Blueprint('supermercados', __name__)

# Dados mockados (depois vai pro banco)
SUPERMERCADOS_DB = [
    {
        "id": 1,
        "nome": "Carrefour",
        "endereco": "Av. Paulista, 1000",
        "nota": 7,
        "sacola_forte": True
    },
    {
        "id": 2,
        "nome": "Atacadão",
        "endereco": "Marginal Tietê, 500",
        "nota": 9,
        "sacola_forte": True
    },
    {
        "id": 3,
        "nome": "Pão de Açúcar",
        "endereco": "Rua Augusta, 200",
        "nota": 6,
        "sacola_forte": False
    },
    {
        "id": 4,
        "nome": "Mercadinho do Zé",
        "endereco": "Rua da Esquina, 10",
        "nota": 4,
        "sacola_forte": False
    }
]

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
    supermercado = next((s for s in SUPERMERCADOS_DB if s['id'] == supermercado_id), None)
    if not supermercado:
        return jsonify({"error": "Supermercado não encontrado"}), 404

    materiais = [
        {
            "id": m['id'], 
            "nome": m['nome'],
            "resistencia": m['resistencia']
        } 
        for m in MATERIAIS_DB if m['supermercado_id'] == supermercado_id
    ]
    return jsonify(materiais)