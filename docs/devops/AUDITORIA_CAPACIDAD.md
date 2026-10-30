# Comparación de capacidad de la API — E2

Fecha: 30 de octubre de 2026. Documento de asistencia elaborado con Codex. El equipo debe verificar los resultados y formular sus propias justificaciones académicas, conclusiones y reflexiones.

## Fuente y alcance

La rúbrica de `EP2_DOY0101_Estudiante.docx`, tabla de IE3/IE5, evalúa ajuste de parámetros de escalabilidad/desempeño y orquestación eficiente, escalable y estable. Sus descriptores coinciden con los del PDF previamente revisado. El DOCX original está fuera de Git, en Descargas; SHA-256 `10db079f3b8f28281ef8f5ad3989573c67a24c3b54ec9983d6a7746eae450cc5`.

La actividad `2.2.1 Docker Compose.pdf`, pp. 3 y 13, y `semana-7.pdf`, pp. 23, 35–37, enseñan límites por ambiente, medición y alcance de Compose en un host. Esta comparación de dos presupuestos es una adaptación del proyecto para aportar evidencia de ajuste de capacidad vertical. La pauta no prescribe las cifras, el número de peticiones ni una mejora porcentual obligatoria. No se incorpora otra plataforma.

## Método reproducible

| Variable | Valor |
|---|---|
| Presupuesto `standard` de API | 0,5 CPU y 192 MiB |
| Presupuesto `expanded` de API | 1 CPU y 384 MiB |
| MySQL | 1 CPU y 768 MiB en las cuatro repeticiones |
| Migraciones | 0,5 CPU y 192 MiB en las cuatro repeticiones |
| Imagen y aplicación | Mismo ID y revisión OCI, sin reconstruir entre repeticiones |
| Datos por repetición | Base vacía propia; una categoría, una ubicación, 24 productos activos con mínimo 5 y stock 2 por producto |
| Preparación | Registro/login, comprobaciones funcionales existentes y 16 consultas de calentamiento |
| Carga medida | 2.400 GET, 8 clientes concurrentes; 600 por endpoint: productos, stock, alertas y lista de compras |
| Orden | `standard`, `expanded`, `expanded`, `standard`; dos repeticiones por presupuesto |
| Medición | Tiempo monotónico del cliente, latencias media/p50/p95/máxima y solicitudes completadas por segundo; Docker stats durante arranque, preparación y carga |

Cada repetición crea un proyecto, puerto, credenciales y volumen propios. Se comprueba el conjunto completo de productos y las cantidades de cada respuesta; una respuesta HTTP correcta con inventario incompleto o equivocado falla. Todas las operaciones medidas son lecturas. El tiempo de carga excluye arranque, siembra y calentamiento; incluye planificación del cliente y transporte/validación HTTP. No se aplican reintentos para ocultar errores.

La carga usa un modelo de solicitudes cerradas: hasta ocho en vuelo y un total fijo. No reproduce una tasa externa constante ni mide la capacidad máxima sostenible. p95 usa el rango superior correspondiente al 95% de las observaciones ordenadas. El resumen compara la mediana de rendimiento y la mediana de p95 de las dos repeticiones por presupuesto; ese último valor no es un p95 agrupado de todas las solicitudes.

## Controles del pipeline

`scripts/compare_capacity.py` reutiliza el despliegue existente con sobreescrituras Compose temporales limitadas a la API. Comprueba cuatro informes, mismo commit/imagen/caso, todas las respuestas correctas, cuotas efectivas, recursos constantes de MySQL/migraciones, ausencia de OOM/reinicios observados, muestras de API/MySQL y limpieza correcta. Un fallo impide aprobar el job obligatorio `despliegue`.

Se conserva `capacity-<SHA>` durante 30 días, con el informe conjunto y los cuatro informes individuales. Se mantiene también el reporte de despliegue habitual. El timeout del job pasa de 12 a 18 minutos para incluir las cuatro ejecuciones. Los resultados solo contienen métricas y campos de inspección permitidos; no se conservan contraseñas, JWT ni configuración interpolada.

La comparación no exige que el presupuesto ampliado gane: un resultado más lento también debe registrarse. Los casos aislados comprueban el rechazo de comparaciones inválidas y que una medición desfavorable no se cambie artificialmente en mejora.

## Repetición local

Con Docker disponible y una imagen construida con revisión OCI, desde la raíz:

