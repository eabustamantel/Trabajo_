import hashlib
from models import create_admin

# Create default admin user
usuario = 'admin'
password = 'admin'
hashed_password = hashlib.sha256(password.encode()).hexdigest()

admin_data = {
    'usuario': usuario,
    'password': hashed_password
}

try:
    admin = create_admin(admin_data)
    print(f"Admin user created successfully: {admin}")
except Exception as e:
    print(f"Error creating admin: {e}")
