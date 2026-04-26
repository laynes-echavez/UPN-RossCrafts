-- ========================================
-- CONFIGURACIÓN DE BASE DE DATOS PARA PRODUCCIÓN
-- Ross Crafts - SQL Server Express
-- ========================================
-- 
-- Ejecutar en SQL Server Management Studio como sysadmin
-- Reemplazar DOMINIO\usuario_iis con el usuario real del servicio

USE master;
GO

-- ========================================
-- 1. CREAR BASE DE DATOS DE PRODUCCIÓN
-- ========================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'ross_crafts_db')
BEGIN
    CREATE DATABASE ross_crafts_db 
    COLLATE Modern_Spanish_CI_AS;
    PRINT '✅ Base de datos ross_crafts_db creada exitosamente';
END
ELSE
BEGIN
    PRINT '⚠️  La base de datos ross_crafts_db ya existe';
END
GO

USE ross_crafts_db;
GO

-- ========================================
-- 2. CONFIGURAR PERMISOS PARA USUARIO IIS
-- ========================================

-- IMPORTANTE: Reemplazar 'DOMINIO\usuario_iis' con el usuario real
-- Ejemplos:
--   - IIS_IUSRS (grupo por defecto de IIS)
--   - NT AUTHORITY\NETWORK SERVICE
--   - DOMINIO\usuario_especifico

DECLARE @usuario NVARCHAR(128) = 'IIS_IUSRS';  -- CAMBIAR ESTO

-- Crear login si no existe
IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = @usuario)
BEGIN
    DECLARE @sql NVARCHAR(MAX) = 'CREATE LOGIN [' + @usuario + '] FROM WINDOWS;';
    EXEC sp_executesql @sql;
    PRINT '✅ Login creado para ' + @usuario;
END
ELSE
BEGIN
    PRINT '⚠️  Login ya existe para ' + @usuario;
END

-- Crear usuario en la base de datos
IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = @usuario)
BEGIN
    DECLARE @sql2 NVARCHAR(MAX) = 'CREATE USER [' + @usuario + '] FOR LOGIN [' + @usuario + '];';
    EXEC sp_executesql @sql2;
    PRINT '✅ Usuario creado en la base de datos';
END
ELSE
BEGIN
    PRINT '⚠️  Usuario ya existe en la base de datos';
END

-- Asignar roles necesarios
DECLARE @sql3 NVARCHAR(MAX) = 'ALTER ROLE db_datareader ADD MEMBER [' + @usuario + '];';
EXEC sp_executesql @sql3;

DECLARE @sql4 NVARCHAR(MAX) = 'ALTER ROLE db_datawriter ADD MEMBER [' + @usuario + '];';
EXEC sp_executesql @sql4;

DECLARE @sql5 NVARCHAR(MAX) = 'ALTER ROLE db_ddladmin ADD MEMBER [' + @usuario + '];';
EXEC sp_executesql @sql5;

PRINT '✅ Roles asignados: db_datareader, db_datawriter, db_ddladmin';
GO

-- ========================================
-- 3. VERIFICAR PERMISOS
-- ========================================

PRINT '';
PRINT '========================================';
PRINT 'VERIFICACIÓN DE PERMISOS';
PRINT '========================================';
PRINT '';

SELECT 
    dp.name AS usuario,
    dp.type_desc AS tipo,
    r.name AS rol
FROM sys.database_role_members drm
JOIN sys.database_principals dp ON drm.member_principal_id = dp.principal_id
JOIN sys.database_principals r ON drm.role_principal_id = r.principal_id
WHERE dp.name IN ('IIS_IUSRS', 'NT AUTHORITY\NETWORK SERVICE')
ORDER BY dp.name, r.name;

PRINT '';
PRINT '✅ Configuración completada';
PRINT '';
PRINT 'Próximos pasos:';
PRINT '1. Verificar que el usuario mostrado arriba es correcto';
PRINT '2. Ejecutar: python scripts\check_db.py';
PRINT '3. Ejecutar: deploy.bat';
PRINT '';
GO

-- ========================================
-- 4. CONFIGURACIÓN ADICIONAL (OPCIONAL)
-- ========================================

-- Habilitar SQL Server Browser (para instancias nombradas)
-- Ejecutar en CMD como administrador:
-- net start "SQL Server Browser"

-- Habilitar TCP/IP si es necesario
-- SQL Server Configuration Manager > SQL Server Network Configuration > 
-- Protocols for SQLEXPRESS01 > TCP/IP > Enable

-- ========================================
-- 5. BACKUP AUTOMÁTICO (RECOMENDADO)
-- ========================================

-- Crear job de backup diario (requiere SQL Server Agent)
-- Ajustar la ruta según tu configuración

/*
USE msdb;
GO

EXEC sp_add_job
    @job_name = N'Backup Ross Crafts DB',
    @enabled = 1,
    @description = N'Backup diario de ross_crafts_db';

EXEC sp_add_jobstep
    @job_name = N'Backup Ross Crafts DB',
    @step_name = N'Backup Database',
    @subsystem = N'TSQL',
    @command = N'BACKUP DATABASE ross_crafts_db TO DISK = ''C:\Backups\ross_crafts_db.bak'' WITH INIT;',
    @retry_attempts = 3,
    @retry_interval = 5;

EXEC sp_add_schedule
    @schedule_name = N'Daily at 2 AM',
    @freq_type = 4,  -- Daily
    @freq_interval = 1,
    @active_start_time = 020000;  -- 2:00 AM

EXEC sp_attach_schedule
    @job_name = N'Backup Ross Crafts DB',
    @schedule_name = N'Daily at 2 AM';

EXEC sp_add_jobserver
    @job_name = N'Backup Ross Crafts DB';
GO
*/
