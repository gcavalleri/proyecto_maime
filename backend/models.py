from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    contrasenia = db.Column(db.String(130), nullable=False)  
    plata = db.Column(db.Integer, default=100)
    inventarios = db.relationship('Inventario', backref='usuario', lazy=True)
    cocinas = db.relationship('Cocina', backref='usuario', lazy=True)
    cartas = db.relationship('Mazo', backref='usuario', lazy=True)


class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False) 

class Inventario(db.Model):
    __tablename__ = 'inventario'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    producto = db.relationship('Producto', backref='inventarios', lazy=True)

class Cocina(db.Model):
    __tablename__ = 'cocina'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto = db.relationship('Producto', backref='cocinas', lazy=True)

class Carta(db.Model):
    __tablename__ = 'carta'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    imagen = db.Column(db.String(80), nullable=False)

class Mazo(db.Model):
    __tablename__ = 'mazo'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    carta_id = db.Column(db.Integer, db.ForeignKey('carta.id'), nullable=False)
    desbloqueado = db.Column(db.Boolean, default=False, nullable=False)
    carta = db.relationship('Carta', backref='usuario_cartas', lazy=True)