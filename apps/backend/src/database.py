from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """
    Configura e inicializa o SQLAlchemy com o Flask app.
    Lê a DATABASE_URL das variáveis de ambiente.
    """
    import os

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL não configurada! "
            "Defina no arquivo .env (local) ou nas variáveis de ambiente (Supabase)."
        )

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)