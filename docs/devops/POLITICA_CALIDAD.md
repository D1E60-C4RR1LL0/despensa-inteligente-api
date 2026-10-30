# Política de calidad de la API — E2

Política acordada para este proyecto, basada en los contenidos de semanas 8–9 y la rúbrica IE2/IE3. El 80% se adopta como decisión del proyecto; la pauta no impone ese porcentaje. Esta documentación de asistencia se elaboró con Codex y debe ser validada por el equipo.

## Condiciones para integrar y desplegar

1. Todas las pruebas automatizadas deben aprobar.
2. La cobertura global de sentencias de los módulos de la API debe ser al menos 80%, según `.coveragerc`.
3. Snyk debe aprobar con la política `high` ya configurada.
4. La imagen debe construirse y aprobar la auditoría Compose.
5. El despliegue de revisión debe confirmar identidad de imagen, funcionamiento, límites efectivos de recursos sin OOM/reinicios observados, muestras válidas de API/MySQL y limpieza. La comparación de capacidad debe completar cuatro repeticiones comparables con respuestas correctas; no se exige una mejora de velocidad para aprobar. Ver [AUDITORIA_RECURSOS.md](AUDITORIA_RECURSOS.md) y [AUDITORIA_CAPACIDAD.md](AUDITORIA_CAPACIDAD.md).
6. `develop` y `main` requieren Pull Request, rama actualizada, conversaciones resueltas y los checks `pruebas`, `seguridad`, `imagen` y `despliegue` aprobados. Las protecciones también se aplican a administradores.

La política de ramas queda descrita en [branch-protection.json](branch-protection.json). Guardar ese JSON en Git no aplica las reglas: su estado efectivo debe verificarse en GitHub. Se exige pasar por PR, con cero aprobaciones externas obligatorias; esta decisión mantiene operable el flujo del repositorio sin presentar los checks ni una revisión propia como aprobación independiente de otro integrante. Los force push y el borrado de las dos ramas estables están deshabilitados.

## Alcance de la medición

Se mide `app`, `config`, `models`, `routes`, `schemas` y `utils`. La cobertura es global de sentencias, no cobertura de ramas, código nuevo, infraestructura ni un mínimo individual por módulo. Los scripts de despliegue, Alembic y las pruebas se validan mediante sus comprobaciones específicas; no se contabilizan dentro de ese porcentaje de API.

Un promedio suficiente no reemplaza los casos críticos. Se priorizan autenticación/roles/JWT, modificaciones de inventario, referencias válidas, rechazo de duplicados, actualizaciones parciales y conservación de proveedores/ubicaciones con registros asociados. No se eliminan archivos o casos del alcance para aumentar la métrica.

## Tipos de pruebas

| Tipo | Archivos o ejecución | Qué verifica |
|---|---|---|
| Unitarias o aisladas | `test_token_utils.py`, `test_compose_env.py`, `test_deployment_identity.py`, `test_resource_limits.py`, `test_capacity_comparison.py` | Reglas JWT sin red/BD; generación de configuración en archivos temporales; rechazo de imagen/revisión con Docker sustituido por un doble; límites/OOM/reinicios; comparación de cargas e integridad de respuestas. |
| Integración API/BD | Autenticación, categorías, productos, proveedores, ubicaciones, stock, movimientos y modelos | Comportamiento HTTP y persistencia/reglas de inventario usando SQLite de prueba. |
| Integración de configuración/migraciones | `test_jwt_configuration.py`, `test_migrations.py` | Procesos Python aislados, entorno, Alembic y esquema de prueba. |
| Integración en contenedores | `audit_compose.py` y `deploy_simulated.py` | API/MySQL, migraciones, persistencia, identidad, funcionamiento y limpieza en Docker. |

La suite completa contiene distintos tipos; no se presenta su total como cantidad de pruebas unitarias puras.

## Ejecución y evidencias

Desde la raíz en PowerShell, con el entorno de desarrollo instalado:

```powershell
$env:DATABASE_URL = 'sqlite:///:memory:'
.\venv\Scripts\python.exe -m pytest --cov --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:.quality-reports/coverage.xml --cov-report=html:.quality-reports/html --junitxml=.quality-reports/junit.xml
```

Para ejecutar solo el grupo aislado durante el desarrollo:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_token_utils.py tests/test_compose_env.py tests/test_deployment_identity.py tests/test_resource_limits.py tests/test_capacity_comparison.py
```

El primer comando coincide con el control de CI. Un fallo de prueba o del umbral devuelve un estado fallido e impide avanzar a imagen/despliegue. El artefacto `quality-<SHA>` conserva JUnit, XML y HTML durante 30 días, también ante fallos cuando se generan archivos. No se versionan el archivo de datos de cobertura ni las bases de prueba. Los resultados observados y las pruebas de bloqueo se registran en [AUDITORIA_CALIDAD_GOBERNANZA.md](AUDITORIA_CALIDAD_GOBERNANZA.md).
