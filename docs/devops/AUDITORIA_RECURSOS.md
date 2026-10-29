# Recursos de Docker Compose — E2

Fecha: 29 de octubre de 2026. Documento de asistencia elaborado con Codex; el equipo debe revisar los datos y formular su propia justificación académica. No sustituye sus conclusiones ni acredita una calificación.

## Relación con la pauta y las clases

| Fuente | Contenido confirmado | Aplicación en este bloque |
|---|---|---|
| `EP2_DOY0101_Estudiante.pdf`, pp. 2 y 5 | Compose o Kubernetes; capacidad/escalabilidad, seguridad/gobernanza y orquestación eficiente y estable en IE3/IE5. | Acotar recursos de los tres servicios existentes y comprobar su aplicación y funcionamiento. La pauta no fija CPU, memoria ni número de réplicas. |
| `2.2.1 Docker Compose.pdf`, pp. 3 y 13 | Límites de CPU/memoria en ejecución/Compose. | Declarar `cpus` y `mem_limit` en Compose. |
| `semana-7.pdf`, pp. 23, 35–37 | Recursos por ambiente, estadísticas, archivos Compose alternativos y alcance de Compose en un host. | Medir antes/después y usar una sobreescritura temporal para repetir la línea base local. |

Los PDF originales están en Descargas, fuera de Git. La automatización Python, los valores seleccionados, el perfil HTTP y los rechazos en CI son adaptaciones de este proyecto. No son exigencias textuales del docente. No se incorpora Kubernetes, otro escáner ni infraestructura pagada.

## Configuración y controles

| Servicio | CPU máxima configurada | Memoria configurada |
|---|---:|---:|
| `db` | 1 | 768 MiB |
| `migrate` | 0,5 | 192 MiB |
| `api` | 0,5 | 192 MiB |

La primera línea base observó hasta 443,20 MiB en MySQL y 72,32 MiB en API. Los presupuestos dejan margen sobre esas muestras; migraciones reutiliza el presupuesto Python y luego se comprobó su ejecución limitada. Son valores iniciales para este escenario académico: deben revisarse si cambia la carga, el volumen de datos o el ambiente. El presupuesto de CPU puede introducir espera por cuota; no representa CPU reservada ni una garantía de rendimiento.

`deploy_simulated.py` mantiene las validaciones de identidad, salud, migraciones y persistencia. Además:

- Rechaza límites ausentes o no positivos antes de levantar Compose.
- Muestrea exclusivamente su proyecto aleatorio con `docker stats --no-stream`, durante arranque y operaciones.
- Ejecuta 40 GET autenticados: diez rondas sobre productos, stock, alertas y lista de compras, después de registro/login y escritura/lectura de una categoría.
- Compara los límites declarados con `HostConfig.NanoCpus` y `HostConfig.Memory` de los tres contenedores; rechaza discrepancias, OOM y reinicios observados.
- Exige muestras de API y MySQL y ausencia de errores de muestreo. La migración breve puede terminar entre muestras: se admite ese caso, pero se exige salida 0 y límites efectivos.
- Conserva medidas, perfil, identidad y limpieza en el reporte existente del job `despliegue`. Un rechazo falla el job obligatorio; no se crea una puerta paralela.

Solo se extraen campos permitidos de la configuración/inspección. No se guardan variables de entorno, contraseñas, JWT ni configuración interpolada en el informe.

## Evidencia local

Imagen de aplicación con revisión OCI `7b84892db37faa5a28e3fd7c7f96e32ae5b7942a` (base del bloque), ID `sha256:6e5a249f197e35ed1a956ad6713dbf71bd6d17462f3e966aafebf8d9f375556d`. Docker Engine 27.2.0, Compose v2.29.2-desktop.2, contenedores Linux en Docker Desktop. Los scripts y Compose son los cambios de esta rama; no se atribuye esta ejecución a una imagen de un commit futuro.

| Servicio | Máximo muestreado base (MiB) | Muestras base | Máximo muestreado limitado (MiB) | Muestras limitado |
|---|---:|---:|---:|---:|
| MySQL | 443,20 | 10 | 442,90 | 10 |
| Migraciones | Sin muestra | 0 | 49,93 | 1 |
| API | 72,32 | 3 | 81,39 | 5 |

Ambas ejecuciones finalizaron con identidad correcta, migraciones/servicios saludables, 40/40 consultas, cero OOM/reinicios observados, sin errores de muestreo y limpieza correcta. Docker confirmó cero límites explícitos en la base y exactamente 1 CPU/768 MiB y 0,5 CPU/192 MiB en la ejecución limitada. La repetición posterior con `--baseline-resources`, sin editar el Compose limitado, también aprobó y confirmó límites cero; observó 452,00 MiB en MySQL y 72,33 MiB en API. El [resumen JSON versionado](evidencias/recursos-locales.json) conserva fechas, identidades, límites y resultados de las tres ejecuciones.

