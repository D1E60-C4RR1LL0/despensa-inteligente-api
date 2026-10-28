# Seguridad y Dependabot — Evaluación 2

Fecha: 28 de octubre de 2026. Rama: `feature/e2-seguridad`, creada desde `develop` en `a2966e86b84f47575921482fc84649d2982c0d5a`. Asistencia técnica realizada con Codex; el equipo debe validar las fuentes y elaborar sus propias justificaciones académicas.

## Alcance y relación con las clases

La pauta oficial, p. 2, exige Dependabot, análisis de código con SonarQube o Snyk y alertas o bloqueos ante fallos de seguridad. La elección de este proyecto es Dependabot más Snyk, sin incorporar un segundo proveedor SAST.

La semana 10, p. 10–19, explica puertas de seguridad, SCA y SAST; sus ejemplos usan Snyk para dependencias y SonarCloud para código. Se mantiene `snyk test` como SCA y se utiliza `snyk code test` para el análisis de código solicitado por E2. Este segundo comando es una adaptación respaldada por la documentación oficial de Snyk; no se presenta como un comando mostrado literalmente en esas clases. Los secretos siguen el contenido de la semana 2. El umbral `high` es la política elegida para este proyecto, no un valor impuesto por la pauta.

La configuración y las correcciones de roles/dependencias son controles de este proyecto. Las versiones exactas, el calendario de Dependabot y el pin de acciones son decisiones verificadas de implementación; no son nuevos requisitos académicos. DAST, infraestructura adicional y despliegue permanente permanecen fuera de este bloque.

## Punto de partida verificado

