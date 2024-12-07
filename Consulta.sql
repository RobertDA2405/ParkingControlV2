CREATE DATABASE bdparqueo


-- Crear la tabla Cliente
CREATE TABLE Cliente (
	 idclient INT AUTO_INCREMENT PRIMARY KEY,
    Cedula VARCHAR (20) UNIQUE,
    Nombre VARCHAR(30),
    Apellido VARCHAR(30),
    Direccion VARCHAR(150),
    NumeroContacto INT(10)
);

-- Crear la tabla Vehiculo
CREATE TABLE Vehiculo (
    idvehicle INT AUTO_INCREMENT PRIMARY KEY,
    Placa VARCHAR (10),
    tipo_Vehiculo VARCHAR (20),
    Color VARCHAR (15),
    HoraIngreso VARCHAR (15),
    HoraSalida VARCHAR (15),
    Pago REAL,
    Pendiente REAL,
    Observaciones VARCHAR (200),
    idclient INT,
    estado VARCHAR (50),
    FOREIGN KEY (idclient) REFERENCES Cliente(idclient)
);

ALTER TABLE Vehiculo MODIFY COLUMN tipo_Vehiculo VARCHAR(50);



CREATE TABLE users (
    iduser INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE historial (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo_accion VARCHAR(20),
    tabla_afectada VARCHAR(50),
    datos_antiguos TEXT,
    datos_nuevos TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(50)
);