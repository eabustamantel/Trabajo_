from supabase import create_client, Client
from backend.config import Config
import os

# Inicializar cliente de Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

# Funciones para inicializar tablas en Supabase (si no existen)
def initialize_tables():
    """
    Esta función crea las tablas en Supabase si no existen.
    En Supabase, las tablas se crean manualmente en el dashboard o via SQL,
    pero podemos verificar si existen.
    """
    pass  # Las tablas se crean manualmente en Supabase

# Funciones helper para operaciones CRUD con Supabase
class SupabaseCRUD:
    @staticmethod
    def get_all(table_name):
        try:
            response = supabase.table(table_name).select('*').execute()
            return response.data if response.data is not None else []
        except Exception as e:
            print(f"Error in get_all for {table_name}: {e}")
            return []

    @staticmethod
    def get_by_id(table_name, id):
        if id is None:
            return None
        try:
            response = supabase.table(table_name).select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error in get_by_id for {table_name}, id {id}: {e}")
            return None

    @staticmethod
    def create(table_name, data):
        try:
            response = supabase.table(table_name).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error in create for {table_name}: {e}")
            if hasattr(e, 'message'):
                raise ValueError(e.message)
            else:
                raise ValueError(str(e))

    @staticmethod
    def update(table_name, id, data):
        try:
            response = supabase.table(table_name).update(data).eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error in update for {table_name}, id {id}: {e}")
            return None

    @staticmethod
    def delete(table_name, id):
        try:
            response = supabase.table(table_name).delete().eq('id', id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error in delete for {table_name}, id {id}: {e}")
            return None

    @staticmethod
    def get_where(table_name, column, value):
        try:
            response = supabase.table(table_name).select('*').eq(column, value).execute()
            return response.data if response.data is not None else []
        except Exception as e:
            print(f"Error in get_where for {table_name}, {column}={value}: {e}")
            return []

# Funciones específicas para cada entidad
def get_clientes():
    return SupabaseCRUD.get_all('clientes')

def get_cliente_by_id(id):
    return SupabaseCRUD.get_by_id('clientes', id)

def create_cliente(data):
    return SupabaseCRUD.create('clientes', data)

def update_cliente(id, data):
    return SupabaseCRUD.update('clientes', id, data)

def delete_cliente(id):
    return SupabaseCRUD.delete('clientes', id)

def get_inventarios():
    return SupabaseCRUD.get_all('inventario')

def get_inventario_by_id(id):
    return SupabaseCRUD.get_by_id('inventario', id)

def create_inventario(data):
    return SupabaseCRUD.create('inventario', data)

def update_inventario(id, data):
    return SupabaseCRUD.update('inventario', id, data)

def delete_inventario(id):
    return SupabaseCRUD.delete('inventario', id)

def get_vehiculos():
    return SupabaseCRUD.get_all('vehiculos')

def get_vehiculo_by_id(id):
    return SupabaseCRUD.get_by_id('vehiculos', id)

def create_vehiculo(data):
    return SupabaseCRUD.create('vehiculos', data)

def update_vehiculo(id, data):
    return SupabaseCRUD.update('vehiculos', id, data)

def delete_vehiculo(id):
    return SupabaseCRUD.delete('vehiculos', id)

def get_ordenes():
    ordenes = SupabaseCRUD.get_all('ordenes')
    # Agregar información del cliente
    for orden in ordenes:
        if orden.get('cliente_id'):
            cliente = get_cliente_by_id(orden['cliente_id'])
            if cliente:
                orden['cliente_nombre'] = f"{cliente['nombre']} {cliente['apellido']}"
            else:
                orden['cliente_nombre'] = None
    return ordenes

def get_orden_by_id(id):
    return SupabaseCRUD.get_by_id('ordenes', id)

def create_orden(data):
    # No validar existencia de cliente_id o vehiculo_id, registrar tal como viene
    return SupabaseCRUD.create('ordenes', data)

def update_orden(id, data):
    # No validar existencia de cliente_id o vehiculo_id, actualizar tal como viene
    return SupabaseCRUD.update('ordenes', id, data)

def delete_orden(id):
    return SupabaseCRUD.delete('ordenes', id)

def get_empleados():
    return SupabaseCRUD.get_all('empleados')

def get_empleado_by_id(id):
    return SupabaseCRUD.get_by_id('empleados', id)

def create_empleado(data):
    return SupabaseCRUD.create('empleados', data)

def update_empleado(id, data):
    return SupabaseCRUD.update('empleados', id, data)

def delete_empleado(id):
    return SupabaseCRUD.delete('empleados', id)

def get_proveedores():
    return SupabaseCRUD.get_all('proveedores')

def get_proveedor_by_id(id):
    return SupabaseCRUD.get_by_id('proveedores', id)

def create_proveedor(data):
    return SupabaseCRUD.create('proveedores', data)

def update_proveedor(id, data):
    return SupabaseCRUD.update('proveedores', id, data)

def delete_proveedor(id):
    return SupabaseCRUD.delete('proveedores', id)

# Funciones para Admin (para login)
def get_admin_by_credentials(usuario, hashed_password):
    response = supabase.table('admin').select('*').eq('usuario', usuario).eq('password', hashed_password).execute()
    return response.data[0] if response.data else None

def create_admin(data):
    return SupabaseCRUD.create('admin', data)
