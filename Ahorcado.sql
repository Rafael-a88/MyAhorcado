CREATE database ahorcado;
USE ahorcado;

CREATE TABLE Frutas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Conceptos_informaticos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE Nombres_persona (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    partidas_ganadas INT DEFAULT 0,
    partidas_perdidas INT DEFAULT 0
);

INSERT INTO Frutas (nombre) VALUES ('Manzana'), ('Banana'), ('Naranja'), ('Fresa'), ('Uva'), ('Pera'), ('Sandia'), ('Cereza'), ('Mango'), ('Piña');
INSERT INTO Conceptos_informaticos (nombre) VALUES ('Algoritmo'), ('Programacion'), ('Python'), ('Redes'), ('Compilador'), ('Sistema'), ('IA'), ('BigData'), ('Ciberseguridad'), ('Java'); 
INSERT INTO Nombres_persona (nombre) VALUES ('Juan'), ('Maria'), ('Pedro'), ('Ana'), ('Luis'), ('Carlos'), ('Sofia'), ('Jose'), ('Laura'), ('David');

