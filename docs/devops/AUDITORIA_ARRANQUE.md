# Auditoría de migraciones y arranque

Fecha: 26 de octubre de 2026. Asistencia técnica realizada con Codex; el equipo debe revisar los resultados y elaborar sus propias justificaciones académicas.

## Corrección realizada

La nueva revisión `f3171e47e124`, posterior a `0c11a0e481fc`, crea las siete tablas de inventario faltantes, incluidos índices, claves foráneas y restricciones únicas. Conserva las dos revisiones anteriores. `alembic/env.py` carga explícitamente todos los modelos y `app.py` dejó de ejecutar `Base.metadata.create_all()`.

La secuencia para una base vacía es **configurar DATABASE_URL → ejecutar `alembic upgrade head` → iniciar la API**. Importar la aplicación no crea tablas ni valida la disponibilidad de la base: las migraciones y la comprobación funcional son etapas explícitas.

Se trabajó en la rama local `feature/e2-migraciones-arranque`, creada desde la versión estable de E1 abierta en `main`, conservando la documentación pendiente. No se realizaron commits, push, merges ni cambios en el MySQL existente del usuario.

## Repetir la auditoría

Desde la raíz, con las dependencias de `requirements.txt` instaladas:

```powershell
.\venv\Scripts\python.exe scripts/audit_bootstrap.py
```

El script crea una base SQLite temporal dentro de `.pytest_cache`, migra hasta `head`, compara el esquema con los modelos y comprueba que importar la API no agregue tablas. Repite `upgrade head` y utiliza `TestClient` para probar OpenAPI, registro, login, productos, stocks, alertas y lista de compras. No sustituye las dependencias de base de datos de la API.

También revierte únicamente la nueva migración sobre esa base desechable, comprueba que el usuario de prueba permanezca y vuelve a migrar hasta `head`. El script fija `DATABASE_URL` antes de importar el proyecto: no utiliza la conexión del `.env` ni modifica el entorno del terminal. La base temporal se elimina al terminar.

Con Docker Desktop disponible se puede repetir en MySQL:

```powershell
docker pull mysql:8.4
.\venv\Scripts\python.exe scripts/audit_bootstrap.py --mysql
```

Este modo crea su propio contenedor, utiliza credenciales aleatorias mediante variables de entorno, publica un puerto aleatorio solo en `127.0.0.1` y almacena los datos en `tmpfs`. El contenedor se elimina al terminar, incluso si falla la auditoría. No acepta una URL de base existente. La imagen queda en la caché de Docker.

