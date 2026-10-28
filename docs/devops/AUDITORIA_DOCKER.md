# Contenerización de la API — Evaluación 2

Fecha: 26 de octubre de 2026. Rama: `feature/e2-docker`, creada desde `develop` en `8bc070391d68cf72d40e91a6bd3d79ed705fc604`. Documento de asistencia técnica elaborado con Codex; el equipo debe revisar los resultados y redactar sus propias justificaciones académicas.

## Alcance y estado

Este bloque implementa el Dockerfile, las exclusiones del contexto, la configuración JWT por entorno y la construcción de imagen en el workflow. La imagen se validó localmente sobre Linux/amd64 con un MySQL temporal. Compose, publicación en registry, análisis de seguridad y despliegue automático siguen pendientes.

Antes de comenzar se verificó el merge del [PR #5](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/5) y el [CI exitoso de develop](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40403273828), correspondientes al commit de base. Esa ejecución no incluye el nuevo job Docker, que aún no se ha ejecutado remotamente.

## Correspondencia con la materia

Contraste realizado el 27 de octubre de 2026 con la pauta oficial y los PDF de clases en Descargas. La pauta define lo evaluado; las decisiones técnicas particulares no deben presentarse como exigencias del docente.

| Implementación | Clasificación y respaldo |
|---|---|
| Dockerfile y construcción de imagen en GitHub Actions | `[E2-OBLIGATORIO]`: pauta, p. 2, IE1. `[CLASE]`: semana 5, p. 22–24; semana 8, p. 5. |
| `.dockerignore` | `[CLASE]`: semana 5, p. 24. Apoya la contenerización; no es un requisito textual separado de la pauta. |
| PyTest y build condicionado a pruebas | `[E2-OBLIGATORIO]`: pruebas en CI, pauta p. 2, IE2. `[CLASE]`: semana 2, p. 15, dependencia con `needs`; semana 8, p. 5–7, puerta de calidad. |
| Variables de entorno y extracción de la clave JWT del código | `[CLASE]`: semana 7, p. 8–10, configuración por entorno y secretos sin versionar; semana 10, p. 9, secretos fuera del código. El nombre `JWT_SECRET_KEY` y sus validaciones son una adaptación de esta API. |
| Healthcheck y persistencia con volumen | `[CLASE]`: semana 6, p. 23–25, healthchecks; semana 7, volúmenes. La instrucción `HEALTHCHECK` en nuestro Dockerfile, el endpoint seleccionado y los valores de tiempo son decisiones de implementación; los ejemplos de clase consultados usan Compose. |
| Imagen `slim`, usuario no root y permisos `contents: read` | `[RECOMENDACIÓN]`: decisiones para la imagen y el workflow. No se identificaron como exigencias textuales independientes ni se confirmó su instrucción literal en los pasajes de clase revisados. |
| Separación de `requirements-dev.txt` e instalación solo de wheels | `[RECOMENDACIÓN]`: decisiones para las dependencias Python y el tamaño de la imagen; no son requisitos textuales del curso. |
| Scripts de auditoría, `docker build --check` y casos concretos de regresión | `[RECOMENDACIÓN]`: comprobaciones y herramientas propias para obtener evidencia. Aplican conceptos de automatización, pruebas y documentación, pero sus archivos, comandos y escenarios exactos no vienen prescritos por la pauta. |
| Corrección de Alembic y Uvicorn como comando de inicio | Adaptaciones del stack ya existente en el repositorio. No deben atribuirse a una exigencia de usar Alembic o Uvicorn en la asignatura. |

La implementación central corresponde a la materia. Los complementos anteriores se registran para que el equipo pueda distinguirlos, comprenderlos y decidir su uso, sin ampliar la lista de obligaciones académicas. El desarrollo siguiente debe conservar esa distinción y evitar herramientas o servicios adicionales sin una necesidad concreta.

## Detalle de archivos

| Archivo | Cambio |
|---|---|
| `Dockerfile` | Imagen Python 3.12 slim, dependencias de ejecución, Alembic, Uvicorn y usuario `app` con UID/GID 10001. |
| `.dockerignore` | Contexto limitado a los archivos necesarios; exclusión de archivos locales incluso dentro de directorios permitidos. |
| `requirements.txt` | Dependencias de ejecución, conservando sus versiones. |
| `requirements-dev.txt` | Incluye las anteriores y las tres dependencias PyTest con sus versiones originales. |
| `.env.example` | Variables necesarias con valores ilustrativos; deja la clave JWT vacía. |
| `utils/utils.py` | Lee `JWT_SECRET_KEY`; rechaza valores ausentes, vacíos o compuestos solo por espacios. |
| `tests/conftest.py` | Genera una clave efímera exclusiva de la suite. |
| `tests/test_jwt_configuration.py` | Cuatro casos de configuración y firma JWT. |
| `scripts/audit_bootstrap.py` | Genera una clave efímera para conservar el aislamiento de la auditoría anterior. |
| `scripts/audit_docker.py` | Prueba la imagen con un MySQL temporal y peticiones HTTP a la API. |
| `.github/workflows/ci.yml` | Pruebas en push a develop y PR a develop/main; build Docker condicionado al éxito de las pruebas. |

El Dockerfile usa `python:3.12-slim-bookworm`, coherente con el Python 3.12 del CI y del proyecto. Primero copia las dependencias para reutilizar esa capa cuando solo cambia el código. Instala wheels con `--only-binary=:all:` y no instala compiladores. No se añadió multi-stage: la construcción comprobada no requirió una etapa de compilación que hubiera que separar de la imagen final.

Solo se copian `app.py`, `alembic.ini`, `requirements.txt` y los directorios de aplicación/migraciones. No se utiliza `COPY . .`. La exclusión del contexto y las copias explícitas se verificaron inspeccionando la imagen. La documentación de [Docker sobre contexto](https://docs.docker.com/build/concepts/context/#dockerignore-files), sus [prácticas de construcción](https://docs.docker.com/build/building/best-practices/) y la guía de [FastAPI en contenedores](https://fastapi.tiangolo.com/deployment/docker/) fueron las referencias técnicas consultadas.

El comando predeterminado es `python -m uvicorn app:app --host 0.0.0.0 --port 8000`. No utiliza modo de desarrollo ni recarga. No aplica migraciones al arrancar: deben ejecutarse como paso explícito, con la misma configuración de base de datos. El contenedor de prueba de migraciones y el servidor utilizaron la misma imagen.

El healthcheck consulta `/openapi.json` con la biblioteca estándar de Python. Verifica respuesta HTTP, no disponibilidad de MySQL. Las peticiones autenticadas de la auditoría verifican por separado el acceso funcional a la base de datos.

## Configuración obligatoria

La API requiere `DATABASE_URL` y `JWT_SECRET_KEY` en el entorno o en el `.env` local. El `.env` no se copia a la imagen. La clave JWT ya no tiene un valor predeterminado en código. Para una sesión local de PowerShell:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Para conservar la clave entre reinicios, configurarla en el `.env` local o en el mecanismo de secretos del entorno. Cambiarla invalida tokens firmados con la anterior. La base y el `.env` existentes del usuario no se modificaron durante este bloque. Al ejecutar la API con la configuración local anterior, hay que incorporar esta nueva variable.

Las pruebas y auditorías generan claves temporales sin publicarlas. Los comandos de construcción no reciben secretos por `ARG` ni `ENV` del Dockerfile. No se añadieron credenciales a archivos versionados.

## Comprobaciones locales ejecutadas

```powershell
docker build --tag inventory-api:e2-docker .
docker build --check .
.\venv\Scripts\python.exe scripts/audit_docker.py
$env:DATABASE_URL = 'sqlite:///:memory:'
.\venv\Scripts\python.exe -m pytest -q -o log_cli=false
.\venv\Scripts\python.exe scripts/audit_bootstrap.py
```

`audit_docker.py` requiere Docker disponible y la imagen `mysql:8.4` descargada. Crea una red propia y un MySQL con datos en `tmpfs`, aplica Alembic desde la imagen de la API y arranca Uvicorn en otro contenedor. Publica un puerto aleatorio solo en `127.0.0.1`. Las credenciales se transmiten mediante variables de entorno y no se muestran en el reporte. Al terminar elimina los contenedores y la red de prueba.

| Comprobación | Resultado observado |
|---|---|
| Construcción Docker | Código 0. |
| Validaciones `docker build --check` | Sin advertencias. |
| Python dentro de la imagen | 3.12.15. |
| Tamaño reportado por Docker | 229706284 bytes, aproximadamente 219 MiB. |
| Contexto de construcción inicial | 78.81 kB. |
| Usuario efectivo | UID 10001, no root. |
| PyTest instalado en la imagen | No. |
| Archivos `.env`, `.env.example`, `.git`, `venv`, `tests`, `ci.db` y `.coverage` en `/app` | Ausentes. |
| MySQL temporal utilizado | 8.4.13. |
| Migración desde la imagen a la base temporal | Correcta. |
| OpenAPI, registro y login por HTTP | Correctos. |
| Productos, stocks, alertas y lista de compras por HTTP | HTTP 200 con listas vacías. |
| Healthcheck de la API | `healthy`. |
| Arranque de la imagen sin JWT_SECRET_KEY | Rechazado con error de configuración, como corresponde. |
| Demostración SQLite con volumen Docker | Migración y registro correctos; dato conservado al detener el servidor y consultar desde otro contenedor. |
| Auditoría anterior de arranque sobre SQLite | Código 0, nueve tablas, cero diferencias y reversión/reconstrucción correctas. |
| Suite completa local | **57 passed, 4 warnings in 26.09s**, código 0. |

Los cuatro avisos de la suite corresponden al rollback de las fixtures existentes, ya documentados en la auditoría de arranque. El aviso conocido de passlib/bcrypt no impidió registro ni login. No se hicieron actualizaciones de versiones de las dependencias heredadas ni un escaneo de vulnerabilidades en este bloque.

Imagen generada:

```text
sha256:8c7f8b82507479450a13cc5d2eb29364164d08e8d81eb6f38783d41bedac4be0
```

Digest de la base Python observado durante la construcción:

```text
sha256:6a0e06f5ba0b373d051aabd3fffb9b873f27f9a2a3a14bcbe37dee6f0e3bbc70
```

La etiqueta de Python mantiene la línea 3.12 y Bookworm, pero admite nuevas versiones de parche. Algunas dependencias transitivas tampoco están fijadas en un lockfile completo; estos identificadores documentan lo realmente probado, sin afirmar que cualquier reconstrucción futura genere bytes idénticos.

## CI y evidencia pendiente

El workflow conserva las pruebas y agrega el job `imagen` con `needs: pruebas`. Si las pruebas fallan, no se construye la imagen. El build utiliza `inventory-api:${{ github.sha }}` para relacionarlo con la ejecución. Los permisos del workflow son `contents: read`.

Se verificaron localmente la sintaxis YAML, la dependencia entre jobs y la construcción efectiva del Dockerfile. Falta subir la rama y abrir su PR a `develop` para comprobar los dos jobs en GitHub Actions. Este documento no acredita todavía ese resultado remoto ni un despliegue automático. La imagen local y las imágenes base descargadas permanecen en Docker; los recursos temporales de prueba se eliminaron.
