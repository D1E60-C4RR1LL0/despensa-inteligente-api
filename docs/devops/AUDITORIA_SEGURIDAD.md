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
| certifi | [GHSA-6q48-6c7w-9gw2](https://github.com/advisories/GHSA-6q48-6c7w-9gw2), sin CVE informado en la consulta | 2024.6.2 → 2026.10.18 |

Una comparación local con `packaging.SpecifierSet` confirmó que las versiones propuestas quedan fuera de los rangos afectados de las 50 alertas iniciales. Esto no equivale a un análisis actualizado de todas las dependencias, ni a cierre remoto de las alertas; Snyk y Dependabot deben aportar esa evidencia adicional.

## Registro público y roles

Se reprodujo un fallo de autorización en `/signup`: una petición sin autenticar con `role: admin` recibía HTTP 200. La prueba negativa nueva falló antes de corregirlo, con `200 != 422`.

`UserCreate.role` se restringió a `Literal["user"]`, con `user` como valor predeterminado. Ahora la petición que intenta autoasignar `admin` recibe HTTP 422 y no crea una fila de usuario. El registro sin rol crea un usuario normal. Los administradores existentes y la autorización del endpoint administrativo se conservan; `/signup` no es un mecanismo para otorgar privilegios administrativos.

Se añadieron dos pruebas para estos comportamientos. Es una corrección del código propio, no un CVE atribuido a una dependencia ni un hallazgo que se afirme producido por Snyk.

## Puerta de seguridad del pipeline

`seguridad` ejecuta Snyk Code sobre el código y Snyk Open Source sobre `requirements-dev.txt`, que incluye también las dependencias de ejecución. La SCA de Snyk valida esta rama mientras Dependabot refleja principalmente el estado de `main`.

Los comandos fijados son:

```bash
snyk code test --severity-threshold=high --json-file-output=.security-reports/snyk-code.json
snyk test --file=requirements-dev.txt --package-manager=pip --command=python --severity-threshold=high --json-file-output=.security-reports/snyk-dependencies.json
```

El job `imagen` depende de `pruebas` y `seguridad`. No hay `continue-on-error` en los análisis. Un hallazgo sobre el umbral, autenticación inválida, falta de token u otro error del analizador impide construir y ejecutar la auditoría de contenedores. Un error de análisis no se registra como ausencia de vulnerabilidades.

Los JSON se conservan como artefactos cuando se generan, incluso tras un fallo, durante 14 días. Snyk Code puede no generar JSON si no encuentra incidencias; la ausencia del archivo por sí sola no acredita un análisis correcto: debe comprobarse el código de salida y el log del paso.

Las acciones oficiales se fijaron por SHA y se actualizaron a versiones verificadas con Node 24 para resolver las advertencias observadas en los CI anteriores. Snyk CLI se fija en v1.1308.3 mediante la acción oficial de setup. El token solo se inyecta en el guard de configuración y los pasos de análisis; no en pip ni en la construcción Docker.

Referencias: [Snyk Code](https://docs.snyk.io/developer-tools/snyk-cli/commands/code-test), [Snyk test](https://docs.snyk.io/developer-tools/snyk-cli/commands/test) y [autenticación CLI/CI](https://docs.snyk.io/developer-tools/snyk-cli/authenticate-to-use-the-cli).

## Cuenta y secretos

El usuario creó una cuenta Snyk y habilitó Snyk Code. Se comprobaron los nombres `SNYK_TOKEN` en los almacenes de Actions y Dependabot, sin leer su valor. Se configuró la variable no secreta `SNYK_ORG=d1e60-c4rr1ll0`, tomando el slug visible en la captura facilitada por el usuario. Su autenticación y selección efectiva deben verificarse en la ejecución real.

Los PR de Dependabot utilizan su almacén de secretos, por eso ambos deben contener el mismo token. El valor no se escribe en el repositorio, en `.env` ni en el chat. Las renovaciones deben actualizar ambos almacenes antes de la caducidad del PAT. La cuenta Free tiene límites de pruebas: consultar el [plan vigente de Snyk](https://snyk.io/plans/).

## Evidencia y trabajo pendiente

- Instalación de las dependencias propuestas: correcta.
- Comparación contra los rangos de las 50 alertas iniciales: ninguna versión propuesta dentro de esos rangos.
- Suite local: **61 passed, 4 warnings in 31.49s**.
- Corrección de roles: prueba negativa fallida antes del cambio y aprobada después.
- Imagen con dependencias y roles corregidos: construida correctamente, identificador `sha256:0892287e78c69b36b7c72da47dba2fef2bbda3a0f368ecc4c8cea7da1ee0e595`. La auditoría Compose terminó con código 0: imagen solicitada utilizada, arranque/API correctos, esquema de 9 tablas sin diferencias, persistencia tras recrear contenedores y bloqueo ante migración fallida. Sus recursos temporales se eliminaron.
- Análisis real de Snyk, prueba de su bloqueo y CI de esta rama: pendientes hasta ejecutar el PR. No se declara IE3 completo mientras falte esa evidencia.

No se ha medido aún el cumplimiento de todos los parámetros de escalabilidad de IE3 ni se ha implantado el despliegue automático de IE4. Las reflexiones individuales y justificaciones académicas deben ser elaboradas por el equipo según la pauta.
