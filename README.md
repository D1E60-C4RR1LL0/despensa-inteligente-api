# Despensa Inteligente API

API REST para la gestión de productos, existencias y movimientos de inventario de una despensa doméstica.

El proyecto está desarrollado con **FastAPI** y **SQLAlchemy** e incorpora autenticación de usuarios, gestión de productos, control de stock, movimientos de inventario y funcionalidades de apoyo para productos con existencias bajas.

Además, esta entrega incorpora un flujo de trabajo basado en **Git**, integración continua mediante **GitHub Actions**, pruebas automatizadas y control de versiones mediante **GitHub Releases**.

---

## Contenido

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Flujo de trabajo Git](#flujo-de-trabajo-git)
- [Modelos de branching](#modelos-de-branching)
- [Convenciones de ramas](#convenciones-de-ramas)
- [Convenciones de commits](#convenciones-de-commits)
- [Flujo colaborativo y trazabilidad](#flujo-colaborativo-y-trazabilidad)
- [Pull Requests](#pull-requests)
- [Estrategia de revisión](#estrategia-de-revisión)
- [Flujo de merge](#flujo-de-merge)
- [Flujo DevOps](#flujo-devops)
- [Integración continua](#integración-continua)
- [Configuración segura de base de datos](#configuración-segura-de-base-de-datos)
- [Pruebas automatizadas](#pruebas-automatizadas)
- [Funcionalidades agregadas](#funcionalidades-agregadas)
- [Versionamiento y Releases](#versionamiento-y-releases)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Ejecución con Docker](#ejecución-con-docker)
- [Orquestación con Docker Compose](#orquestación-con-docker-compose)
- [Seguridad del pipeline](#seguridad-del-pipeline)
- [Documentación de la API](#documentación-de-la-api)
- [Estado del proyecto](#estado-del-proyecto)
- [Planificación de la Evaluación 2](#planificación-de-la-evaluación-2)

---

## Características

### Gestión de la aplicación

- Autenticación de usuarios mediante JWT.
- Control de acceso mediante roles.
- Gestión de categorías.
- Gestión de proveedores.
- Gestión de ubicaciones.
- Gestión de productos.
- Gestión de existencias.
- Gestión de movimientos de inventario.

### Funcionalidades agregadas en esta entrega

- Alertas de stock bajo.
- Lista de compras sugerida.
- Exclusión de productos inactivos de las alertas de stock.
- Pruebas automatizadas.
- Integración continua con GitHub Actions.
- Flujo de trabajo basado en ramas.
- Integración de cambios mediante Pull Requests.
- Versionamiento mediante GitHub Releases.

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| **Python** | Lenguaje principal |
| **FastAPI** | Framework para la API REST |
| **SQLAlchemy** | ORM para interacción con la base de datos |
| **Pydantic** | Validación y serialización de datos |
| **MySQL** | Base de datos de la aplicación |
| **Alembic** | Migraciones de base de datos |
| **Pytest** | Pruebas automatizadas |
| **Git** | Control de versiones |
| **GitHub** | Repositorio y colaboración |
| **GitHub Actions** | Integración continua |
| **Docker** | Imagen de la API y ejecución en contenedores |

---

## Estructura del proyecto

```text
despensa-inteligente-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── config/
│   └── database.py
│
├── models/
├── routes/
├── schemas/
├── tests/
├── utils/
│
├── app.py
├── alembic.ini
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
└── README.md
```

---

# Flujo de trabajo Git

El repositorio cuenta con las ramas principales `main` y `develop`, además de ramas de trabajo `feature/*` y `hotfix/*`.

La estructura utilizada es:

```text
main
  │
  └── develop
        │
        ├── feature/*
        │
        └── hotfix/*
```

### Flujo general

```text
┌─────────────────────────┐
│       feature/*         │
│   Nueva funcionalidad   │
└────────────┬────────────┘
             │
             │ Pull Request
             ▼
┌─────────────────────────┐
│        develop          │
│ Rama de integración     │
└────────────┬────────────┘
             │
             │ Pull Request
             ▼
┌─────────────────────────┐
│          main           │
│    Versión estable      │
└────────────┬────────────┘
             │
             ▼
        GitHub Release
```

## Ramas principales

### `main`

Contiene las versiones estables del proyecto.

### `develop`

Es la rama utilizada para integrar y validar cambios antes de incorporarlos a la versión estable.

### `feature/*`

Se utilizan para desarrollar nuevas funcionalidades de forma aislada.

Ejemplos utilizados durante el proyecto:

```text
feature/alertas-stock-bajo
feature/lista-compras
```

### `hotfix/*`

Se utilizan para desarrollar correcciones específicas sobre funcionalidades existentes.

Ejemplo utilizado durante el proyecto:

```text
hotfix/corregir-alerta-stock
```

---

# Modelos de branching

Existen diferentes estrategias para organizar el desarrollo mediante ramas.

## Git Flow

Git Flow utiliza ramas principales como `main` y `develop`, complementadas por ramas destinadas a funcionalidades, correcciones y versiones.

```text
main
 │
 └── develop
      ├── feature/*
      ├── release/*
      └── hotfix/*
```

Permite separar el desarrollo de nuevas funcionalidades de las versiones estables.

## GitHub Flow

GitHub Flow utiliza una estructura más sencilla, generalmente basada en una rama principal y ramas temporales integradas mediante Pull Requests.

```text
main
 │
 ├── feature
 │
 └── Pull Request
          │
          ▼
        merge
```

Es adecuado para equipos que buscan un flujo sencillo y entregas frecuentes.

## Trunk-Based Development

Trunk-Based Development concentra el desarrollo alrededor de una rama principal o *trunk*.

```text
main
 ├── cambio pequeño
 ├── cambio pequeño
 ├── cambio pequeño
 └── cambio pequeño
```

Busca reducir la duración de las ramas y favorecer la integración frecuente.

### Comparación de modelos

| Modelo | Característica principal | Ventaja | Contexto recomendado |
|---|---|---|---|
| Git Flow | Utiliza `main`, `develop`, `feature` y `hotfix` | Separa el desarrollo de las versiones estables | Proyectos con entregas planificadas |
| GitHub Flow | Utiliza una rama principal y ramas temporales | Flujo simple y rápido | Equipos con entregas frecuentes |
| Trunk-Based Development | Concentra la integración alrededor de una rama principal | Reduce la divergencia entre ramas | Equipos con integración continua y CI/CD maduro |

## Estrategia utilizada

Para esta entrega elegí **Git Flow** porque, al realizar el desarrollo de manera individual, me permite mantener separados los distintos cambios y trabajar cada funcionalidad de forma independiente. Además, como esta actividad exige demostrar un flujo de desarrollo mediante ramas, Pull Requests y merges, esta estrategia facilita representar y mantener ordenado el proceso. Finalmente, la separación entre `feature/*`, `develop` y `main` me permite mantener una trazabilidad clara de los cambios realizados y revisar posteriormente qué modificaciones corresponden a cada funcionalidad.

---

# Convenciones de ramas

| Tipo | Formato | Ejemplo |
|---|---|---|
| Rama estable | `main` | `main` |
| Integración | `develop` | `develop` |
| Nueva funcionalidad | `feature/<nombre>` | `feature/lista-compras` |
| Corrección | `hotfix/<nombre>` | `hotfix/corregir-alerta-stock` |

### Convenciones utilizadas

- Utilizar nombres breves y descriptivos.
- Utilizar minúsculas.
- Separar palabras mediante guiones.
- Utilizar el prefijo correspondiente al tipo de trabajo.
- Evitar nombres genéricos como `cambios`, `prueba` o `nueva-rama`.

---

# Convenciones de commits

Los commits utilizan una estructura basada en tipos para identificar el propósito del cambio.

| Tipo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un problema |
| `hotfix:` | Corrección urgente |
| `ci:` | Cambios relacionados con integración continua |
| `test:` | Incorporación o modificación de pruebas |
| `docs:` | Cambios de documentación |
| `chore:` | Mantenimiento o configuración |

### Ejemplos utilizados durante el proyecto

```text
feat: agregar alertas de stock bajo
feat: agregar lista de compras sugerida
hotfix: excluir productos inactivos de alertas
ci: configurar pipeline de pruebas
ci: configurar base de datos para pruebas
chore: configurar entorno seguro de base de datos
```

---

# Flujo colaborativo y trazabilidad

El desarrollo se realizó utilizando Git como sistema de control de versiones y GitHub como plataforma de colaboración.

Aunque el desarrollo fue realizado individualmente, se utilizó el flujo de trabajo colaborativo solicitado para separar funcionalidades, correcciones, revisiones e integración.

El flujo utilizado fue:

1. Actualizar la rama `develop`.
2. Crear una rama de funcionalidad o corrección.
3. Realizar los cambios localmente.
4. Ejecutar las pruebas.
5. Registrar los cambios mediante `commit`.
6. Enviar la rama al repositorio remoto mediante `push`.
7. Crear un Pull Request hacia `develop`.
8. Revisar y validar los cambios.
9. Realizar el `merge`.
10. Actualizar nuevamente la rama local mediante `pull`.
11. Integrar `develop` en `main` mediante Pull Request.
12. Crear la versión estable mediante GitHub Release.

### Comandos principales

```bash
git clone <repositorio>

git checkout develop
git pull origin develop

git checkout -b feature/<nombre>

git add .
git commit -m "feat: descripción del cambio"
git push -u origin feature/<nombre>

git checkout develop
git pull origin develop

git merge <rama>
git push origin develop
```

La trazabilidad del código se mantiene mediante el historial de commits, las ramas, los Pull Requests, los merges y las releases registrados en GitHub.

---

# Pull Requests

Los cambios desarrollados en ramas independientes se incorporan mediante **Pull Requests**.

```text
feature/*
     │
     ▼
Pull Request
     │
     ▼
 develop
     │
     ▼
Pull Request
     │
     ▼
  main
```

Durante el desarrollo se integraron los siguientes cambios:

| Cambio | Rama de origen | Rama de destino |
|---|---|---|
| Alertas de stock bajo | `feature/alertas-stock-bajo` | `develop` |
| Lista de compras sugerida | `feature/lista-compras` | `develop` |
| Corrección de alertas | `hotfix/corregir-alerta-stock` | `develop` |
| Integración final | `develop` | `main` |

---

# Estrategia de revisión

Los cambios se integran mediante Pull Requests para mantener una revisión previa antes de incorporarlos a las ramas de integración o estable.

La revisión considera:

- Verificar que el cambio corresponda al objetivo de la rama.
- Revisar los archivos modificados antes del merge.
- Ejecutar las pruebas automatizadas.
- Verificar que GitHub Actions finalice correctamente.
- Revisar que no existan conflictos con la rama destino.
- Integrar el Pull Request después de que las validaciones sean satisfactorias.

En los Pull Requests hacia `main`, el resultado de GitHub Actions se utiliza como validación automática antes de realizar el merge.

---

# Flujo de merge

Los cambios de las ramas `feature/*` y `hotfix/*` se integran mediante Pull Requests hacia `develop`.

Una vez que los cambios se encuentran validados, `develop` se integra mediante un Pull Request hacia `main`.

```text
feature/*
    │
    │ Pull Request
    ▼
develop
    │
    │ Pull Request
    ▼
main
```

El merge se realiza después de revisar los cambios y verificar el resultado de las pruebas automatizadas.

---

# Flujo DevOps

El proyecto implementa un flujo DevOps que integra control de versiones, colaboración, integración continua, pruebas automatizadas e incorporación de versiones estables.

```text
Desarrollo local
      |
      v
     Git
      |
      v
    GitHub
      |
      v
 Pull Request
      |
      v
GitHub Actions
      |
      v
Instalación de dependencias
      |
      v
Ejecución de pytest
      |
      v
Validación automática
      |
      v
    Merge
      |
      v
  develop
      |
      v
 Pull Request
      |
      v
    main
      |
      v
 GitHub Release
```

Este flujo permite detectar errores mediante validaciones automáticas antes de integrar cambios en las ramas principales y mantener una versión estable del proyecto.

---

# Integración continua

El proyecto utiliza **GitHub Actions** para ejecutar pruebas y análisis de seguridad antes de construir la imagen Docker.

El workflow se encuentra en:

```text
.github/workflows/ci.yml
```

## Eventos que ejecutan el pipeline

El workflow se ejecuta ante:

```yaml
on:
  push:
    branches:
      - develop

  pull_request:
    branches:
      - develop
      - main
```

## Flujo del pipeline

```text
Cambio en el repositorio
          |
          v
    GitHub Actions
          |
          v
  Descargar repositorio
          |
          v
   Configurar Python 3.12
          |
          v
 Instalar dependencias
          |
          v
Configurar entorno de pruebas
          |
          v
       Ejecutar pytest
          |
          v
    Verificar seguridad
          |
          v
    Construir imagen Docker
          |
          v
    Verificar Compose
          |
          v
   Resultado del pipeline
```

## Rol de GitHub Actions dentro de CI/CD

GitHub Actions se utiliza en esta entrega como herramienta de **Integración Continua (CI)**.

Cada push sobre `develop` y cada Pull Request dirigido hacia `develop` o `main` activa el workflow.

El pipeline permite:

- Obtener la versión actual del código.
- Configurar el entorno de Python.
- Instalar las dependencias.
- Configurar la variable de entorno necesaria para las pruebas.
- Ejecutar la suite de pruebas automatizadas.
- Construir la imagen con la etiqueta `inventory-api:<SHA de la ejecución>`, mediante un job que depende de las pruebas y los análisis de seguridad.
- Verificar con Compose el arranque, la persistencia y el bloqueo ante una migración fallida, usando recursos temporales.
- Informar el resultado del proceso.

De esta manera, la validación del código no depende únicamente de una revisión manual antes de la integración.

El job `pruebas` instala `requirements-dev.txt`; `seguridad` ejecuta Snyk Code y el análisis de dependencias. El job `imagen` espera que ambos aprueben, construye el Dockerfile y ejecuta `scripts/audit_compose.py --image inventory-api:${{ github.sha }}` con permisos `contents: read`. La auditoría utiliza esa imagen sin reconstruirla y comprueba su identificador en los contenedores de API y migraciones. Docker y Compose ya pasaron en GitHub Actions en los bloques anteriores. El primer CI con Snyk detectó una incidencia crítica de certifi y bloqueó la imagen; se corrigió la versión y falta confirmar el nuevo CI. La imagen no se publica todavía en un registry y el stack de auditoría se elimina al terminar: es una prueba de integración, no un entorno desplegado permanente.

### CI y CD en este proyecto

La implementación realizada se concentra principalmente en **Integración Continua (CI)**.

La automatización valida los cambios mediante pruebas antes de su integración en las ramas principales.

La publicación de la versión estable se realiza mediante GitHub Releases. En esta entrega no se implementa un despliegue automático hacia un entorno productivo, por lo que no se presenta como una implementación completa de Continuous Deployment (CD).

---

# Configuración segura de base de datos

La conexión a la base de datos utiliza la variable de entorno:

```text
DATABASE_URL
```

La aplicación y Alembic obtienen la información de conexión desde esta variable.

Ejemplo para un entorno local:

```text
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/despensa
```

La firma JWT utiliza además `JWT_SECRET_KEY`, obligatoria para ejecutar la API. Puede definirse en el entorno o en el `.env` local. `.env.example` documenta las variables sin incluir una clave real. Para generar una clave nueva para la sesión en PowerShell:

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Para conservar la misma clave entre sesiones, guardarla en el `.env` local sin versionarla. Cambiar la clave invalida los tokens anteriores. Las pruebas y auditorías generan su propia clave efímera.

### Buenas prácticas

- No almacenar credenciales directamente en el código.
- No publicar archivos `.env`.
- Configurar las variables necesarias en cada entorno.
- Utilizar una base de datos independiente para las pruebas automatizadas cuando corresponda.

---

# Pruebas automatizadas

El proyecto utiliza **Pytest** para realizar pruebas automatizadas.

Para ejecutar las pruebas localmente:

```bash
pytest
```

Las pruebas cubren:

- Autenticación.
- Usuarios.
- Categorías.
- Productos.
- Proveedores.
- Ubicaciones.
- Stock.
- Movimientos de inventario.
- Restricciones de modelos.
- Autorización de endpoints.
- Alertas de stock bajo.
- Lista de compras sugerida.

### Estado actual

La E1 cerró con **49 pruebas automatizadas exitosas**. Tras las pruebas de migraciones, configuración y autorización del registro público, la suite local tiene **61 pruebas aprobadas**. Las evidencias están en las auditorías de [arranque](docs/devops/AUDITORIA_ARRANQUE.md), [Docker](docs/devops/AUDITORIA_DOCKER.md), [Compose](docs/devops/AUDITORIA_COMPOSE.md) y [seguridad](docs/devops/AUDITORIA_SEGURIDAD.md).

Las mismas pruebas se ejecutan automáticamente mediante GitHub Actions.

---

# Funcionalidades agregadas

## Alertas de stock bajo

Se agregó un endpoint para consultar productos cuyo stock actual se encuentra en o por debajo del stock mínimo configurado.

```http
GET /stocks/alertas
```

La funcionalidad considera solamente productos activos.

---

## Lista de compras sugerida

Se agregó una funcionalidad para consultar productos que requieren reposición considerando su stock actual y el stock mínimo configurado.

```http
GET /productos/lista-compras
```

La respuesta permite obtener una lista orientativa de productos que deberían ser considerados para una próxima compra.

---

# Versionamiento y Releases

Las versiones estables del proyecto se publican mediante **GitHub Releases**.

La primera versión estable de esta entrega corresponde a:

```text
v1.0.0
```

### Flujo de versionamiento

```text
feature/*
    |
    v
develop
    |
    v
Pull Request
    |
    v
main
    |
    v
v1.0.0
```

---

# Requisitos previos

Antes de ejecutar el proyecto se requiere:

- Python 3.12 o una versión compatible.
- pip.
- Git.
- Un motor de base de datos configurado.
- Una variable de entorno `DATABASE_URL`.

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api.git
cd despensa-inteligente-api
```

## 2. Crear el entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements-dev.txt
```

`requirements-dev.txt` incluye las dependencias de ejecución y las de pruebas. Para un entorno que solo ejecuta la API, instalar `requirements.txt`.

## 4. Configurar la base de datos

Configurar las variables de entorno:

```text
DATABASE_URL
JWT_SECRET_KEY
```

Usar `.env.example` como referencia para completar el `.env` local, conservando la configuración existente. `JWT_SECRET_KEY` debe tener una clave propia; el ejemplo la deja vacía para exigir su configuración.

## 5. Ejecutar las migraciones

Para una base vacía, aplicar las migraciones antes de iniciar la API:

```bash
alembic upgrade head
```

La aplicación ya no crea tablas automáticamente al arrancar. Si la base contiene tablas creadas por una versión anterior, seguir primero el [procedimiento para bases existentes](docs/devops/AUDITORIA_ARRANQUE.md#bases-existentes-con-tablas-creadas-automáticamente); la nueva migración detecta ese caso y se detiene antes de crear tablas de inventario.

## 6. Iniciar la API

```bash
fastapi dev app.py
```

La API estará disponible en:

```text
http://localhost:8000
```

---

# Ejecución con Docker

Construir la imagen desde la raíz:

```powershell
docker build --tag inventory-api:e2-docker .
```

La imagen usa Python 3.12, ejecuta Uvicorn en `0.0.0.0:8000` como usuario `app` y recibe `DATABASE_URL` y `JWT_SECRET_KEY` en tiempo de ejecución. Incluye Alembic, pero las migraciones se ejecutan explícitamente antes de arrancar el servidor. `.dockerignore` limita el contexto a los archivos necesarios y excluye `.env`, Git, entornos virtuales, pruebas y bases locales.

Para una comprobación completa y desechable con MySQL, incluido el arranque real del servidor y peticiones HTTP:

```powershell
docker pull mysql:8.4
python scripts/audit_docker.py
```

El script crea un MySQL temporal, aplica las migraciones desde la imagen y arranca la API con un puerto aleatorio local. Comprueba registro, login, consultas de inventario, healthcheck y exclusiones de archivos. Elimina sus contenedores y su red al terminar. No utiliza el MySQL ni el `.env` del usuario.

Para levantar una demostración manual con SQLite en un volumen Docker independiente:

```powershell
$env:DATABASE_URL = "sqlite:////data/demo.db"
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(32))"
docker volume create inventory-e2-demo
docker run --rm --env DATABASE_URL --env JWT_SECRET_KEY --mount type=volume,source=inventory-e2-demo,target=/data inventory-api:e2-docker python -m alembic upgrade head
docker run --rm --publish 127.0.0.1:8000:8000 --env DATABASE_URL --env JWT_SECRET_KEY --mount type=volume,source=inventory-e2-demo,target=/data inventory-api:e2-docker
```

La demostración queda disponible en `http://localhost:8000/docs`. `Ctrl+C` detiene el servidor; el volumen conserva sus datos. Las variables anteriores afectan esa sesión de PowerShell y seleccionan SQLite para la demostración. El healthcheck consulta `/openapi.json`: acredita respuesta HTTP, mientras que la auditoría comprueba también operaciones con base de datos.

Para conectar la imagen a MySQL, proporcionar una URL válida desde el contenedor: `localhost` dentro del contenedor identifica al propio contenedor. En Docker Desktop, una base del host puede requerir `host.docker.internal`; entre contenedores se usa su nombre de servicio o alias de red. El stack Compose de la siguiente sección utiliza `db`. Ver los resultados de la imagen en [AUDITORIA_DOCKER.md](docs/devops/AUDITORIA_DOCKER.md).

---

# Orquestación con Docker Compose

El archivo `docker-compose.yml` define MySQL (`db`), una tarea breve de migración (`migrate`) y la API (`api`). La secuencia es: MySQL saludable → migraciones completadas → API. La tarea de migración reutiliza la imagen de la API y termina con código 0; ese estado es el esperado.

Preparar una configuración local independiente del MySQL y del `.env` existentes:

```powershell
python scripts/init_compose_env.py
docker compose --env-file .env.compose config --quiet
docker compose --env-file .env.compose up --build --detach --wait --wait-timeout 180
docker compose --env-file .env.compose ps --all
```

El helper genera `.env.compose` con credenciales propias y una clave JWT sin mostrarlas. Si el archivo ya existe, lo conserva. `.env.compose.example` documenta las variables; `.gitignore` excluye la configuración real. `config --quiet` valida sin mostrar los secretos interpolados.

La API queda disponible en `http://localhost:8000/docs`. El puerto puede cambiarse mediante `API_PORT` en `.env.compose`. MySQL no publica un puerto en el host: la API lo alcanza como `db` por la red `backend`. Los datos se guardan en el volumen `mysql_data`, cuyo nombre real incluye el proyecto Compose.

Ver logs o detener los servicios conservando los datos:

```powershell
docker compose --env-file .env.compose logs --tail 100 api migrate
docker compose --env-file .env.compose down
```

Repetir `up` con las mismas variables permite recuperar los datos del volumen. Añadir `--volumes` a `down` elimina esos datos: no es el comando habitual para detener este stack. Las variables `MYSQL_*` inicializan usuarios y base cuando el volumen está vacío; cambiarlas después no actualiza automáticamente las cuentas ya almacenadas. Conservar `.env.compose` junto con la persistencia y planificar cualquier cambio de credenciales.

`COMPOSE_DATABASE_URL` es la URL interna de este stack y se pasa a la API como `DATABASE_URL`. Su nombre separado evita reutilizar por accidente una `DATABASE_URL` de la sesión local. Si se editan usuario, contraseña o base en el archivo, la URL debe mantenerse coherente. Como en las clases, las variables del entorno de la consola pueden prevalecer sobre el archivo.

`API_IMAGE` permite seleccionar la imagen compartida por API y migraciones; el valor predeterminado es `inventory-api:local`. CI utiliza la etiqueta con SHA del build y la auditoría comprueba que se pruebe exactamente ese artefacto.

Para comprobar arranque, persistencia, esquema y fallo de migración en un proyecto completamente desechable:

```powershell
python scripts/audit_compose.py
```

El script usa un proyecto, credenciales, puerto y volumen propios. Elimina exclusivamente ese proyecto de auditoría y sus datos al terminar. No utiliza `.env.compose`, el `.env` ni el MySQL existente del usuario. La correspondencia con semanas 6–7, las adaptaciones del proyecto y las evidencias están en [AUDITORIA_COMPOSE.md](docs/devops/AUDITORIA_COMPOSE.md).

---

# Seguridad del pipeline

Dependabot tiene alertas y actualizaciones de seguridad activadas en GitHub. `.github/dependabot.yml` configura revisiones semanales de pip y las acciones, con PR de versiones hacia `develop`. El archivo debe llegar a la rama predeterminada `main` para que GitHub active esa planificación; las alertas y actualizaciones de seguridad siguen la rama predeterminada.

El job `seguridad` ejecuta `snyk code test` y `snyk test` con umbral `high`. `imagen` depende de `pruebas` y `seguridad`: un análisis fallido o no ejecutable bloquea la construcción y la auditoría Compose. La configuración requiere `SNYK_TOKEN` en los secretos de **Actions y Dependabot**, y `SNYK_ORG` como variable no secreta del repositorio. No guardar el token en archivos ni compartirlo en el chat.

Se solicita salida JSON de Snyk y se conserva como artefacto. El [primer CI de seguridad](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628001505) verificó la autenticación, aprobó Snyk Code con el umbral elegido y bloqueó la imagen por un hallazgo crítico de certifi. Se actualizó a la versión corregida; la [auditoría de seguridad](docs/devops/AUDITORIA_SEGURIDAD.md) registra esa evidencia, la línea base de 50 alertas, la política y el estado de la repetición. Un análisis con umbral `high` no informa sobre todas las severidades.

El registro público acepta únicamente el rol `user`, que también es el valor predeterminado. Intentar crear un administrador mediante `/signup` devuelve HTTP 422. Las cuentas administrativas existentes conservan sus permisos.

---

# Documentación de la API

Una vez iniciada la aplicación, se puede acceder a la documentación interactiva.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

# Estado del proyecto

| Componente | Estado |
|---|---|
| API REST | ✅ |
| Autenticación | ✅ |
| Gestión de productos | ✅ |
| Gestión de stock | ✅ |
| Movimientos de inventario | ✅ |
| Alertas de stock bajo | ✅ |
| Lista de compras sugerida | ✅ |
| Pruebas automatizadas | ✅ |
| GitHub Actions | ✅ |
| Pull Requests | ✅ |
| Release `v1.0.0` | ✅ |
| Imagen Docker de la API | ✅ Validada localmente con MySQL temporal |
| Construcción Docker en CI | ✅ Validada en el PR #6 y su merge en develop |
| Orquestación con Compose | ✅ Validada localmente y en CI del PR #7 y su merge |

---

## Planificación de la Evaluación 2

La referencia de trabajo para la segunda entrega de Ingeniería DevOps está en la [guía maestra E2](docs/devops/GUIA_MAESTRA_E2_DOY0101.md). La [revisión inicial](docs/devops/REVISION_E2.md) contrasta esa guía con la pauta oficial y el repositorio, registra las pruebas ejecutadas y separa requisitos, recomendaciones y puntos por verificar.

Las auditorías de [arranque](docs/devops/AUDITORIA_ARRANQUE.md), [Docker](docs/devops/AUDITORIA_DOCKER.md), [Compose](docs/devops/AUDITORIA_COMPOSE.md) y [seguridad](docs/devops/AUDITORIA_SEGURIDAD.md) registran la evolución y la evidencia de cada bloque. Siguen pendientes la validación remota del nuevo bloque de seguridad y el despliegue automático con su trazabilidad.

## Licencia

Este proyecto mantiene la licencia definida originalmente para la API.
