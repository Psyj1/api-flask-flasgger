from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Configuração do Swagger
    app.config['SWAGGER'] = {
        'title': 'Sacolas API',
        'uiversion': 3
    }
    Swagger(app)

    # Espaço reservado para registrar Blueprints depois

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)