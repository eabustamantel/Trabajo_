import requests

base_url = 'http://localhost:5000'

# Test endpoints that are failing
endpoints = [
    '/api/ordenes',
    '/api/empleados',
    '/api/clientes',
    '/api/inventarios'
]

for endpoint in endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}")
        print(f"{endpoint}: {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")
