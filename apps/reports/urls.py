from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # APIs para gráficos
    path('api/ventas-semana/', views.ventas_semana_api, name='ventas_semana_api'),
    path('api/top-productos/', views.top_productos_api, name='top_productos_api'),
    
    # Reportes
    path('reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('reportes/stock/', views.reporte_stock, name='reporte_stock'),
    path('reportes/clientes/', views.reporte_clientes, name='reporte_clientes'),
    
    # Exportar
    path('reportes/ventas/pdf/', views.reporte_ventas_pdf, name='reporte_ventas_pdf'),
    path('reportes/ventas/excel/', views.reporte_ventas_excel, name='reporte_ventas_excel'),
    path('reportes/stock/excel/', views.reporte_stock_excel, name='reporte_stock_excel'),
]
