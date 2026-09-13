# Despensa Inteligente API

Es una API REST para la gestión de productos, existencias y movimientos de inventario de una despensa doméstica.

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
- ️Gestión de categorías.
- Gestión de proveedores.
- Gestión de ubicaciones.
- Gestión de productos.
- Gestión de existencias.
- Gestión de movimientos de inventario.

### Funcionalidades agregadas en esta entrega

- ️Alertas de stock bajo.
- Lista de compras sugerida.
- Exclusión de productos inactivos de las alertas de stock.
- Pruebas automatizadas.
- ️Integración continua con GitHub Actions.
- Flujo de trabajo basado en ramas.
- Integración de cambios mediante Pull Requests.
- ️Versionamiento mediante GitHub Releases.

---

## ️ Tecnologías

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
│  └── workflows/
│    └── ci.yml
│
├── alembic/
│  ├── versions/
│  └── env.py
│
├── config/
│  └── database.py
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

En el proyecto se utiliza una estrategia de ramas para separar el desarrollo de nuevas funcionalidades, las correcciones y las versiones estables.

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
│    feature/*     │
│  Nueva funcionalidad  │
└────────────┬────────────┘
       │
       │ Pull Request
       ▼
┌─────────────────────────┐
│    develop     │
│ Rama de integración   │
└────────────┬────────────┘
       │
       │ Pull Request
       ▼
┌─────────────────────────┐
│     main      │
│  Versión estable   │
└────────────┬────────────┘
       │
       ▼
    GitHub Release
```

## Ramas principales

### `main`

Contiene las versiones estables del proyecto.

### `develop`

Es la rama que utilicé para integrar y validar cambios antes de incorporarlos a la versión estable.

### `feature/*`

Fue utilizada para desarrollar nuevas funcionalidades de forma aislada.

Ejemplos utilizados:

```text
feature/alertas-stock-bajo
feature/lista-compras
```

### `hotfix/*`

Fue utilizada para desarrollar correcciones específicas.

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


### Comparación de modelos

| Modelo | Característica principal | Ventaja | Contexto recomendado |
|---|---|---|---|
| Git Flow | Utiliza ramas `main`, `develop`, `feature` y `hotfix` | Separa claramente el desarrollo de las versiones estables | Proyectos con entregas planificadas y varias etapas de integración |
| GitHub Flow | Utiliza una rama principal y ramas temporales integradas mediante Pull Requests | Flujo simple y rápido | Equipos que realizan entregas frecuentes |
| Trunk-Based Development | Concentra la integración alrededor de una rama principal | Reduce la divergencia entre ramas | Equipos con integración continua y CI/CD maduro |

## Estrategia utilizada

Para esta entrega utilicé una estructura basada en **Git Flow**, con `main` como rama estable, `develop` como rama de integración y ramas `feature/*` y `hotfix/*` para cambios específicos.

---

# ️ Convenciones de ramas

| Tipo | Formato | Ejemplo |
|---|---|---|
| Rama estable | `main` | `main` |
| Integración | `develop` | `develop` |
| Nueva funcionalidad | `feature/<nombre>` | `feature/lista-compras` |
| Corrección | `hotfix/<nombre>` | `hotfix/corregir-alerta-stock` |

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


# Flujo colaborativo y trazabilidad

El desarrollo se realizó utilizando Git como sistema de control de versiones y GitHub como plataforma de colaboración.

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

### Comandos principales del flujo

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

Durante el desarrollo se utilizaron Pull Requests para integrar:

| Cambio | Rama de origen | Rama de destino |
|---|---|---|
| Alertas de stock bajo | `feature/alertas-stock-bajo` | `develop` |
| Lista de compras sugerida | `feature/lista-compras` | `develop` |
| Corrección de alertas | `hotfix/corregir-alerta-stock` | `develop` |
| Integración final | `develop` | `main` |

---

# ️ Integración continua

En el proyecto utilizó **GitHub Actions** para ejecutar automáticamente las pruebas.

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


## Rol de GitHub Actions dentro de CI/CD

GitHub Actions se utiliza en esta entrega como herramienta de Integración Continua (CI).

Cada cambio realizado sobre `develop` y cada Pull Request dirigido hacia `main` puede activar automáticamente el workflow. El pipeline permite:

- Obtener la versión actual del código.
- Configurar el entorno de Python.
- Instalar las dependencias.
- Configurar la variable de entorno necesaria para las pruebas.
- Ejecutar la suite de pruebas automatizadas.
- Informar el resultado del proceso.

De esta manera, la validación del código no depende únicamente de una revisión manual antes de la integración.

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

## ️ Alertas de stock bajo

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

# ️ Versionamiento y Releases

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
| API REST | ✔ |
| Autenticación | ✔ |
| Gestión de productos | ✔ |
| Gestión de stock | ✔ |
| Movimientos de inventario | ✔ |
| Alertas de stock bajo | ✔ |
| Lista de compras sugerida | ✔ |
| Pruebas automatizadas | ✔ |
| GitHub Actions | ✔ |
| Pull Requests | ✔ |
| Release `v1.0.0` | ✔ |

---
