# Guía de Contribución - UPN RossCrafts

## 📋 Sobre el Proyecto

Este es un proyecto académico desarrollado como Capstone para la Universidad Privada del Norte (UPN). El sistema Ross Crafts es una plataforma integral de e-commerce y POS desarrollada con Django.

## 🤝 Cómo Contribuir

### Para Estudiantes y Académicos

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/laynes-echavez/UPN-RossCrafts.git
   cd UPN-RossCrafts
   ```

2. **Crear una rama para tu contribución**
   ```bash
   git checkout -b feature/nombre-de-tu-mejora
   ```

3. **Realizar cambios siguiendo las convenciones**
   - Código en español para comentarios y documentación
   - Seguir PEP 8 para Python
   - Usar nombres descriptivos para variables y funciones
   - Documentar funciones complejas

4. **Probar tus cambios**
   ```bash
   python validate_system_flows.py
   python manage.py test
   ```

5. **Commit con mensaje descriptivo**
   ```bash
   git commit -m "feat: descripción clara de la mejora"
   ```

6. **Push y crear Pull Request**
   ```bash
   git push origin feature/nombre-de-tu-mejora
   ```

### Tipos de Contribuciones Bienvenidas

- 🐛 **Bug fixes**: Corrección de errores
- ✨ **Features**: Nuevas funcionalidades
- 📚 **Documentación**: Mejoras en documentación
- 🎨 **UI/UX**: Mejoras en diseño e interfaz
- ⚡ **Performance**: Optimizaciones de rendimiento
- 🔒 **Security**: Mejoras de seguridad
- 🧪 **Tests**: Nuevas pruebas o mejoras

### Convenciones de Código

#### Python/Django
```python
# Bueno
def calcular_total_venta(items, descuento=0):
    """
    Calcula el total de una venta aplicando descuento.
    
    Args:
        items (list): Lista de items de venta
        descuento (Decimal): Descuento a aplicar
    
    Returns:
        Decimal: Total calculado
    """
    subtotal = sum(item.subtotal for item in items)
    return subtotal - descuento

# Malo
def calc(i, d=0):
    return sum(x.subtotal for x in i) - d
```

#### HTML/Templates
```html
<!-- Bueno -->
<div class="card shadow-sm">
    <div class="card-header bg-primary text-white">
        <h5 class="mb-0">{{ titulo }}</h5>
    </div>
    <div class="card-body">
        {{ contenido }}
    </div>
</div>

<!-- Malo -->
<div class="card">
    <div class="card-header">{{ titulo }}</div>
    <div class="card-body">{{ contenido }}</div>
</div>
```

#### JavaScript
```javascript
// Bueno
function actualizarCarrito(productoId, cantidad) {
    const datos = {
        producto_id: productoId,
        cantidad: cantidad,
        csrfmiddlewaretoken: getCsrfToken()
    };
    
    return fetch('/carrito/actualizar/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    });
}

// Malo
function upd(id, qty) {
    fetch('/carrito/actualizar/', {
        method: 'POST',
        body: JSON.stringify({producto_id: id, cantidad: qty})
    });
}
```

### Estructura de Commits

Usar [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan funcionalidad)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `chore:` Tareas de mantenimiento

Ejemplos:
```bash
git commit -m "feat: agregar filtro por fecha en reportes de ventas"
git commit -m "fix: corregir cálculo de IGV en checkout"
git commit -m "docs: actualizar guía de instalación"
```

### Proceso de Review

1. **Automated Checks**: El PR debe pasar todas las validaciones automáticas
2. **Code Review**: Al menos un revisor debe aprobar los cambios
3. **Testing**: Verificar que no se rompen funcionalidades existentes
4. **Documentation**: Actualizar documentación si es necesario

### Configuración del Entorno de Desarrollo

1. **Instalar dependencias de desarrollo**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-django coverage
   ```

2. **Configurar pre-commit hooks** (opcional)
   ```bash
   pip install pre-commit
   pre-commit install
   ```

3. **Ejecutar tests antes de commit**
   ```bash
   python manage.py test
   python validate_system_flows.py
   ```

### Reportar Issues

Al reportar un bug o solicitar una feature:

1. **Usar templates apropiados**
2. **Incluir información del entorno**:
   - Versión de Python
   - Versión de Django
   - Sistema operativo
   - Navegador (si aplica)

3. **Pasos para reproducir** (para bugs)
4. **Comportamiento esperado vs actual**
5. **Screenshots** si es relevante

### Código de Conducta

- Ser respetuoso y constructivo
- Enfocarse en el código, no en las personas
- Aceptar feedback de manera positiva
- Ayudar a otros estudiantes y colaboradores

### Recursos Útiles

- [Documentación de Django](https://docs.djangoproject.com/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Stripe API Documentation](https://stripe.com/docs/api)

### Contacto

Para preguntas sobre contribuciones:
- **Issues**: [GitHub Issues](https://github.com/laynes-echavez/UPN-RossCrafts/issues)
- **Discussions**: [GitHub Discussions](https://github.com/laynes-echavez/UPN-RossCrafts/discussions)

---

**¡Gracias por contribuir al proyecto Ross Crafts! 🎓**