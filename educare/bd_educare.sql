CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    periodo VARCHAR(50),
    curso VARCHAR(100),
    dataDaUltimaConsulta DATE,
    email VARCHAR(100),
    telefone VARCHAR(20),
    observacoes TEXT,
    links TEXT
);
