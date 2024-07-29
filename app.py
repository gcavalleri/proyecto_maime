from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session, app
from flask_sqlalchemy import SQLAlchemy
from backend.models import db, Usuario, Inventario, Producto, Cocina, Mazo, Carta
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos_usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_super_secreta'  # Clave secreta para sesiones



db.init_app(app)
with app.app_context():
    db.create_all()
    
#creo una lista de productos para cargar
def crear_productos():
    productos_para_cargar = [
        {'nombre': 'marroc'},{'nombre': 'bananina'},{'nombre': 'corazones'},{'nombre': 'licorita'}
    ]
    for producto_data in productos_para_cargar:
        producto = Producto(nombre=producto_data['nombre'])
        db.session.add(producto)

    db.session.commit()

#creo una lista de cocinas para cargar por usuario
def crear_cocinas(usuario_id):
    cocinas_cargar = [
        {'nombre': 'cocina1'}, {'nombre': 'cocina2'}, {'nombre': 'cocina3'}
    ]
    for cocina_data in cocinas_cargar:
        producto = Cocina(nombre=cocina_data['nombre'], usuario_id=usuario_id)
        db.session.add(producto)

    db.session.commit()

#creo las cartas con nombre y ruta de imagen ponele
def crear_cartas():
    cartas_cargar = [
        {'nombre': 'ricky vs flavio', 'imagen': 'carta1'}, {'nombre': 'ricky rolls', 'imagen': 'carta2'}, 
        {'nombre': 'ricky gym', 'imagen': 'carta3'}, {'nombre': 'ricky apagaste la luz', 'imagen': 'carta4'}, 
        {'nombre': 'ricky gritito', 'imagen': 'carta5'}, {'nombre': 'comandante ricky V', 'imagen': 'carta6'},
        {'nombre': 'ricky el rey', 'imagen': 'carta7'}, {'nombre': 'ricky santo', 'imagen': 'carta8'}, 
        {'nombre': 'ricky-wonka', 'imagen': 'carta9'}
    ]
    for carta_data in cartas_cargar:
        producto = Carta(nombre=carta_data['nombre'], imagen=carta_data['imagen'])
        db.session.add(producto)
    
    db.session.commit()

#con esta funcion lo que hago es actualizar los mazos de cartas una vez creado alguna
def actualizar_mazo_carta_nueva(nueva_carta):
    usuarios = Usuario.query.all()
    for usuario in usuarios:
        #verifica si el usuario ya tiene la carta en su mazo
        usuario_carta = Mazo.query.filter_by(usuario_id=usuario.id, carta_id=nueva_carta.id).first()
        if not usuario_carta:
            nueva_carta_mazo = Mazo(usuario_id=usuario.id, carta_id=nueva_carta.id, desbloqueado=False)
            db.session.add(nueva_carta_mazo)
    db.session.commit()    

@app.route('/')
def index():
    #pagina principal para que inicie sesion
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        nombre = request.form['nombre']
        contrasenia = request.form['contrasenia']

        #verifica si el usuario ya existe
        if Usuario.query.filter_by(email=email).first():
            flash('El usuario ya está registrado.', 'error')
            return redirect(url_for('registro'))

        #de no existir crea un nuevo usuario
        nuevo_usuario = Usuario(email=email, nombre=nombre, contrasenia=contrasenia)
        db.session.add(nuevo_usuario)
        db.session.commit()

        productos = Producto.query.all()
        if not productos:
            crear_productos()

        productos = Producto.query.all()
        for producto in productos:
            inventario = Inventario(usuario_id=nuevo_usuario.id, producto_id=producto.id, cantidad=0)
            db.session.add(inventario)

        crear_cocinas(nuevo_usuario.id)

        cartas = Carta.query.all()
        if not cartas:
            crear_cartas()

        cartas = Carta.query.all()
        for carta in cartas:
            mazo = Mazo(usuario_id=nuevo_usuario.id, carta_id=carta.id, desbloqueado=False)
            db.session.add(mazo)
        
        db.session.commit()
        #carga los productos, junto con las cartas y las respectivas cocinas

        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('index'))

    return render_template('registro.html')

#login: si la ocntrasenia y el usuario coinciden iniciara sesion y lo mandara
#a su pagina de usuario de lo contrario reintentara
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasenia = request.form['contrasenia']

        usuario = Usuario.query.filter_by(nombre=nombre, contrasenia=contrasenia).first()

        if usuario and usuario.contrasenia == contrasenia:
            session['usuario_id'] = usuario.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('pagina_usuario'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

#cierra sesion
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Sesión cerrada exitosamente.', 'info')
    return redirect(url_for('index'))

#la pagina del usuario, aca se mostrara algunos de los datos del usuario
@app.route('/usuario')
def pagina_usuario():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para ver esta página.', 'error')
        return redirect(url_for('login'))
    
    usuario = Usuario.query.get(session['usuario_id'])
    inventarios = usuario.inventarios
    
    
    #se obtienen los detalles del producto en el inventario del usuario
    productos = []
    for inventario in inventarios:
        producto = Producto.query.get(inventario.producto_id)
        productos.append({
            'nombre': producto.nombre,
            'cantidad': inventario.cantidad,
        })

    #cocinas conectas con el usuario
    cocinas = usuario.cocinas

    #informacion del usuario relevante para la pagina
    plata_usuario = usuario.plata

    #las cartas que posea los usuarios
    cartas = Mazo.query.filter_by(usuario_id = usuario.id).all()
    cartas_data = []
    for carta in cartas:
        carta_data = Carta.query.get(carta.carta_id)
        cartas_data.append({
            'nombre': carta_data.nombre,
            'imagen': carta_data.imagen,
            'desbloqueado': carta.desbloqueado
        })

    #se devuelve a un html junto la informacion relacionada con el usuario
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('index.html', usuario=usuario, productos=productos, cocinas=cocinas, plata=plata_usuario, cartas=cartas_data)

#obtiene todos los usuarios en lista
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    usuarios_json = [{'id': usuario.id, 'email': usuario.email, 'nombre': usuario.nombre, 'contrasenia': usuario.contrasenia} for usuario in usuarios]
    return jsonify(usuarios_json)

#funcion simplre que dependiendo el producto suma el producto al inventario
@app.route('/cocinar', methods=['POST'])
def cocinar():
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'message': 'Debes iniciar sesión para cocinar.'})

    user_id = session['usuario_id']
    producto_id = request.form.get('producto_id')

    producto = Producto.query.get(producto_id)
    if not producto:
        return jsonify({'success': False, 'message': 'Producto no encontrado.'})

    inventario = Inventario.query.filter_by(usuario_id=user_id, producto_id=producto_id).first()
    if inventario:
        inventario.cantidad += 1
    else:
        inventario = Inventario(usuario_id=user_id, producto_id=producto_id, cantidad=1)
        db.session.add(inventario)

    db.session.commit()
    return jsonify({'success': True, 'message': f'Producto {producto.nombre} añadido al inventario.'})

#funcion simple con los pedidos ya cargados para realizar missiones a cambio de plata
@app.route('/misiones/<mision_id>', methods=['POST'])
def misiones(mision_id):
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'message': 'No estás autenticado.'})

    usuario_id = session['usuario_id']
    usuario = Usuario.query.get(usuario_id)
    
    #se definio las misiones y sus requisitos
    misiones_requerimientos = {
        'mission1': {'productos': {1: 3, 2: 2}, 'plata': 50},
        'mission2': {'productos': {3: 1, 4: 2}, 'plata': 30},
        'mission3': {'productos': {1: 5, 4: 1}, 'plata': 70},
        'mission4': {'productos': {2: 3, 3: 4}, 'plata': 60}
    }
    
    requisitos = misiones_requerimientos[mision_id]
    productos_requeridos = requisitos['productos']
    plata_ganada = requisitos['plata']

    #verifica si el usuario tiene los productos necesarios
    for producto_id, cantidad_requerida in productos_requeridos.items():
        inventario = Inventario.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
        if not inventario or inventario.cantidad < cantidad_requerida:
            return jsonify({'success': False, 'message': 'No tienes los productos necesarios para esta misión.'})

    #si tiene todos los productos necesarios, actualiza el inventario y añade la plata
    for producto_id, cantidad_requerida in productos_requeridos.items():
        inventario = Inventario.query.filter_by(usuario_id=usuario_id, producto_id=producto_id).first()
        inventario.cantidad -= cantidad_requerida
        db.session.add(inventario)

    usuario.plata += plata_ganada
    db.session.commit()

    return jsonify({'success': True, 'message': f'Misión completada. Ganaste {plata_ganada} de plata.'})

#devuelve una fotocard de ricky si cumple con los requisitos
@app.route('/gatcha', methods=['POST'])
def gatcha():
    if 'usuario_id' not in session:
        return jsonify({'error': 'Debes iniciar sesión.'}), 401
    
    usuario = Usuario.query.get(session['usuario_id'])
    costo_gatcha = 40  #define el costo de una tirada gacha

    if usuario.plata < costo_gatcha:
        return jsonify({'error': 'No tienes suficiente plata.'}), 400

    usuario.plata -= costo_gatcha

    #obtengo todas las cartas disponibles que el usuario no haya desbloqueado
    cartas_no_desbloqueadas = Carta.query.outerjoin(Mazo, (Carta.id == Mazo.carta_id) & (Mazo.usuario_id == usuario.id))\
        .filter((Mazo.id.is_(None)) | (Mazo.desbloqueado == False)).all()

    if not cartas_no_desbloqueadas:
        return jsonify({'error': 'No hay cartas disponibles para desbloquear.'}), 400

    #seleccionar una carta aleatoria
    carta_ganada = random.choice(cartas_no_desbloqueadas)

    #verificar si el usuario ya tiene la carta
    usuario_carta = Mazo.query.filter_by(usuario_id=usuario.id, carta_id=carta_ganada.id).first()
    if usuario_carta:
        usuario_carta.desbloqueado = True
    else:
        nueva_carta = Mazo(usuario_id=usuario.id, carta_id=carta_ganada.id, desbloqueado=True)
        db.session.add(nueva_carta)

    db.session.commit()

    return jsonify({
        'success': 'Has ganado una carta!',
        'carta': {
            'nombre': carta_ganada.nombre,
            'imagen': carta_ganada.imagen
        },
        'plata_restante': usuario.plata
    })

@app.route('/cartas/<int:carta_id>', methods=['DELETE'])
def eliminar_carta(carta_id):
    carta = Carta.query.get(carta_id)
    if not carta:
        return jsonify({'error': 'Carta no encontrada.'}), 404
    
    Mazo.query.filter_by(carta_id=carta_id).delete()

    db.session.delete(carta)
    db.session.commit()
    
    return jsonify({'success': 'Carta eliminada exitosamente.'}), 200

@app.route('/cartas', methods=['POST'])
def agregar_carta():
    data = request.get_json()
    nombre = data.get('nombre')
    imagen = data.get('imagen')
    
    if not nombre or not imagen:
        return jsonify({'error': 'Faltan datos.'}), 400
    
    nueva_carta = Carta(nombre=nombre, imagen=imagen)
    db.session.add(nueva_carta)
    db.session.commit()
    
    actualizar_mazo_carta_nueva(nueva_carta)

    return jsonify({'success': 'Carta agregada exitosamente.'}), 201

@app.route('/cartas/<int:carta_id>', methods=['PUT'])
def actualizar_carta(carta_id):
    carta = Carta.query.get(carta_id)
    if not carta:
        return jsonify({'error': 'Carta no encontrada.'}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    imagen = data.get('imagen')

    if not nombre or not imagen:
        return jsonify({'error': 'Faltan datos.'}), 400

    carta.nombre = nombre
    carta.imagen = imagen
    db.session.commit()

    return jsonify({'success': 'Carta actualizada exitosamente.'}), 200

@app.route('/cartas', methods=['GET'])
def obtener_todas_las_cartas():
    cartas = Carta.query.all()
    cartas_data = [{'id': carta.id, 'nombre': carta.nombre, 'imagen': carta.imagen} for carta in cartas]

    return jsonify(cartas_data), 200

if __name__ == '__main__':
    app.run(debug = True)