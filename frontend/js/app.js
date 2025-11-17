
const API_BASE = 'https://trabajo-production.up.railway.app/api';

let currentEntity = '';

function getPageName(entity) {
    if (entity === 'cliente') return 'clientes';
    if (entity === 'orden') return 'ordenes';
    if (entity === 'empleado') return 'empleados';
    if (entity === 'proveedor') return 'proveedores';
    return entity; // inventario
}

function getPlural(entity) {
    if (entity === 'orden') return 'ordenes';
    if (entity === 'proveedor') return 'proveedores';
    return entity + 's';
}

// Navigation
function loadPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(page).classList.add('active');

    switch(page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'clientes':
            loadClientes();
            break;
        case 'inventario':
            loadInventario();
            break;
        case 'ordenes':
            loadOrdenes();
            break;
        case 'empleados':
            loadEmpleados();
            break;
        case 'proveedores':
            loadProveedores();
            break;
    }
}



// Clientes
async function loadClientes() {
    try {
        const clientes = await fetch(`${API_BASE}/clientes`).then(r => r.json());
        const tbody = document.querySelector('#clientes-table tbody');
        tbody.innerHTML = '';

        clientes.forEach(cliente => {
            const row = `
                <tr>
                    <td>${cliente.id}</td>
                    <td>${cliente.nombre}</td>
                    <td>${cliente.apellido}</td>
                    <td>${cliente.telefono || ''}</td>
                    <td>${cliente.email || ''}</td>
                    <td>${cliente.direccion || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="editEntity('cliente', ${cliente.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEntity('cliente', ${cliente.id})">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading clientes:', error);
    }
}

// Inventario
async function loadInventario() {
    try {
        const inventario = await fetch(`${API_BASE}/inventarios`).then(r => r.json());
        const tbody = document.querySelector('#inventario-table tbody');
        tbody.innerHTML = '';

        inventario.forEach(item => {
            const row = `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.nombre}</td>
                    <td>${item.descripcion || ''}</td>
                    <td>${item.cantidad}</td>
                    <td>$${item.precio}</td>
                    <td>${item.categoria || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="editEntity('inventario', ${item.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEntity('inventario', ${item.id})">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading inventario:', error);
    }
}

// Ordenes
async function loadOrdenes() {
    try {
        const ordenes = await fetch(`${API_BASE}/ordenes`).then(r => r.json());
        const tbody = document.querySelector('#ordenes-table tbody');
        tbody.innerHTML = '';

        ordenes.forEach(orden => {
            const row = `
                <tr>
                    <td>${orden.id}</td>
                    <td>${orden.descripcion}</td>
                    <td>${new Date(orden.fecha_creacion).toLocaleDateString()}</td>
                    <td>${orden.estado}</td>
                    <td>${orden.cliente_nombre || ''}</td>
                    <td>${orden.vehiculo_id || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="editEntity('orden', ${orden.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEntity('orden', ${orden.id})">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading ordenes:', error);
    }
}

// Empleados
async function loadEmpleados() {
    try {
        const empleados = await fetch(`${API_BASE}/empleados`).then(r => r.json());
        const tbody = document.querySelector('#empleados-table tbody');
        tbody.innerHTML = '';

        empleados.forEach(empleado => {
            const row = `
                <tr>
                    <td>${empleado.id}</td>
                    <td>${empleado.nombre}</td>
                    <td>${empleado.apellido}</td>
                    <td>${empleado.puesto || ''}</td>
                    <td>${empleado.telefono || ''}</td>
                    <td>${empleado.email || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="editEntity('empleado', ${empleado.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEntity('empleado', ${empleado.id})">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading empleados:', error);
    }
}

// Proveedores
async function loadProveedores() {
    try {
        const proveedores = await fetch(`${API_BASE}/proveedores`).then(r => r.json());
        const tbody = document.querySelector('#proveedores-table tbody');
        tbody.innerHTML = '';

        proveedores.forEach(proveedor => {
            const row = `
                <tr>
                    <td>${proveedor.id}</td>
                    <td>${proveedor.nombre}</td>
                    <td>${proveedor.contacto || ''}</td>
                    <td>${proveedor.telefono || ''}</td>
                    <td>${proveedor.email || ''}</td>
                    <td>${proveedor.direccion || ''}</td>
                    <td>
                        <button class="btn-edit" onclick="editEntity('proveedor', ${proveedor.id})">Editar</button>
                        <button class="btn-delete" onclick="deleteEntity('proveedor', ${proveedor.id})">Eliminar</button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error loading proveedores:', error);
    }
}

// Modal and Forms
function showForm(entity, id = null) {
    currentEntity = entity;
    const modal = document.getElementById('modal');
    const title = document.getElementById('modal-title');
    const form = document.getElementById('entity-form');

    title.textContent = id ? `Editar ${entity}` : `Agregar ${entity}`;
    form.innerHTML = getFormFields(entity);

    if (entity === 'orden') {
        populateClienteSelect();
    }

    if (id) {
        loadEntityData(entity, id);
    }

    modal.style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('entity-form').reset();
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('error-message').textContent = '';
}

function getFormFields(entity) {
    const fields = {
        cliente: `
            <label>Nombre:</label>
            <input type="text" name="nombre" required>
            <label>Apellido:</label>
            <input type="text" name="apellido" required>
            <label>Teléfono:</label>
            <input type="tel" name="telefono">
            <label>Email:</label>
            <input type="email" name="email">
            <label>Dirección:</label>
            <textarea name="direccion"></textarea>
        `,
        inventario: `
            <label>Nombre:</label>
            <input type="text" name="nombre" required>
            <label>Descripción:</label>
            <textarea name="descripcion"></textarea>
            <label>Cantidad:</label>
            <input type="number" name="cantidad" required>
            <label>Precio:</label>
            <input type="number" step="0.01" name="precio" required>
            <label>Categoría:</label>
            <select name="categoria">
                <option value="">Seleccionar</option>
                <option value="vehiculos">Vehículos</option>
                <option value="repuestos">Repuestos</option>
                <option value="herramientas">Herramientas</option>
                <option value="insumos">Insumos</option>
            </select>
        `,
        orden: `
            <label>Descripción:</label>
            <textarea name="descripcion" required></textarea>
            <label>Estado:</label>
            <select name="estado">
                <option value="pendiente">Pendiente</option>
                <option value="en_progreso">En Progreso</option>
                <option value="completada">Completada</option>
            </select>
            <label>Cliente:</label>
            <select name="cliente_id">
                <option value="">Seleccionar Cliente</option>
            </select>
            <label>ID Vehículo:</label>
            <input type="number" name="vehiculo_id">
        `,
        empleado: `
            <label>Nombre:</label>
            <input type="text" name="nombre" required>
            <label>Apellido:</label>
            <input type="text" name="apellido" required>
            <label>Puesto:</label>
            <input type="text" name="puesto">
            <label>Teléfono:</label>
            <input type="tel" name="telefono">
            <label>Email:</label>
            <input type="email" name="email">
        `,
        proveedor: `
            <label>Nombre:</label>
            <input type="text" name="nombre" required>
            <label>Contacto:</label>
            <input type="text" name="contacto">
            <label>Teléfono:</label>
            <input type="tel" name="telefono">
            <label>Email:</label>
            <input type="email" name="email">
            <label>Dirección:</label>
            <textarea name="direccion"></textarea>
        `
    };

    return fields[entity] + '<button type="submit" class="btn-save">Guardar Cambios</button><button type="button" class="btn-cancel" onclick="closeModal()">Cancelar</button>';
}

async function loadEntityData(entity, id) {
    try {
        const data = await fetch(`${API_BASE}/${getPlural(entity)}/${id}`).then(r => r.json());
        const form = document.getElementById('entity-form');

        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key] || '';
            }
        });
    } catch (error) {
        console.error(`Error loading ${entity} data:`, error);
    }
}

document.getElementById('entity-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    const method = e.target.dataset.id ? 'PUT' : 'POST';
    const url = e.target.dataset.id
        ? `${API_BASE}/${getPlural(currentEntity)}/${e.target.dataset.id}`
        : `${API_BASE}/${getPlural(currentEntity)}`;

    try {
        const response = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert(method === 'POST' ? 'Datos guardados correctamente' : 'Datos actualizados correctamente');
            closeModal();
            try {
                loadPage(getPageName(currentEntity));
                if (currentEntity !== 'orden') loadDashboard();
            } catch (pageError) {
                console.error('Error updating page:', pageError);
            }
        } else {
            const errorData = await response.json();
            if (errorData.error) {
                const errorElement = document.getElementById('error-message');
                errorElement.textContent = errorData.error;
                errorElement.style.display = 'block';
            } else {
                alert('Error al guardar los datos');
            }
        }
    } catch (error) {
        console.error('Error saving data:', error);
        alert('Error al guardar los datos');
    }
});

async function editEntity(entity, id) {
    currentEntity = entity;
    const modal = document.getElementById('modal');
    const title = document.getElementById('modal-title');
    const form = document.getElementById('entity-form');

    title.textContent = `Editar ${entity}`;
    form.innerHTML = getFormFields(entity);
    form.dataset.id = id;

    await loadEntityData(entity, id);
    modal.style.display = 'block';
}

async function deleteEntity(entity, id) {
    if (confirm(`¿Estás seguro de eliminar este ${entity}?`)) {
        try {
            const response = await fetch(`${API_BASE}/${getPlural(entity)}/${id}`, { method: 'DELETE' });
            if (response.ok) {
                loadPage(getPageName(entity));
                if (entity !== 'orden') loadDashboard();
            } else {
                alert('Error al eliminar');
            }
        } catch (error) {
            console.error('Error deleting:', error);
            alert('Error al eliminar');
        }
    }
}

// Counter animation for dashboard stats
function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 20);
}

// Scroll animation observer
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observe sections for scroll animations
    document.querySelectorAll('.page').forEach(section => {
        observer.observe(section);
    });
}

// Enhanced dashboard loading with animations
async function loadDashboard() {
    try {
        const [clientes, inventario, ordenes, empleados] = await Promise.all([
            fetch(`${API_BASE}/clientes`).then(r => r.json()),
            fetch(`${API_BASE}/inventarios`).then(r => r.json()),
            fetch(`${API_BASE}/ordenes`).then(r => r.json()),
            fetch(`${API_BASE}/empleados`).then(r => r.json())
        ]);

        const totalClientes = clientes.length;
        const totalInventario = inventario.length;
        const ordenesActivas = ordenes.filter(o => o.estado !== 'completada').length;
        const totalEmpleados = empleados.length;

        // Animate counters
        setTimeout(() => animateCounter(document.getElementById('total-clientes'), totalClientes), 500);
        setTimeout(() => animateCounter(document.getElementById('total-inventario'), totalInventario), 700);
        setTimeout(() => animateCounter(document.getElementById('ordenes-activas'), ordenesActivas), 900);
        setTimeout(() => animateCounter(document.getElementById('total-empleados'), totalEmpleados), 1100);

    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// PDF Generation
async function generatePDF(entity) {
    try {
        const response = await fetch(`${API_BASE}/pdf/${entity}`);

        if (!response.ok) {
            throw new Error('Error al generar el PDF');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        // Create a temporary link to trigger download
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${entity}_reporte.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        alert('Reporte generado correctamente');
    } catch (error) {
        console.error('Error generating PDF:', error);
        alert('Error al generar el reporte');
    }
}

// Populate cliente select for orders
async function populateClienteSelect() {
    try {
        const clientes = await fetch(`${API_BASE}/clientes`).then(r => r.json());
        const select = document.querySelector('select[name="cliente_id"]');
        select.innerHTML = '<option value="">Seleccionar Cliente</option>';

        clientes.forEach(cliente => {
            const option = document.createElement('option');
            option.value = cliente.id;
            option.textContent = `${cliente.nombre} ${cliente.apellido}`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading clientes for select:', error);
    }
}

// Logout function
function logout() {
    fetch('/api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            window.location.href = '/login';
        }
    })
    .catch(error => {
        console.error('Error during logout:', error);
        window.location.href = '/login';
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadPage('dashboard');
    initScrollAnimations();
});