Estas cifras son máximos de muestras espaciadas, no el pico real ni consumo garantizado. En Linux la CLI descuenta caché inactiva al informar memoria ([Docker stats](https://docs.docker.com/reference/cli/docker/container/stats/)); no equivale a toda la memoria contabilizada por el límite. Los porcentajes CPU dependen del intervalo; se verifican las cuotas efectivas mediante Docker, no por exigir que cada muestra respete un porcentaje exacto. El perfil es funcional, secuencial y breve: no es una prueba de estrés, capacidad máxima, concurrencia ni SLA. Las latencias de ejecuciones individuales no demuestran una mejora de rendimiento.

Suite local tras el cambio: **123 aprobaciones**, cero errores/fallos, **92,74%** global de sentencias de la API (856/923), con los cuatro avisos previos de rollback SQLAlchemy. Comprende 23 comprobaciones aisladas y 100 de integración/configuración, más las ejecuciones Docker. Los casos nuevos prueban normalización de unidades, rechazo de límites ausentes/ignorados, OOM/reinicios y prohibición del modo sin límites en CI. La cobertura de API no se presenta como cobertura de estos scripts.

## Repetición y evidencia remota

Actualización de integración: el [PR #15](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/15) se integró en `develop` como `67b6ab1498caeebd31a1c08f500f7bb9206d879f`. Su [push 40937752277](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40937752277) aprobó los cuatro jobs. Se verificaron los ZIP de calidad y despliegue: 123 aprobaciones, cobertura 92,74%, staging con nueve checks verdaderos, cuotas exactas, 40/40 consultas, sin OOM/reinicios observados y limpieza correcta. MySQL/API tuvieron 7/2 muestras, máximos muestreados 456,70/70,95 MiB; migraciones terminó entre muestras con salida 0. La [matriz de cierre](MATRIZ_EVIDENCIAS_E2.md) conserva enlaces y pendientes; los párrafos siguientes describen el procedimiento y las fotografías anteriores a la integración.

Después de construir una imagen con etiqueta OCI del commit que se vaya a validar, obtener su ID y ejecutar desde la raíz:

```powershell
$revision = git rev-parse HEAD
docker build --label "org.opencontainers.image.revision=$revision" --tag inventory-api:resources-review .
$imageId = docker image inspect --format '{{.Id}}' inventory-api:resources-review
.\venv\Scripts\python.exe scripts/deploy_simulated.py --image inventory-api:resources-review --expected-image-id $imageId --commit $revision --environment local-bounded --output deployment/resources-bounded.json
```

Para una comparación local opcional, repetir el último comando con `--baseline-resources`, otro ambiente/nombre de reporte. Esa opción crea un archivo Compose temporal que pone ambos límites en cero, sin modificar el archivo versionado. CI rechaza la opción antes de ejecutar Docker. Cada ejecución usa recursos propios y elimina únicamente su proyecto/volumen temporal.

El workflow existente ejecuta el script actualizado sobre la imagen transferida del mismo CI y conserva `deployment-<SHA>` por 30 días. Verificar en el PR de esta rama los cuatro jobs, `resource_mode: bounded`, límites efectivos, consultas, muestras y limpieza antes del merge; luego comprobar el push a `develop`. No confundir este requisito de revisión con resultados remotos aún no observados en esta fotografía local.

La base `develop` proviene del [PR #14](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/14), cuyo [push 40931904036](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40931904036) aprobó los cuatro jobs y 109 pruebas, cobertura 92,74% y staging correcto. Esa ejecución precede a los límites y no los acredita.

## Alcance pendiente para la entrega

Se demuestra control de recursos y estabilidad en el escenario medido de un host. Compose permite ajustar presupuestos y separar servicios; no se ha demostrado escalado horizontal, balanceo, autoscaling ni recuperación multinodo. Añadir dos réplicas sin necesidad o evidencia no acredita esos resultados. El equipo debe explicar ese alcance frente a IE3/IE5 y consultar al docente si espera una demostración adicional de escalabilidad.

Queda cerrar la matriz de indicadores/evidencias, revisar README y documentación propia del equipo y preparar el PR de entrega hacia `main`. Dependabot programado debe activarse/verificarse al llegar su configuración a la rama predeterminada; las alertas históricas de `main` no se confunden con el análisis Snyk de `develop`. No se declara completado el 100% de la evaluación por este bloque.