```powershell
$revision = git rev-parse HEAD
docker build --label "org.opencontainers.image.revision=$revision" --tag inventory-api:capacity-review .
$imageId = docker image inspect --format '{{.Id}}' inventory-api:capacity-review
.\venv\Scripts\python.exe scripts/compare_capacity.py --image inventory-api:capacity-review --expected-image-id $imageId --commit $revision --environment local-capacity --output deployment/capacity-local.json
```

El informe conjunto conserva las cuatro ejecuciones y sus identidades. Se exige la misma carga y versión en las cuatro; cambiar una de ellas invalida la comparación.

## Resultados locales observados

Se midió la imagen de aplicación de `develop` en `79b38132a908fde7207db64702c77087d34aee9f`, ID `sha256:e810cee0d59dd85c6b5736164a9ec8a0c06b9161c56848e02d83ba881000f8ec`, utilizando los scripts de esta rama. Docker Engine 27.2.0 y Compose v2.29.2-desktop.2. Inicio/fin: 30-10-2026, 21:54:52–22:02:18 UTC (18:54:52–19:02:18 en Santiago). Esta medición previa al commit no se atribuye a una imagen de un commit futuro.

| Orden y perfil | Consultas correctas | Tiempo de carga (s) | Solicitudes/s | p95 (ms) |
|---|---:|---:|---:|---:|
| 1 — standard | 2.400/2.400 | 85,378 | 28,110 | 414,926 |
| 2 — expanded | 2.400/2.400 | 52,635 | 45,597 | 321,185 |
| 3 — expanded | 2.400/2.400 | 54,761 | 43,827 | 329,897 |
| 4 — standard | 2.400/2.400 | 117,656 | 20,398 | 727,099 |

El [resumen JSON local](evidencias/capacidad-local.json) conserva cuotas declaradas/efectivas, resultados, conteos de muestras, imagen y fechas. Las cuatro repeticiones aprobaron diez comprobaciones cada una, sin errores HTTP/de datos, OOM/reinicios observados ni errores de muestreo, y con limpieza correcta. Cada perfil completó 4.800 lecturas medidas, además de preparación y calentamiento.

La mediana del rendimiento por repetición fue **24,254 solicitudes/s** para standard y **44,712** para expanded: relación observada **1,843**. La mediana del p95 por repetición fue **571,013 ms** y **325,541 ms**, respectivamente. La variación entre las dos repeticiones standard es visible; no se oculta ni se interpreta como mejora causal garantizada. Los resultados aportan evidencia de operación correcta con dos presupuestos y diferencias observadas de desempeño para esta carga.

La suite completa local posterior terminó con **134 aprobaciones y cuatro avisos de rollback ya existentes**, en 75,42 segundos. Cobertura global de sentencias de API: **856/923 = 92,74%**, con mínimo del proyecto de 80%. Son 34 comprobaciones aisladas y 100 de integración/configuración; el porcentaje sigue midiendo la API, no estos scripts. Los once casos nuevos rechazan imagen/carga/cuotas/limpieza inválidas, respuestas HTTP con datos equivocados y verifican el cálculo de métricas sin convertir un presupuesto más lento en una mejora ficticia.

La ejecución remota y el estado de integración se verifican en el PR de `feature/e2-capacidad-compose` y en el push posterior a `develop`. El pipeline conserva `capacity-<SHA>`; una configuración de CI no sustituye la revisión del artefacto generado.

## Límites de interpretación

Se ajustan CPU y memoria juntas; una diferencia observada no permite atribuir por separado el efecto de cada recurso. Dos repeticiones por presupuesto y orden alternado reducen la dependencia de una única ejecución, pero no constituyen un estudio estadístico. El cliente, Docker y otros procesos comparten host; los resultados locales y de Actions deben interpretarse por separado.

Docker stats entrega muestras espaciadas, no picos garantizados; la memoria CLI de Linux descuenta caché inactiva. Distinguir en los informes muestras de arranque, preparación y `capacity_measured`. La tarea breve de migración puede terminar entre muestras, aunque su salida y cuotas se comprueban.

Esta evidencia refuerza capacidad vertical y estabilidad para la carga especificada en un host. No demuestra escalado horizontal, balanceo, autoscaling, alta disponibilidad, SLA ni el comportamiento de una instalación de gran envergadura. La calificación depende del docente; no se declara un 100% de logro por superar estas comprobaciones.
