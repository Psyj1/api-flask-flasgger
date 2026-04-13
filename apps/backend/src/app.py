from flask import Flask
from flasgger import Swagger
from dotenv import load_dotenv
import os

from routes.sacolas import sacolas_bp
from routes.supermercados import supermercados_bp
from routes.materiais import materiais_bp
from routes.resgates import resgates_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    from database import init_db
    init_db(app)

    from schemas.sacola_schema import SacolaSchema
    from schemas.supermercado_schema import SupermercadoSchema
    from schemas.material_schema import MaterialSchema, MaterialIdSchema
    from schemas.resgate_schema import (
        RegistrarResgateSchema,
        ResultadoResgateSchema,
        ResetarProgressoSchema,
        ProgressoResponseSchema,
        HistoricoUsuarioSchema
    )

    db_url = os.getenv('DATABASE_URL', '')
    env_label = 'Supabase' if 'supabase' in db_url else 'Local (Docker)'

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": f"Acervo de Sacolas API — {env_label}",
            "description": "API para gerenciamento de sacolas de supermercado",
            "version": "1.0.0"
        },
        "tags": [
            {"name": "Sacolas"},
            {"name": "Supermercados"},
            {"name": "Materiais"},
            {"name": "Resgates"}
        ],
        "definitions": {
            "Sacola": SacolaSchema.model_json_schema(),
            "Supermercado": SupermercadoSchema.model_json_schema(),
            "Material": MaterialSchema.model_json_schema(),
            "MaterialId": MaterialIdSchema.model_json_schema(),
            "RegistrarResgate": RegistrarResgateSchema.model_json_schema(),
            "ResultadoResgate": ResultadoResgateSchema.model_json_schema(),
            "ResetarProgresso": ResetarProgressoSchema.model_json_schema(),
            "ProgressoResponse": ProgressoResponseSchema.model_json_schema(),
            "HistoricoUsuario": HistoricoUsuarioSchema.model_json_schema(),
            "Error": {
                "type": "object",
                "properties": {"error": {"type": "string"}}
            }
        }
    }

    app.config['SWAGGER'] = {
        'title': f'Acervo de Sacolas API — {env_label}',
        'uiversion': 3,
        'description': f'API para gerenciamento de sacolas. Ambiente: **{env_label}**',
        'specs_route': '/apidocs/'
    }

    Swagger(app, template=swagger_template)

    app.register_blueprint(sacolas_bp, url_prefix='/api/sacolas')
    app.register_blueprint(supermercados_bp, url_prefix='/api/supermercados')
    app.register_blueprint(materiais_bp, url_prefix='/api/materiais')
    app.register_blueprint(resgates_bp, url_prefix='/api/resgates')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)