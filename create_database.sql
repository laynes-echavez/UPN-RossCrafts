-- Script para crear la base de datos Ross Crafts
-- Ejecutar en SQL Server Management Studio o Azure Data Studio

CREATE DATABASE ross_crafts_db COLLATE Modern_Spanish_CI_AS;
GO

USE ross_crafts_db;
GO

-- Verificar que la base de datos fue creada
SELECT name, collation_name, create_date
FROM sys.databases
WHERE name = 'ross_crafts_db';
GO
