// index.js

const API_BASE_URL = 'http://127.0.0.1:5000';
let currentVIN = null; 
let isEditing = false; 
let allInventory = []; // Cache para el filtro de Búsqueda Avanzada

// --- Funciones de Utilidad ---
function showForm(mode, data = {}) {
    // Lógica para mostrar y llenar el formulario (Punto 1)
    const container = document.getElementById('vehicleFormContainer');
    const title = document.getElementById('formTitle');
    const btnSave = document.getElementById('btnSave');
    const btnDelete = document.getElementById('btnDelete');
    const formMessage = document.getElementById('formMessage');

    container.style.display = 'block';
    formMessage.textContent = ''; 

    document.getElementById('fmarca').value = data.Marca || '';
    document.getElementById('fmodelo').value = data.Modelo || '';
    document.getElementById('fprecio').value = data.Precio || '';
    document.getElementById('fkilometraje').value = data.Kilometraje || '';
    document.getElementById('festado').value = data.Estado || 'Disponible';

    if (mode === 'CREATE') {
        isEditing = false;
        title.textContent = `Crear Nuevo Vehículo (VIN: ${currentVIN})`;
        btnSave.textContent = 'Crear Vehículo (POST)';
        btnDelete.style.display = 'none';
        formMessage.style.color = 'orange';
        formMessage.textContent = 'Este VIN no existe. Rellene los campos y haga clic en Crear.';
    } else if (mode === 'EDIT') {
        isEditing = true;
        title.textContent = `Editar Vehículo Existente (VIN: ${currentVIN})`;
        btnSave.textContent = 'Guardar Cambios (PUT)';
        btnDelete.style.display = 'inline-block';
    }
    
    document.getElementById('vinManageInput').disabled = true; 
}

function hideForm() {
    // Lógica para ocultar el formulario (Punto 1)
    document.getElementById('vehicleFormContainer').style.display = 'none';
    document.getElementById('vinManageInput').disabled = false;
    document.getElementById('vinManageInput').value = ''; 
    document.getElementById('formMessage').textContent = '';
    currentVIN = null;
}

function displayMessage(text, isError = false) {
    // Lógica para mostrar mensajes de estado (Punto 1)
    const formMessage = document.getElementById('formMessage');
    formMessage.style.color = isError ? 'red' : 'green';
    formMessage.textContent = text;
}


// --- Lógica del Formulario CRUD (Punto 1) ---

