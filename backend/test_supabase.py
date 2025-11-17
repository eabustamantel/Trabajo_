from models import supabase, get_clientes

try:
    # Test connection by getting clientes
    clientes = get_clientes()
    print("Connection to Supabase successful!")
    print(f"Retrieved {len(clientes)} clientes.")
except Exception as e:
    print(f"Error connecting to Supabase: {e}")
