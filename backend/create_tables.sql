-- Crear tabla inventario
CREATE TABLE IF NOT EXISTS inventario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    cantidad INTEGER NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50)
);

-- Crear tabla vehiculos
CREATE TABLE IF NOT EXISTS vehiculos (
    id SERIAL PRIMARY KEY,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    anio INTEGER,
    placa VARCHAR(20) UNIQUE,
    cliente_id INTEGER REFERENCES clientes(id)
);

-- Crear tabla ordenes
CREATE TABLE IF NOT EXISTS ordenes (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) DEFAULT 'pendiente',
    cliente_id INTEGER,
    vehiculo_id INTEGER
);

-- Crear tabla empleados
CREATE TABLE IF NOT EXISTS empleados (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    puesto VARCHAR(50),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE
);

-- Crear tabla proveedores
CREATE TABLE IF NOT EXISTS proveedores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    contacto VARCHAR(100),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    direccion TEXT
);

-- Crear tabla admin
CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
