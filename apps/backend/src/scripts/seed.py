import sys
import os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from database import db
from models import Sacola, Supermercado, Material, Usuario


SACOLAS = [
    {
        "id": 1,
        "nome": "Sacola Verde Reforcada",
        "descricao": "Sacola resistente do Carrefour",
        "cor": "verde",
        "resistencia": 8,
        "rasgada": False,
    },
    {
        "id": 2,
        "nome": "Sacola Preta do Atacadao",
        "descricao": "Forte e escura",
        "cor": "preta",
        "resistencia": 9,
        "rasgada": False,
    },
    {
        "id": 3,
        "nome": "Sacola de Papel",
        "descricao": "Ecologica mas fraca",
        "cor": "marrom",
        "resistencia": 3,
        "rasgada": False,
    },
]

SUPERMERCADOS = [
    {"id": 1, "sacola_id": 1, "nome": "Carrefour",
     "endereco": "Av. Paulista, 1000", "nota": 7, "sacola_forte": True},
    {"id": 2, "sacola_id": 2, "nome": "Atacadao",
     "endereco": "Marginal Tiete, 500", "nota": 9, "sacola_forte": True},
    {"id": 3, "sacola_id": 3, "nome": "Pao de Acucar",
     "endereco": "Rua Augusta, 200", "nota": 6, "sacola_forte": False},
]

MATERIAIS = [
    {
        "id": 1,
        "supermercado_id": 1,
        "nome": "Plastico Comum",
        "descricao": "Sacola fina que rasga facil",
        "resistencia": 2,
        "biodegradavel": False,
    },
    {
        "id": 2,
        "supermercado_id": 1,
        "nome": "Plastico Reforcado",
        "descricao": "Resiste ate 10kg",
        "resistencia": 8,
        "biodegradavel": False,
    },
    {
        "id": 3,
        "supermercado_id": 2,
        "nome": "Papel Kraft",
        "descricao": "Biodegradavel mas nao pode molhar",
        "resistencia": 3,
        "biodegradavel": True,
    },
    {
        "id": 4,
        "supermercado_id": 3,
        "nome": "TNT",
        "descricao": "Sacola chique de 2 reais",
        "resistencia": 7,
        "biodegradavel": False,
    },
]

USUARIOS = [
    {"id": 1, "username": "aluno_teste"},
    {"id": 2, "username": "aluno_02"},
]


def seed():
    app = create_app()

    with app.app_context():
        if Sacola.query.first():
            print("Banco ja possui dados. Pulando seed.")
            return

        print("Populando banco de dados...")

        for s in SACOLAS:
            db.session.add(Sacola(**s))
        print(f"  {len(SACOLAS)} sacolas inseridas")

        for s in SUPERMERCADOS:
            db.session.add(Supermercado(**s))
        print(f"  {len(SUPERMERCADOS)} supermercados inseridos")

        for m in MATERIAIS:
            db.session.add(Material(**m))
        print(f"  {len(MATERIAIS)} materiais inseridos")

        for u in USUARIOS:
            db.session.add(Usuario(**u))
        print(f"  {len(USUARIOS)} usuarios inseridos")

        db.session.commit()
        print("Seed concluido com sucesso!")


if __name__ == '__main__':
    seed()