Se integró el [PR Compose #7](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/7) después de comprobar sus checks y el commit exacto. El [CI posterior en develop](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40625067399) terminó correctamente antes de crear esta rama.

El repositorio público tenía secret scanning y push protection activados, pero sus alertas y actualizaciones de seguridad Dependabot estaban desactivadas. Se activaron mediante la API de GitHub y se verificó el estado: actualizaciones habilitadas y no pausadas. El grafo de dependencias devolvió 49 paquetes en la consulta inicial.

Tras inicializarse las alertas, GitHub reportó **50 hallazgos: 4 críticos, 19 altos, 20 medios y 7 bajos**. Estos son resultados reales del repositorio, no vulnerabilidades inventadas para la evaluación. La evidencia condensada está en [dependabot-linea-base.csv](evidencias/dependabot-linea-base.csv), con identificadores CVE cuando existen, GHSA, rangos afectados, versión inicial, propuesta y enlace de la fuente.

## Configuración Dependabot

`.github/dependabot.yml` propone revisiones semanales para pip y las acciones de GitHub, con PR de versiones dirigidos a `develop` y límites de 3 y 2 PR abiertos respectivamente. No realiza merges automáticos.

Hay una distinción importante: GitHub lee este archivo desde la rama predeterminada, que sigue siendo `main`. La planificación de actualizaciones de versión quedará operativa cuando el archivo llegue a esa rama mediante el flujo de entrega. Las actualizaciones de seguridad y alertas ya activadas son independientes de esa espera y siguen el estado de la rama predeterminada. Por tanto, integrar correcciones en `develop` no implica que las alertas de `main` desaparezcan inmediatamente. Esto se debe comprobar al publicar la versión estable de E2.

Referencia: [opciones de Dependabot y target-branch](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).

## Correcciones de dependencias

Se actualizaron las versiones afectadas de AnyIO, certifi, dnspython, h11, idna, Jinja2, Mako, orjson, Pygments, PyJWT, python-dotenv, python-multipart, Starlette, ujson y pytest. HTTPcore, FastAPI y pytest-asyncio se ajustaron por compatibilidad con las versiones corregidas. Las versiones propuestas se verificaron contra los metadatos de [PyPI](https://pypi.org/) y los rangos de los avisos de GitHub.

Se seleccionó FastAPI 0.133.1 porque sus metadatos permiten la versión corregida de Starlette conservando Pydantic 2.7.4. La resolución de pip y las pruebas de regresión comprobaron la compatibilidad; no se incorporaron componentes de observabilidad ni nuevas bases de datos.

Ejemplos de los hallazgos críticos de la línea base:

| Paquete | Identificador observado | Versión inicial → propuesta |
|---|---|---|
| h11 | [CVE-2025-43859 / GHSA-vqfr-h8mv-ghfj](https://github.com/advisories/GHSA-vqfr-h8mv-ghfj) | 0.14.0 → 0.16.0 |
| AnyIO | [CVE-2026-63374 / GHSA-82r6-8w77-94w6](https://github.com/advisories/GHSA-82r6-8w77-94w6) | 4.4.0 → 4.14.2 |
| PyJWT | [CVE-2026-102268 / GHSA-ffc3-869f-jxw9](https://github.com/advisories/GHSA-ffc3-869f-jxw9) | 2.8.0 → 2.15.0 |
| certifi | [GHSA-6q48-6c7w-9gw2](https://github.com/advisories/GHSA-6q48-6c7w-9gw2), sin CVE informado en la consulta | 2024.6.2 → 2026.10.19 |

Una comparación local con `packaging.SpecifierSet` confirmó que las versiones propuestas quedan fuera de los rangos afectados de las 50 alertas iniciales. Esto no equivale a un análisis actualizado de todas las dependencias, ni a cierre remoto de las alertas; Snyk y Dependabot deben aportar esa evidencia adicional.

## Registro público y roles

Se reprodujo un fallo de autorización en `/signup`: una petición sin autenticar con `role: admin` recibía HTTP 200. La prueba negativa nueva falló antes de corregirlo, con `200 != 422`.

`UserCreate.role` se restringió a `Literal["user"]`, con `user` como valor predeterminado. Ahora la petición que intenta autoasignar `admin` recibe HTTP 422 y no crea una fila de usuario. El registro sin rol crea un usuario normal. Los administradores existentes y la autorización del endpoint administrativo se conservan; `/signup` no es un mecanismo para otorgar privilegios administrativos.

Se añadieron dos pruebas para estos comportamientos. Es una corrección del código propio, no un CVE atribuido a una dependencia ni un hallazgo que se afirme producido por Snyk.

## Puerta de seguridad del pipeline

`seguridad` ejecuta Snyk Code sobre el código y Snyk Open Source sobre `requirements-dev.txt`, que incluye también las dependencias de ejecución. La SCA de Snyk valida esta rama mientras Dependabot refleja principalmente el estado de `main`.

Los comandos fijados son:

```bash
set -o pipefail
snyk code test --severity-threshold=high --json | tee .security-reports/snyk-code.json
snyk test --file=requirements-dev.txt --package-manager=pip --command=python --severity-threshold=high --json | tee .security-reports/snyk-dependencies.json
```

El job `imagen` depende de `pruebas` y `seguridad`. No hay `continue-on-error` en los análisis. Un hallazgo sobre el umbral, autenticación inválida, falta de token u otro error del analizador impide construir y ejecutar la auditoría de contenedores. Un error de análisis no se registra como ausencia de vulnerabilidades.

Los resultados se solicitan mediante `--json` y se capturan con `tee` para conservarlos como artefactos, incluso tras un fallo, durante 14 días. `pipefail` conserva el fallo de Snyk aunque `tee` termine correctamente. La ausencia de resultados o un archivo vacío no acredita un análisis correcto: deben comprobarse el código de salida y el contenido. Las primeras ejecuciones no subieron informes: `upload-artifact` excluye por defecto las carpetas ocultas. Se habilitó `include-hidden-files` únicamente sobre el patrón `.security-reports/*.json`, se captura explícitamente la salida y se establece error si no se encuentran archivos. Esto no incluye otros archivos ocultos del repositorio.

Las acciones oficiales se fijaron por SHA y se actualizaron a versiones verificadas con Node 24 para resolver las advertencias observadas en los CI anteriores. Snyk CLI se fija en v1.1308.3 mediante la acción oficial de setup. El token solo se inyecta en el guard de configuración y los pasos de análisis; no en pip ni en la construcción Docker.

Referencias: [Snyk Code](https://docs.snyk.io/developer-tools/snyk-cli/commands/code-test), [Snyk test](https://docs.snyk.io/developer-tools/snyk-cli/commands/test) y [autenticación CLI/CI](https://docs.snyk.io/developer-tools/snyk-cli/authenticate-to-use-the-cli).

## Cuenta y secretos

El usuario creó una cuenta Snyk y habilitó Snyk Code. Se comprobaron los nombres `SNYK_TOKEN` en los almacenes de Actions y Dependabot, sin leer su valor. Se configuró la variable no secreta `SNYK_ORG=d1e60-c4rr1ll0`, tomando el slug visible en la captura facilitada por el usuario y confirmado después mediante la URL de su organización. La autenticación y la selección de organización quedaron verificadas por los análisis reales de CI descritos a continuación.

Los PR de Dependabot utilizan su almacén de secretos, por eso ambos deben contener el mismo token. El valor no se escribe en el repositorio, en `.env` ni en el chat. Las renovaciones deben actualizar ambos almacenes antes de la caducidad del PAT. La cuenta Free tiene límites de pruebas: consultar el [plan vigente de Snyk](https://snyk.io/plans/).

## Primera ejecución real y bloqueo verificado

Se abrió el [PR #12 en borrador](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/12). En la [primera ejecución de CI](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628001505), sobre `bbd3ed86be9827641fec3ff4925517a41fbdf923`, la cuenta y organización funcionaron, las pruebas aprobaron y Snyk Code terminó con 0 incidencias sobre el umbral configurado. Esto no informa el total de incidencias de severidad inferior.

La SCA analizó 52 dependencias y encontró una incidencia crítica en cuatro rutas: [SNYK-PYTHON-CERTIFI-21280764](https://security.snyk.io/vuln/SNYK-PYTHON-CERTIFI-21280764), que afecta también a la propuesta inicial `certifi==2026.10.18`. Snyk terminó con código 1 y `imagen` quedó omitida. Esta ejecución demuestra el bloqueo ante un hallazgo real, sin introducir código vulnerable artificialmente ni confundir un error de autenticación con una vulnerabilidad.

Se ajustó certifi a `2026.10.19`, versión corregida indicada por Snyk y verificada en PyPI. Este hallazgo adicional ilustra por qué comparar con los 50 rangos iniciales no sustituía el escaneo actualizado.

El [CI de la corrección](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628304613), sobre `38d4a7158791c2a99b94b42404ab01408fe5868c`, aprobó los tres jobs: 61 pruebas, los dos análisis y la construcción/auditoría Compose. La SCA revisó 52 dependencias sin incidencias sobre el umbral y Compose informó `all_checks_pass: true` sobre la imagen `sha256:8bf9b2b87467f7ed6eaab26b0443f4584c85e6dda9151da6588ab68dd1ecc536`. Los resultados de esa ejecución quedaron en el log. La siguiente ejecución verificó además la subida de los JSON tras corregir la inclusión de carpetas ocultas.

## CI final del bloque y artefactos verificados

El [CI 40628651678](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628651678), correspondiente al commit de la rama `b61f553c79ca22584c740e5d17ea95b82e4bb928`, terminó con **pruebas, seguridad e imagen aprobados**. Esta es la ejecución de referencia para el código y el workflow revisados antes de esta actualización documental.

- Pruebas: 61 aprobadas.
- Snyk Code: el JSON descargado contiene 0 resultados con el umbral `high` configurado.
- Snyk Open Source: 52 dependencias analizadas; el JSON informa `ok: true`, `uniqueCount: 0` y `vulnerabilities: []` con ese mismo umbral. Estos resultados no acreditan ausencia de incidencias de severidad inferior.
- Docker y Compose: imagen `sha256:3fb57ffd20160f8268268fc8950b7e3bb3bf92bafe543fdbf9f53635065a7951`, con `requested_image_used: true` y `all_checks_pass: true`. Se verificaron arranque/API, esquema, persistencia y bloqueo ante migración fallida usando la imagen construida en CI con certifi 2026.10.19.

Se descargó el [artefacto de seguridad 12790597158](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628651678/artifacts/12790597158) y se verificó que contiene dos archivos JSON válidos: `snyk-code.json` y `snyk-dependencies.json`, con los resultados anteriores. GitHub registra el nombre `snyk-security-88361a06cc29f16bd4b4a6cd10c274585e4781e2` y el digest del archivo ZIP `sha256:c7ca5ffa917927fb2cd0d4ec13cca3cfa38cd4a2d34d86793eaf66c20a5055c6`. El SHA del nombre corresponde al commit de integración temporal que GitHub prueba en el PR; el commit de la rama se identifica arriba.

La retención configurada es de 14 días; GitHub indica vencimiento del artefacto el 11 de noviembre de 2026. Este registro conserva los identificadores, enlaces y resultados verificados, pero la disponibilidad del ZIP depende de esa retención. El PR #12 continúa en borrador hacia `develop` al registrar esta evidencia.

## Evidencia y trabajo pendiente

- Instalación de las dependencias propuestas: correcta.
- Comparación contra los rangos de las 50 alertas iniciales: ninguna versión propuesta dentro de esos rangos.
- Suite local tras la corrección final de certifi: **61 passed, 4 warnings in 32.23s**. `pip check`: sin incompatibilidades.
- Corrección de roles: prueba negativa fallida antes del cambio y aprobada después.
- Imagen local previa al último ajuste de certifi: construida correctamente, identificador `sha256:0892287e78c69b36b7c72da47dba2fef2bbda3a0f368ecc4c8cea7da1ee0e595`. La auditoría Compose terminó con código 0: imagen solicitada utilizada, arranque/API correctos, esquema de 9 tablas sin diferencias, persistencia tras recrear contenedores y bloqueo ante migración fallida. Sus recursos temporales se eliminaron. La imagen con certifi 2026.10.19 se construyó y probó posteriormente en el CI final documentado arriba.
- Primera ejecución real y bloqueo por hallazgo: verificados. CI final tras actualizar certifi: los tres jobs aprobados y los dos informes JSON descargados y verificados. No se declara IE3 completo: la planificación Dependabot aún debe llegar a la rama predeterminada y quedan aspectos de escalabilidad de la rúbrica.

No se ha medido aún el cumplimiento de todos los parámetros de escalabilidad de IE3 ni se ha implantado el despliegue automático de IE4. Las reflexiones individuales y justificaciones académicas deben ser elaboradas por el equipo según la pauta.
