# Despliegue simulado — Evaluación 2

Fecha: 29 de octubre de 2026. Rama: `feature/e2-despliegue`, creada desde `develop` en `3fc4f753a248ce04c2f0aa9e6f74f7b871bf31ee`. Documento de asistencia técnica elaborado con Codex; el equipo debe verificar las fuentes y redactar sus propias justificaciones y reflexiones académicas.

## Fuentes y alcance

La pauta oficial `EP2_DOY0101_Estudiante.pdf`, p. 2, solicita despliegue automático en un entorno simulado, permite Docker Compose y exige documentar pipeline, trazabilidad y calidad en el README. La rúbrica, p. 5, evalúa el despliegue completo y trazable en IE4. No exige contratar una nube ni mantener una URL pública.

La semana 2, p. 24 y 26, explica ambientes y condiciones por rama; las semanas 6, p. 8–9, y 7, p. 27–31 y 37, desarrollan Compose y su uso en un nodo. La semana 9, p. 22, sitúa el despliegue después de las puertas de calidad. Se mantienen FastAPI, MySQL y Alembic, sin añadir servicios ajenos a la API.

Transferir la imagen entre runners mediante un artefacto, comprobar su ID y revisión OCI, y conservar un JSON son adaptaciones del proyecto para demostrar la trazabilidad requerida. Los nombres de ambientes, las retenciones y las dos pruebas de identidad son decisiones de implementación, no exigencias literales de la pauta. Referencias técnicas: [artefactos entre jobs](https://docs.github.com/en/actions/tutorials/store-and-share-data) y [ambientes de GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

## Base integrada y verificada

El [PR de seguridad #12](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/12) se marcó listo y se integró en `develop` comprobando el SHA exacto de su última actualización documental. El commit de merge es `3fc4f753a248ce04c2f0aa9e6f74f7b871bf31ee`.

El [CI posterior al merge](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40871513844) aprobó `pruebas`, `seguridad` e `imagen` antes de crear esta rama. Esa ejecución corresponde al workflow anterior de tres jobs; no se atribuye a ella el despliegue nuevo.

## Comportamiento del pipeline

El workflow conserva pruebas y Snyk en paralelo. `imagen` espera que ambos aprueben, construye una sola imagen con etiqueta SHA y añade `org.opencontainers.image.revision` con el commit probado. Ejecuta la auditoría Compose existente sobre esa imagen y solamente después exporta el tar y su identificador de Docker.

El nuevo job `despliegue` depende de `imagen`, descarga el artefacto del mismo workflow, carga la imagen y ejecuta `scripts/deploy_simulated.py`. No reconstruye la imagen ni obtiene una etiqueta mutable desde un registry.

| Evento | Ambiente simulado | Commit probado |
|---|---|---|
| PR hacia `develop` o `main` | `revision-simulada` | Integración temporal del PR, identificada por `github.sha` |
| Push a `develop` | `staging-simulado` | Commit integrado en `develop` |
| Push a `main` | `produccion-simulada` | Commit integrado en `main`, cuando se entregue E2 |

Los PR permiten verificar el mecanismo antes del merge. La ejecución por push proporciona el despliegue automático después de integrar. Cada ejecución usa un proyecto Compose nuevo y datos propios dentro del runner; los nombres de ambiente describen la etapa del flujo, no servidores persistentes ni una producción pública.

## Validación y limpieza

El script rechaza una imagen cuyo ID difiera del build o cuya revisión OCI difiera del commit indicado, antes de crear recursos Compose. Las pruebas unitarias nuevas comprueban ambos rechazos y la generación de un informe de fallo.

Si la identidad coincide, genera credenciales aleatorias en un archivo temporal, levanta el Compose existente con `--no-build`, espera salud y migraciones, y comprueba que API y migraciones usen exactamente la imagen recibida. Después valida por HTTP el contrato OpenAPI, el registro de un usuario normal, el login y la creación/lectura de una categoría en MySQL.

El proyecto, red y volumen reciben un nombre aleatorio de esta ejecución. El bloque de limpieza elimina únicamente esos recursos, incluso ante un error de validación. Un fallo de limpieza impide informar éxito. Los secretos, contraseñas y JWT no forman parte del reporte; tampoco se suben `.env`, configuraciones completas de contenedores ni volúmenes. Una cancelación forzada puede impedir la limpieza programada; en GitHub se descarta además el runner alojado al finalizar el job.

La simulación termina al retirar sus recursos. La dirección de la API solo es accesible en el runner durante el job. El informe distingue este ciclo temporal de un servicio permanente.

## Evidencias de trazabilidad

`deployment/report.json` registra ambiente, evento, ref, commit, URL/intento de Actions, etiqueta e ID de imagen, proyecto, fechas, comprobaciones funcionales y resultado de limpieza. Se conserva también un resumen en la página de ejecución de Actions.

La imagen se transfiere como `api-image-<SHA>` con retención de 1 día. El reporte se publica como `deployment-<SHA>` con retención de 30 días; su subida se intenta también ante un fallo y la ausencia del archivo hace fallar ese paso. Los informes Snyk conservan su retención independiente de 14 días. El equipo debe descargar la evidencia necesaria antes de su vencimiento.

La cadena verificable es: PR/commit → ejecución de Actions → pruebas y seguridad → imagen validada → tar del mismo workflow → ID/revisión de la imagen desplegada → operaciones HTTP/MySQL → reporte. En PR el SHA corresponde a la integración temporal; en push corresponde al commit integrado en la rama.

## Comprobaciones de este bloque

- Suite local: **63 passed, 4 warnings in 33.88s**. Se mantienen las 61 pruebas anteriores y se añaden dos pruebas de rechazo de identidad. Los cuatro avisos de rollback ya existían.
- Sintaxis YAML: leída correctamente; eventos push a `develop`/`main` y cuatro jobs declarados.
- Imagen local de revisión: construida con ID `sha256:1ad7e742600b0d1e3ff4b8eb2c17d2b32e9da4c89f6a5d361c7983ea0e94e7d5`. Su etiqueta OCI corresponde al código de API de la base `3fc4f753a248ce04c2f0aa9e6f74f7b871bf31ee`, sin cambios funcionales de API en este bloque.
- Despliegue local: correcto, proyecto `inventory-deploy-9e25ae46a69b`, con identidad de imagen/commit, migraciones, salud, OpenAPI, registro, login y escritura/lectura en MySQL aprobados. El reporte informó `status: success` y `cleanup: success`; quedó en `deployment/local-report.json`, ignorado por Git. Sus credenciales temporales y recursos propios se retiraron.
- Transferencia entre runners y ejecución del nuevo job en GitHub: pendientes de abrir el PR y comprobar sus resultados. La configuración por sí sola no acredita esos resultados.

## Pendientes de la entrega

La integración de este bloque y la ejecución automática por push deben verificarse antes de declarar completado su recorrido hacia la rama de entrega. También siguen pendientes la activación de la planificación Dependabot al llegar a `main`, la revisión de las políticas de calidad y los parámetros de escalabilidad/gobernanza de IE3 e IE5. Este bloque no declara un 100% global de la rúbrica.
