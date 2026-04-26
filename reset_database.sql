-- Script para resetear la base de datos Ross Crafts
-- ADVERTENCIA: Este script eliminará TODOS los datos

USE ross_crafts_db;
GO

-- Desactivar restricciones de clave foránea
EXEC sp_MSforeachtable 'ALTER TABLE ? NOCHECK CONSTRAINT ALL';
GO

-- Eliminar todas las tablas
EXEC sp_MSforeachtable 'DROP TABLE ?';
GO

PRINT 'Base de datos limpiada exitosamente';
GO