async function checkVehicleExistence() {
    // Lógica para verificar la existencia del VIN
    const vinInput = document.getElementById('vinManageInput');
    const vin = vinInput.value.trim().toUpperCase();
    currentVIN = vin;
    
    if (!vin) {
        displayMessage('Por favor, introduzca un VIN.', true);
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/vehicles/${vin}`);
        const data = await response.json();

        if (response.status === 404) {
            // No existe: Opción de Crear
            if (confirm(`Vehículo con VIN ${vin} no encontrado. ¿Desea crear un nuevo vehículo con este VIN?`)) {
                showForm('CREATE');
            } else {
                hideForm();
            }
        } else if (response.status === 200) {
            // Existe: Opción de Editar
            showForm('EDIT', data);
            displayMessage(`Vehículo ${vin} cargado con éxito. Puede editarlo.`, false);
        } 
    } catch (error) {
        displayMessage('Error de red o conexión con la API.', true);
        console.error('Check existence error:', error);
    }
}

document.getElementById('vehicleForm').addEventListener('submit', async function(e) {
    // Lógica para guardar (POST/PUT)
    e.preventDefault();

    const dataToSend = {
        VIN: currentVIN, 
        Marca: document.getElementById('fmarca').value,
        Modelo: document.getElementById('fmodelo').value,
        Precio: parseInt(document.getElementById('fprecio').value), 
        Kilometraje: parseInt(document.getElementById('fkilometraje').value),
        Estado: document.getElementById('festado').value
    };

    let url = `${API_BASE_URL}/vehicles/${currentVIN}`;
    let method = 'PUT';
    let successMsg = 'actualizado';

    if (!isEditing) {
        url = `${API_BASE_URL}/vehicles`;
        method = 'POST';
        successMsg = 'creado';
    }
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataToSend)
        });

        const result = await response.json();

        if (response.ok) {
            displayMessage(`Vehículo ${currentVIN} ${successMsg} con éxito.`, false);
            hideForm();
            fetchAvailableVehicles(); // Refrescar lista de disponibles
        } else {
            displayMessage(`Fallo al ${successMsg}: ${result.details || result.error || result.message}`, true);
        }

    } catch (error) {
        displayMessage('Error de red al guardar.', true);
        console.error('Save error:', error);
    }
});

async function deleteVehicle() {
    // Lógica para eliminar (DELETE)
    if (!confirm(`¿Está seguro de que desea eliminar el vehículo con VIN: ${currentVIN}? Esta acción es irreversible.`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/vehicles/${currentVIN}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok) {
            displayMessage(`Vehículo ${currentVIN} eliminado con éxito.`, false);
            hideForm();
            fetchAvailableVehicles(); 
        } else if (response.status === 404) {
             displayMessage(`Error al eliminar: Vehículo no encontrado.`, true);
        } else {
            displayMessage(`Fallo al eliminar: ${result.error || result.message}`, true);
        }

    } catch (error) {
        displayMessage('Error de red al eliminar.', true);
        console.error('Delete error:', error);
    }
}


// ====================================================================================
// PUNTO 3: BÚSQUEDA DETALLADA POR ATRIBUTOS (Filtros)
// ====================================================================================

// Función para poblar dinámicamente los dropdowns de Marca y Modelo (usa el endpoint GET /vehicles)
async function populateFilters() {
    try {
        const response = await fetch(`${API_BASE_URL}/vehicles`); // Obtiene TODOS los 55 ítems
        const data = await response.json();
        
        allInventory = data.vehicles || []; // Cachear el inventario completo
        
        const marcas = new Set(['']); 
        const modelos = new Set(['']); 

        allInventory.forEach(v => {
            marcas.add(v.Marca);
            modelos.add(v.Modelo);
        });

        const marcaSelect = document.getElementById('searchMarca');
        const modeloSelect = document.getElementById('searchModelo');

        // Poblar Marca
        marcaSelect.innerHTML = '<option value="">Marca</option>';
        Array.from(marcas).sort().forEach(m => {
            if (m) marcaSelect.innerHTML += `<option value="${m}">${m}</option>`;
        });
        
        // Poblar Modelo
        modeloSelect.innerHTML = '<option value="">Modelo</option>';
        Array.from(modelos).sort().forEach(m => {
            if (m) modeloSelect.innerHTML += `<option value="${m}">${m}</option>`;
        });

    } catch (error) {
        console.error('Error al poblar filtros de búsqueda:', error);
    }
}

// Función para buscar y mostrar los detalles de UN vehículo que coincida con los filtros
function findVehicleDetails() {
    const selectedMarca = document.getElementById('searchMarca').value;
    const selectedModelo = document.getElementById('searchModelo').value;
    const detailDiv = document.getElementById('vehicleDetail');

    detailDiv.innerHTML = '<p>Buscando...</p>';

    if (!selectedMarca && !selectedModelo) {
        detailDiv.innerHTML = '<p style="color: red;">Seleccione al menos una Marca o Modelo para buscar.</p>';
        return;
    }

    // Filtrar en la caché (inventario completo)
    const foundVehicle = allInventory.find(v => 
        (!selectedMarca || v.Marca === selectedMarca) && 
        (!selectedModelo || v.Modelo === selectedModelo)
    );

    if (foundVehicle) {
        detailDiv.innerHTML = `
            <h3>Vehículo Encontrado</h3>
            <p><strong>VIN:</strong> ${foundVehicle.VIN}</p>
            <p><strong>Estado:</strong> ${foundVehicle.Estado}</p>
            <pre>${JSON.stringify(foundVehicle, null, 2)}</pre>
        `;
    } else {
        detailDiv.innerHTML = '<p style="color: orange;">No se encontró un vehículo que coincida con la selección.</p>';
    }
}


// ====================================================================================
// PUNTO 4: CONSULTA OBLIGATORIA (Restaurada y Limpia)
// ====================================================================================

// Consulta 1: Consulta Compleja Obligatoria (Punto 4)
async function fetchAvailableVehicles() {
    try {
        // Llama directamente al endpoint sin filtros
        const response = await fetch(`${API_BASE_URL}/vehicles/available`);
        const data = await response.json();
        
        let vehicles = data.vehicles || [];
        
        const tableBody = document.querySelector('#inventoryTable tbody');
        tableBody.innerHTML = ''; 
        
        document.getElementById('countAvailable').textContent = vehicles.length || 0; 
        
        if (vehicles.length === 0) {
             tableBody.innerHTML = '<tr><td colspan="5">No se encontraron vehículos disponibles.</td></tr>';
             return;
        }

        vehicles.forEach(vehicle => {
            const row = tableBody.insertRow();
            const formattedPrice = parseFloat(vehicle.Precio).toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });

            row.insertCell().textContent = vehicle.VIN;
            row.insertCell().textContent = vehicle.Marca;
            row.insertCell().textContent = vehicle.Modelo;
            row.insertCell().textContent = formattedPrice;
            row.insertCell().textContent = vehicle.Kilometraje + ' km';
        });

    } catch (error) {
        console.error('Error fetching available vehicles:', error);
    }
}


// --- FUNCIONES DE CONSULTA (Punto 2) ---

// Consulta 2: Consulta Adicional Empleados (Punto 2)
async function fetchUsersByRole(role) {
    const usersResultDiv = document.getElementById('usersResult');
    usersResultDiv.innerHTML = '<p>Buscando...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/users/role/${role}`);
        const data = await response.json();

        let html = `<h3>Empleados con Rol: ${role} (${data.count} encontrado(s))</h3>`;
        
        if (data.count > 0) {
            html += '<ul>';
            data.employees.forEach(user => {
                html += `<li>${user.Nombre_Completo} (${user.UserID}) - Email: ${user.Email}</li>`;
            });
            html += '</ul>';
        } else {
            html += '<p>No se encontraron empleados con ese rol.</p>';
        }
        usersResultDiv.innerHTML = html;

    } catch (error) {
        usersResultDiv.innerHTML = '<p style="color: red;">Error al conectar con la API para buscar usuarios.</p>';
        console.error('Error fetching users by role:', error);
    }
}


// Cargar funciones iniciales al cargar la página
window.onload = function() {
    populateFilters(); // Carga la lista completa en caché y rellena los dropdowns del Punto 3
    fetchAvailableVehicles(); // Carga la lista inicial del Punto 4
}