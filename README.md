---

# **ParkingControl - Sistema de Gestión de Parqueo**

¡Bienvenido a **ParkingControl**! Este proyecto es un sistema de gestión de parqueos diseñado para administrar de manera eficiente el registro de vehículos, control de pagos, y estado de los mismos dentro y fuera del parqueo.

---

## **Características principales**

### **Interfaz de Administrador**
- **Gestión de Vehículos:**
  - Registrar vehículos nuevos.
  - Editar información de vehículos existentes.
  - Eliminar registros de vehículos.
  - Registrar salidas de vehículos.
- **Control de Empleados:**
  - Ver lista de empleados registrados.
  - Añadir nuevos empleados (solo para administradores).
- **Historial:**
  - Seguimiento de acciones realizadas, como ediciones o eliminaciones.

### **Interfaz de Empleado**
- Funciones limitadas:
  - Registrar vehículos nuevos.
  - Registrar salidas de vehículos.
  - Visualizar vehículos registrados.
  - Sin permisos para eliminar o editar registros de vehículos.

### **Base de Datos**
- Gestión centralizada de información:
  - Tabla de clientes.
  - Tabla de vehículos.
  - Tabla de usuarios (administradores y empleados).
  - Historial de acciones realizadas.

---

## **Tecnologías utilizadas**
- **Lenguaje:** Python
- **Framework:** PyQt6 para la interfaz gráfica.
- **Base de datos:** MySQL
- **Dependencias clave:**
  - `mysql-connector-python` para la conexión con la base de datos.
  - `pyqt6` para construir las interfaces de usuario.

---

## **Instalación**

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tuusuario/ParkingControl.git
   cd ParkingControl
   ```

2. **Configura tu entorno:**
   Asegúrate de tener Python 3.9 o superior instalado.

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura la base de datos:**
   - Importa el archivo `schema.sql` en tu base de datos MySQL.
   - Configura los datos de conexión en el archivo `config/database.py`.

5. **Ejecuta la aplicación:**
   ```bash
   python main.py
   ```

---

## **Cómo exportar a .exe**

1. **Instala pyinstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Genera el archivo ejecutable:**
   Desde la raíz del proyecto, ejecuta:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. **Encuentra tu archivo .exe:**
   El ejecutable estará en la carpeta `dist/`.

---

## **Contribuciones**

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama con tus cambios:
   ```bash
   git checkout -b mi-nueva-funcionalidad
   ```
3. Realiza un commit de tus cambios:
   ```bash
   git commit -m "Añadí una nueva funcionalidad"
   ```
4. Haz push a tu rama:
   ```bash
   git push origin mi-nueva-funcionalidad
   ```
5. Abre un pull request.

---

## **Créditos**

Desarrollado por Roberto David Aráuz Meynard, Garett Antonio Sanchéz Llanes, Alejandra Elizabeth Hernandez Galan, Alexander Samuel Huete García como una solución eficiente para la gestión de parqueos.

---