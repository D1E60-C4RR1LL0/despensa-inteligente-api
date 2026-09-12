# Despensa Inteligente API

API REST para la gestión de productos, existencias y movimientos de inventario de una despensa doméstica.

El proyecto está desarrollado con **FastAPI** y **SQLAlchemy** e incorpora autenticación de usuarios, gestión de productos, control de stock, movimientos de inventario y funcionalidades de apoyo para productos con existencias bajas.

Además, esta entrega incorpora un flujo de trabajo basado en **Git**, integración continua mediante **GitHub Actions**, pruebas automatizadas y control de versiones mediante **GitHub Releases**.

---

## Contenido

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Flujo de trabajo Git](#-flujo-de-trabajo-git)
- [Modelos de branching](#-modelos-de-branching)
- [Convenciones de ramas](#-convenciones-de-ramas)
- [Convenciones de commits](#-convenciones-de-commits)
- [Pull Requests](#-pull-requests)
- [Integración continua](#-integración-continua)
- [Configuración segura de base de datos](#-configuración-segura-de-base-de-datos)
- [Pruebas automatizadas](#-pruebas-automatizadas)
- [Funcionalidades agregadas](#-funcionalidades-agregadas)
- [Versionamiento y Releases](#-versionamiento-y-releases)
- [Instalación](#-instalación)
- [Documentación de la API](#-documentación-de-la-api)

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
└── README.md
```

---

# Flujo de trabajo Git

El proyecto utiliza una estrategia de ramas para separar el desarrollo de nuevas funcionalidades, las correcciones y las versiones estables.

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

Ejemplos utilizados:

```text
feature/alertas-stock-bajo
feature/lista-compras
```

### `hotfix/*`

Se utilizan para desarrollar correcciones específicas.

Ejemplo utilizado:

```text
hotfix/corregir-alerta-stock
```

---

# Modelos de branching

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

GitHub Flow utiliza una estructura más sencilla, generalmente basada en una rama principal y ramas temporales.

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

## Estrategia utilizada

Esta entrega utiliza una estructura basada en **Git Flow**, con `main` como rama estable, `develop` como rama de integración y ramas `feature/*` y `hotfix/*` para cambios específicos.

---

# Convenciones de ramas

| Tipo | Formato | Ejemplo |
|---|---|---|
| Rama estable | `main` | `main` |
| Integración | `develop` | `develop` |
| Nueva funcionalidad | `feature/<nombre>` | `feature/lista-compras` |
| Corrección | `hotfix/<nombre>` | `hotfix/corregir-alerta-stock` |

### Recomendaciones

- Utilizar nombres breves y descriptivos.
- Utilizar minúsculas.
- Separar palabras mediante guiones.
- Evitar nombres genéricos.

---

# Convenciones de commits

| Tipo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un problema |
| `hotfix:` | Corrección urgente |
| `ci:` | Integración continua |
| `test:` | Pruebas |
| `docs:` | Documentación |
| `chore:` | Mantenimiento o configuración |

### Ejemplos reales

```text
feat: agregar alertas de stock bajo
feat: agregar lista de compras sugerida
hotfix: excluir productos inactivos de alertas
ci: configurar pipeline de pruebas
ci: configurar base de datos para pruebas
chore: configurar entorno seguro de base de datos
```

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

Durante el desarrollo se utilizaron Pull Requests para integrar:

| Cambio | Rama de origen | Rama de destino |
|---|---|---|
| Alertas de stock bajo | `feature/alertas-stock-bajo` | `develop` |
| Lista de compras sugerida | `feature/lista-compras` | `develop` |
| Corrección de alertas | `hotfix/corregir-alerta-stock` | `develop` |
| Integración final | `develop` | `main` |

---

# Integración continua

El proyecto utiliza **GitHub Actions** para ejecutar automáticamente las pruebas.

El workflow se encuentra en:

```text
.github/workflows/ci.yml
```

Se ejecuta ante:

```yaml
on:
  push:
    branches:
      - develop

  pull_request:
    branches:
      - main
```

### Flujo del pipeline

```text
Cambio en el repositorio
          │
          ▼
    GitHub Actions
          │
          ▼
  Descargar repositorio
          │
          ▼
   Configurar Python 3.12
          │
          ▼
 Instalar dependencias
          │
          ▼
Configurar entorno de pruebas
          │
          ▼
       Ejecutar pytest
          │
          ▼
   Resultado del pipeline
```

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

### Buenas prácticas

- No almacenar credenciales directamente en el código.
- No publicar archivos `.env`.
- Configurar las variables necesarias en cada entorno.
- Utilizar una base de datos independiente para las pruebas automatizadas cuando corresponda.

---

# Pruebas automatizadas

El proyecto utiliza **Pytest**.

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

> **49 pruebas automatizadas — 49 pruebas exitosas.**

Las mismas pruebas se ejecutan automáticamente mediante GitHub Actions.

---

# Funcionalidades agregadas

## Alertas de stock bajo

Endpoint para consultar productos cuyo stock actual se encuentra en o por debajo del stock mínimo configurado.

```http
GET /stocks/alertas
```

La funcionalidad considera solamente productos activos.

---

## Lista de compras sugerida

Permite consultar productos que requieren reposición considerando su stock actual y el stock mínimo configurado.

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
    │
    ▼
develop
    │
    ▼
Pull Request
    │
    ▼
main
    │
    ▼
v1.0.0
```

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
venv\Scriptsctivate
```

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar la base de datos

Configurar la variable de entorno:

```text
DATABASE_URL
```

## 5. Ejecutar las migraciones

```bash
alembic upgrade head
```

## 6. Iniciar la API

```bash
fastapi dev app.py
```

La API estará disponible en:

```text
http://localhost:8000
```

---

# Documentación de la API

Una vez iniciada la aplicación:

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

---

## Licencia

Este proyecto mantiene la licencia definida originalmente para la API.