MySQL 8.4 es una elección para esta validación, no un requisito académico ni la versión definitiva del futuro Compose. Se verificó la disponibilidad de la [imagen oficial](https://hub.docker.com/_/mysql). Se declaró `PyMySQL[rsa]==1.1.1` para instalar su dependencia de autenticación moderna, manteniendo la versión del driver. La dependencia ya estaba instalada en el entorno usado. El extra está documentado por [PyMySQL](https://pymysql.readthedocs.io/en/latest/user/installation.html).

El código de salida es 0 solo si el esquema coincide con los modelos, la importación no cambia las tablas, la API pasa las comprobaciones y la reversión seguida de reconstrucción conserva al usuario y restaura el esquema. Un fallo retorna código distinto de 0.

## Evidencia de la corrección

| Comprobación | SQLite temporal | MySQL temporal 8.4.13 |
|---|---|---|
| Migraciones desde una base vacía | Correctas | Correctas |
| Revisión alcanzada | `f3171e47e124` | `f3171e47e124` |
| Tablas de aplicación creadas | 9 | 9 |
| Tablas pendientes | 0 | 0 |
| Diferencias detectadas por Alembic | 0 | 0 |
| Tablas añadidas al importar la API | 0 | 0 |
| Repetición de `upgrade head` | Correcta | Correcta |
| OpenAPI, registro y login | Correctos | Correctos |
| Cuatro consultas de inventario | HTTP 200 y listas vacías | HTTP 200 y listas vacías |
| Reversión y reconstrucción | Correctas; usuario conservado | Correctas; usuario conservado |
| Código de salida | 0 | 0 |

Además de las nueve tablas de aplicación existe `alembic_version`, que controla la revisión. El digest observado al descargar `mysql:8.4` fue:

```text
sha256:76f0358884cb92d9a086d24e5671c38048d3fef40f2588703d73eb55392d6b69
```

La prueba usa `TestClient`; no inicia un servidor HTTP externo ni valida una imagen Docker de la API o un despliegue en GitHub Actions. El contenedor es exclusivamente infraestructura de prueba de MySQL y fue eliminado al terminar.

La suite completa finalizó con **53 passed, 4 warnings in 87.00s (0:01:27)** y código 0:

```powershell
$env:DATABASE_URL = 'sqlite:///:memory:'
.\venv\Scripts\python.exe -m pytest -q -o log_cli=false
```

Se conservan las 49 pruebas originales. Las cuatro nuevas pruebas de `tests/test_migrations.py` verifican reconstrucción y reversión sin perder un usuario, detención ante una tabla heredada antes de crear otras, importación sin crear tablas y adopción de un esquema heredado completo sin perder sus datos. Estas pruebas utilizan bases SQLite independientes.

Los cuatro avisos son los `SAWarning` de rollback de las fixtures existentes. Durante la auditoría con registro también apareció el aviso de passlib `(trapped) error reading bcrypt version`; no impidió registro ni login. Esta corrección no modifica las fixtures ni actualiza bcrypt/passlib. No se ha comprobado una ejecución remota de Actions para esta rama.

## Bases existentes con tablas creadas automáticamente

La nueva migración comprueba si ya existe alguna de las siete tablas de inventario y se detiene antes de crear cualquiera de ellas. Esto evita una aplicación parcial por colisión de nombres; es especialmente relevante para el DDL no transaccional de MySQL. No transforma automáticamente una base heredada.

Primero revisar el respaldo y la revisión actual. El siguiente comando compara el esquema configurado con los modelos sin ejecutar migraciones ni cambiar tablas o datos:

```powershell
alembic current
.\venv\Scripts\python.exe scripts/check_schema.py
```

`check_schema.py` utiliza `DATABASE_URL` del entorno o del `.env`. Retorna 0 cuando Alembic no detecta diferencias y 1 cuando las encuentra. Solo cubre las diferencias que Alembic puede detectar; también deben revisarse elementos específicos de la base no representados por los modelos. Consultar los límites de la [autogeneración de Alembic](https://alembic.sqlalchemy.org/en/latest/autogenerate.html).

Solo si se confirma que es una base heredada de E1, que su esquema y restricciones ya coinciden con esta revisión y que existe un respaldo verificado, puede registrarse la revisión sin recrear tablas:

```powershell
alembic stamp f3171e47e124
alembic upgrade head
```

`stamp` cambia únicamente la revisión registrada: no crea ni repara tablas. No utilizarlo para ocultar diferencias, saltar revisiones desconocidas o tratar una base parcial. Si hay diferencias, se necesita una reconciliación específica. El [cookbook de Alembic](https://alembic.sqlalchemy.org/en/latest/cookbook.html#building-an-up-to-date-database-from-scratch) describe el marcado de un esquema ya construido.

La adopción se probó con una base SQLite desechable. No se ejecutó `stamp`, `upgrade` ni `downgrade` sobre el MySQL existente del usuario. El `downgrade` de la nueva revisión elimina las siete tablas de inventario y sus datos; aquí se ejecutó solo sobre bases temporales.

## Hallazgo inicial conservado

Antes de la corrección, las migraciones terminaban en `0c11a0e481fc` y creaban solo `users` y `token_blacklist`. Quedaban siete tablas y 20 operaciones de esquema pendientes, incluidas tablas e índices. Al importar `app.py`, la API creaba las tablas faltantes y ocultaba la insuficiencia de las migraciones. La auditoría retornaba código 1.

Las tablas faltantes eran `categorias`, `proveedores`, `tipos_movimiento`, `ubicaciones`, `productos`, `movimientos_inventario` y `stocks`. La nueva revisión resuelve esa diferencia sin reescribir el historial anterior.
