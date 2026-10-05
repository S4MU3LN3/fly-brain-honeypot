-- dump_produccion_completo_2026.sql
CREATE TABLE usuarios (id INT, email VARCHAR(255), password_hash VARCHAR(255));
INSERT INTO usuarios VALUES (1, 'admin@empresa.com', '$2y$10$N9qo8uLOickgx2ZMRZoMye');
INSERT INTO usuarios VALUES (2, 'finanzas@empresa.com', '$2y$10$vI8aWBnW3fID.ZQ4/zo1G.');
CREATE TABLE tarjetas (id INT, numero VARCHAR(20), cvv VARCHAR(4), titular VARCHAR(100));
INSERT INTO tarjetas VALUES (1, '4532015112830366', '123', 'EMPRESA SA');
