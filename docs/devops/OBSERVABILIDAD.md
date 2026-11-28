
# Monitoreo y observabilidad — E3

## 1. Herramientas implementadas

| Herramienta | Función |
|---|---|
| Prometheus Client | Instrumentación de FastAPI. |
| Prometheus | Recopilación y almacenamiento de métricas. |
| Grafana | Visualización mediante dashboards. |
| cAdvisor | Monitoreo de recursos de contenedores. |

## 2. Arquitectura

La infraestructura de observabilidad se integra mediante docker-compose.observabilidad.yml, conservando el archivo Docker Compose original de la E2.

Los servicios se comunican mediante la red backend.
Prometheus y Grafana utilizan volúmenes persistentes.

## 3. Instrumentación de la aplicación

El módulo utils/metrics.py registra solicitudes HTTP, códigos de respuesta y duración de las operaciones.

El módulo utils/inventory_metrics.py consulta el estado del inventario utilizando los modelos existentes.

| Endpoint | Intervalo de recopilación |
|---|---|
| /metrics | 15 segundos |
| /metrics/inventario | 60 segundos |

## 4. Métricas recopiladas

- Disponibilidad del endpoint de métricas.
- Estado de las consultas a MySQL.
- Errores HTTP 5xx.
- Productos activos.
- Productos con stock bajo.
- Productos agotados.
- Movimientos de las últimas 24 horas.
- Entradas y salidas de inventario.
- Solicitudes por endpoint.
- Latencia P95.
- CPU por contenedor.
- Memoria por contenedor.

Las métricas de stock consideran productos activos y agregan las existencias de todas sus ubicaciones.

## 5. Dashboard

El dashboard Despensa Inteligente - Observabilidad contiene 12 paneles distribuidos en tres secciones:

1. Estado operacional.
2. Estado y actividad del inventario.
3. Rendimiento e infraestructura.

Su configuración se encuentra versionada en:

monitoring/grafana/dashboards/despensa-observabilidad.json

La fuente de datos y el dashboard se aprovisionan automáticamente mediante archivos de configuración.

## 6. Alarmas

| Alarma | Condición | Duración |
|---|---|---|
| APINoDisponible | Fallo de recopilación de métricas de FastAPI | 30 segundos |
| MySQLNoDisponible | Fallo en las consultas de inventario | 60 segundos |

Las reglas se evalúan cada 15 segundos y se encuentran definidas en monitoring/prometheus/alerts.yml.

Se realizó una prueba controlada deteniendo FastAPI.
Prometheus activó la alarma APINoDisponible y volvió al estado INACTIVE después de recuperar el servicio.

La alarma de MySQL está configurada, pero su activación independiente todavía no se ha demostrado.

## 7. Validaciones realizadas

| Indicador | Resultado |
|---|---|
| Targets de Prometheus | 4 disponibles |
| Productos activos de prueba | 4 |
| Productos con stock bajo | 2 |
| Productos agotados | 1 |
| Movimientos registrados | 5 |
| Entradas | 4 |
| Salidas | 1 |
| Pruebas automatizadas aprobadas | 137 |
| Cobertura global | 93,22% |
| Cobertura mínima exigida | 80% |

Las pruebas automatizadas incluyen la validación de métricas HTTP, métricas de inventario y el comportamiento ante errores de consultas a la base de datos.

## 8. Evidencias

Las capturas de las validaciones se encuentran en el directorio capturas/E3/.

