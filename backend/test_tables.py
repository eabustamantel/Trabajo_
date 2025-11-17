from models import supabase

# Test all tables
tables = ['clientes', 'inventario', 'ordenes', 'empleados', 'proveedores', 'vehiculos', 'admin']

for table in tables:
    try:
        response = supabase.table(table).select('*').execute()
        print(f"{table}: {len(response.data)} records")
        if response.data:
            print(f"  Sample: {response.data[0]}")
    except Exception as e:
        print(f"{table}: ERROR - {e}")
