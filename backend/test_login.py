import hashlib
from models import get_admin_by_credentials

# Test login with default credentials
usuario = 'admin'
password = 'admin123'  # Use the actual password from DB

print(f"Testing login for usuario: {usuario}")
print(f"Password: {password}")

admin = get_admin_by_credentials(usuario, password)
if admin:
    print("Login successful!")
    print(f"Admin data: {admin}")
else:
    print("Login failed. Admin not found or password incorrect.")

# Also check if admin exists at all
from models import supabase
response = supabase.table('admin').select('*').execute()
print(f"All admin records: {response.data}")
