import requests

base_url = 'http://localhost:5000'

# Test endpoints that are failing
endpoints = [
    '/api/ordenes',
    '/api/empleados'
]

for endpoint in endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}")
        print(f"{endpoint}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text}")
            # Try to get more details from the server logs
            print("  Checking server logs...")
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")

# Also test the functions directly
from models import get_ordenes, get_empleados

print("\nDirect function calls:")
try:
    ordenes = get_ordenes()
    print(f"get_ordenes(): {len(ordenes)} records")
    print(f"  Type: {type(ordenes)}")
    if ordenes:
        print(f"  Sample: {ordenes[0]}")
except Exception as e:
    print(f"get_ordenes() ERROR: {e}")

try:
    empleados = get_empleados()
    print(f"get_empleados(): {len(empleados)} records")
    print(f"  Type: {type(empleados)}")
    if empleados:
        print(f"  Sample: {empleados[0]}")
except Exception as e:
    print(f"get_empleados() ERROR: {e}")
