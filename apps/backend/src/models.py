from database import db


class Sacola(db.Model):
    __tablename__ = 'sacolas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String)
    cor = db.Column(db.String)
    resistencia = db.Column(db.Integer)
    rasgada = db.Column(db.Boolean, default=False)

    supermercados = db.relationship('Supermercado', backref='sacola', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'cor': self.cor,
            'resistencia': self.resistencia,
            'rasgada': self.rasgada,
            'supermercado_id': None
        }


class Supermercado(db.Model):
    __tablename__ = 'supermercados'

    id = db.Column(db.Integer, primary_key=True)
    sacola_id = db.Column(db.Integer, db.ForeignKey('sacolas.id'), nullable=False)
    nome = db.Column(db.String, nullable=False)
    endereco = db.Column(db.String)
    nota = db.Column(db.Integer)
    sacola_forte = db.Column(db.Boolean, default=True)

    materiais = db.relationship('Material', backref='supermercado', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'sacola_id': self.sacola_id,
            'nome': self.nome,
            'endereco': self.endereco,
            'nota': self.nota,
            'sacola_forte': self.sacola_forte,
        }


class Material(db.Model):
    __tablename__ = 'materiais'

    id = db.Column(db.Integer, primary_key=True)
    supermercado_id = db.Column(db.Integer, db.ForeignKey('supermercados.id'), nullable=False)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String)
    resistencia = db.Column(db.Integer)
    biodegradavel = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'supermercado_id': self.supermercado_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'resistencia': self.resistencia,
            'biodegradavel': self.biodegradavel,
        }
    
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    resgates = db.relationship('ResgateRegistro', backref='usuario', lazy=True)
    progresso = db.relationship('ProgressoSupermercado', backref='usuario', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }


class ResgateRegistro(db.Model):
    __tablename__ = 'resgates_registros'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materiais.id'), nullable=False)
    foi_resgatado = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'material_id': self.material_id,
            'foi_resgatado': self.foi_resgatado,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
        }


class ProgressoSupermercado(db.Model):
    __tablename__ = 'progresso_supermercados'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    supermercado_id = db.Column(db.Integer, db.ForeignKey('supermercados.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'supermercado_id': self.supermercado_id,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }