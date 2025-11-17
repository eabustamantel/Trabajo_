from flask import Flask, request, jsonify, send_from_directory, redirect, session
from flask_cors import CORS
from backend.models import (
    initialize_tables,
    get_clientes, get_cliente_by_id, create_cliente, update_cliente, delete_cliente,
    get_inventarios, get_inventario_by_id, create_inventario, update_inventario, delete_inventario,
    get_vehiculos, get_vehiculo_by_id, create_vehiculo, update_vehiculo, delete_vehiculo,
    get_ordenes, get_orden_by_id, create_orden, update_orden, delete_orden,
    get_empleados, get_empleado_by_id, create_empleado, update_empleado, delete_empleado,
    get_proveedores, get_proveedor_by_id, create_proveedor, update_proveedor, delete_proveedor,
    get_admin_by_credentials, create_admin,
    supabase
)
from backend.config import Config
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
from io import BytesIO
import datetime
import os
import hashlib

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
CORS(app)

@app.route('/')
def index():
    if 'logged_in' in session:
        return send_from_directory('../frontend', 'index.html')
    else:
        return redirect('/login')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# CRUD for Clientes
@app.route('/api/clientes', methods=['GET'])
def api_get_clientes():
    try:
        clientes = get_clientes()  # esta es la función importada desde models
        return jsonify(clientes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clientes', methods=['POST'])
def create_cliente_endpoint():
    try:
        data = request.get_json()

        # Check for existing client by email or telefono
        existing_clientes = supabase.table('clientes').select('*').or_(
            f"email.eq.{data.get('email')},telefono.eq.{data.get('telefono')}"
        ).execute()

        if existing_clientes.data:
            return jsonify({'error': '⚠️ El cliente ya existe. No se puede duplicar el registro.'}), 409

        cliente = create_cliente(data)
        return jsonify({'message': 'Cliente creado', 'id': cliente['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['GET'])
def get_cliente_endpoint(id):
    try:
        cliente = get_cliente_by_id(id)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        return jsonify(cliente)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['PUT'])
def update_cliente_endpoint(id):
    try:
        data = request.get_json()
        cliente = update_cliente(id, data)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        return jsonify({'message': 'Cliente actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def delete_cliente_endpoint(id):
    try:
        cliente = delete_cliente(id)
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        return jsonify({'message': 'Cliente eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD for Inventario
@app.route('/api/inventarios', methods=['GET'])
def get_inventario():
    try:
        items = get_inventarios()
        return jsonify(items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventarios', methods=['POST'])
def create_inventario_endpoint():
    try:
        data = request.get_json()
        item = create_inventario(data)
        return jsonify({'message': 'Item creado', 'id': item['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventarios/<int:id>', methods=['GET'])
def get_inventario_item_endpoint(id):
    try:
        item = get_inventario_by_id(id)
        if not item:
            return jsonify({'error': 'Item no encontrado'}), 404
        return jsonify(item)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventarios/<int:id>', methods=['PUT'])
def update_inventario_endpoint(id):
    try:
        data = request.get_json()
        item = update_inventario(id, data)
        if not item:
            return jsonify({'error': 'Item no encontrado'}), 404
        return jsonify({'message': 'Item actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/inventarios/<int:id>', methods=['DELETE'])
def delete_inventario_endpoint(id):
    try:
        item = delete_inventario(id)
        if not item:
            return jsonify({'error': 'Item no encontrado'}), 404
        return jsonify({'message': 'Item eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD for Vehiculos
@app.route('/api/vehiculos', methods=['GET'])
def api_get_vehiculos():
    try:
        vehiculos = get_vehiculos()
        return jsonify(vehiculos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehiculos', methods=['POST'])
def create_vehiculo_endpoint():
    try:
        data = request.get_json()
        vehiculo = create_vehiculo(data)
        return jsonify({'message': 'Vehículo creado', 'id': vehiculo['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    try:
        vehiculo = get_vehiculo_by_id(id)
        if not vehiculo:
            return jsonify({'error': 'Vehículo no encontrado'}), 404
        return jsonify(vehiculo)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehiculos/<int:id>', methods=['PUT'])
def update_vehiculo(id):
    try:
        data = request.get_json()
        vehiculo = update_vehiculo(id, data)
        if not vehiculo:
            return jsonify({'error': 'Vehículo no encontrado'}), 404
        return jsonify({'message': 'Vehículo actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vehiculos/<int:id>', methods=['DELETE'])
def delete_vehiculo(id):
    try:
        vehiculo = delete_vehiculo(id)
        if not vehiculo:
            return jsonify({'error': 'Vehículo no encontrado'}), 404
        return jsonify({'message': 'Vehículo eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD for Ordenes
@app.route('/api/ordenes', methods=['GET'])
def get_ordenes_endpoint():
    try:
        ordenes = get_ordenes()
        return jsonify(ordenes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordenes/<int:id>', methods=['GET'])
def get_orden(id):
    try:
        orden = get_orden_by_id(id)
        if not orden:
            return jsonify({'error': 'Orden no encontrada'}), 404
        return jsonify(orden)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordenes', methods=['POST'])
def create_orden_endpoint():
    try:
        data = request.get_json()
        orden = create_orden(data)
        if not orden:
            return jsonify({'error': 'Failed to create orden'}), 500
        return jsonify({'message': 'Orden creada', 'id': orden['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordenes/<int:id>', methods=['PUT'])
def update_orden_endpoint(id):
    try:
        data = request.get_json()
        orden = update_orden(id, data)
        if not orden:
            return jsonify({'error': 'Orden no encontrada'}), 404
        return jsonify({'message': 'Orden actualizada'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ordenes/<int:id>', methods=['DELETE'])
def delete_orden(id):
    try:
        orden = delete_orden(id)
        if not orden:
            return jsonify({'error': 'Orden no encontrada'}), 404
        return jsonify({'message': 'Orden eliminada'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD for Empleados
@app.route('/api/empleados', methods=['GET'])
def get_empleados_endpoint():
    try:
        empleados = get_empleados()
        return jsonify(empleados)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados/<int:id>', methods=['GET'])
def get_empleado(id):
    try:
        empleado = get_empleado_by_id(id)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify(empleado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados', methods=['POST'])
def create_empleado_endpoint():
    try:
        data = request.get_json()
        empleado = create_empleado(data)
        return jsonify({'message': 'Empleado creado', 'id': empleado['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados/<int:id>', methods=['PUT'])
def update_empleado_endpoint(id):
    try:
        data = request.get_json()
        empleado = update_empleado(id, data)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify({'message': 'Empleado actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/empleados/<int:id>', methods=['DELETE'])
def delete_empleado(id):
    try:
        empleado = delete_empleado(id)
        if not empleado:
            return jsonify({'error': 'Empleado no encontrado'}), 404
        return jsonify({'message': 'Empleado eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD for Proveedores
@app.route('/api/proveedores', methods=['GET'])
def get_proveedores_endpoint():
    try:
        proveedores = get_proveedores()
        return jsonify(proveedores)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/<int:id>', methods=['GET'])
def get_proveedor(id):
    try:
        proveedor = get_proveedor_by_id(id)
        if not proveedor:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
        return jsonify(proveedor)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores', methods=['POST'])
def create_proveedor_endpoint():
    try:
        data = request.get_json()
        proveedor = create_proveedor(data)
        return jsonify({'message': 'Proveedor creado', 'id': proveedor['id']}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/<int:id>', methods=['PUT'])
def update_proveedor_endpoint(id):
    try:
        data = request.get_json()
        proveedor = update_proveedor(id, data)
        if not proveedor:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
        return jsonify({'message': 'Proveedor actualizado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proveedores/<int:id>', methods=['DELETE'])
def delete_proveedor(id):
    try:
        proveedor = delete_proveedor(id)
        if not proveedor:
            return jsonify({'error': 'Proveedor no encontrado'}), 404
        return jsonify({'message': 'Proveedor eliminado'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PDF Generation endpoints
@app.route('/api/pdf/<entity>', methods=['GET'])
def generate_pdf(entity):
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )

    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'img', 'logo.jpg')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2*inch, height=1*inch)
        elements.append(logo)
        elements.append(Spacer(1, 12))

    # Header
    header = Paragraph("Taller Valenciano Guayaquil 2025", title_style)
    elements.append(header)
    elements.append(Spacer(1, 12))

    # Entity-specific data and table headers
    if entity == 'clientes':
        data = get_clientes()
        headers = ['ID', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Dirección']
        table_data = [headers] + [[d['id'], d['nombre'], d['apellido'], d['telefono'], d['email'], d['direccion']] for d in data]
        title = "Reporte de Clientes"

    elif entity == 'inventario':
        data = get_inventarios()
        headers = ['ID', 'Nombre', 'Descripción', 'Cantidad', 'Precio', 'Categoría']
        table_data = [headers] + [[d['id'], d['nombre'], d['descripcion'], d['cantidad'], f"${d['precio']:.2f}", d['categoria']] for d in data]
        title = "Reporte de Inventario"

    elif entity == 'ordenes':
        data = get_ordenes()
        headers = ['ID', 'Descripción', 'Fecha Creación', 'Estado', 'Cliente ID', 'Vehículo ID']
        table_data = [headers] + [[d['id'], d['descripcion'], d['fecha_creacion'], d['estado'], d['cliente_id'], d['vehiculo_id']] for d in data]
        title = "Reporte de Órdenes"

    elif entity == 'empleados':
        data = get_empleados()
        headers = ['ID', 'Nombre', 'Apellido', 'Puesto', 'Teléfono', 'Email']
        table_data = [headers] + [[d['id'], d['nombre'], d['apellido'], d['puesto'], d['telefono'], d['email']] for d in data]
        title = "Reporte de Empleados"

    elif entity == 'proveedores':
        data = get_proveedores()
        headers = ['ID', 'Nombre', 'Contacto', 'Teléfono', 'Email', 'Dirección']
        table_data = [headers] + [[d['id'], d['nombre'], d['contacto'], d['telefono'], d['email'], d['direccion']] for d in data]
        title = "Reporte de Proveedores"

    else:
        return jsonify({'error': 'Entidad no válida'}), 400

    # Title
    title_para = Paragraph(title, styles['Heading2'])
    elements.append(title_para)
    elements.append(Spacer(1, 12))

    # Create the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Footer with generation date
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1
    )
    footer = Paragraph(f"Generado el {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", footer_style)
    elements.append(Spacer(1, 24))
    elements.append(footer)

    # Build the PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and return it
    buffer.seek(0)
    return buffer.getvalue(), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename={entity}_reporte.pdf'
    }

# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check in admin table (note: password in DB might not be hashed)
    admin = get_admin_by_credentials(usuario, password)  # Try plain password first
    if not admin:
        admin = get_admin_by_credentials(usuario, hashed_password)  # Fallback to hashed
    if admin:
        session['logged_in'] = True
        session['user'] = usuario
        return jsonify({'message': 'Login exitoso'}), 200
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401

# Logout endpoint
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return jsonify({'message': 'Logout exitoso'}), 200

# Protected route example (dashboard)
@app.route('/app')
def app_page():
    if 'logged_in' in session:
        return send_from_directory('../frontend', 'index.html')
    else:
        return redirect('/login')
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "Backend funcionando 🚀"})

# Serve login page
@app.route('/login')
def login_page():
    return send_from_directory('../frontend', 'login.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)