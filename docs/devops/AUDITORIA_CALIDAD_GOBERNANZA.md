# Calidad y gobernanza — E2

Fecha: 29 de octubre de 2026. Rama: `feature/e2-calidad-gobernanza`, creada desde `develop` en `1a366540083224e4eddcca4d60fbef2b232da9a9`. Documento de asistencia técnica elaborado con Codex; el equipo debe validar fuentes y resultados y redactar sus propias justificaciones académicas.

## Fuentes y alcance

La pauta E2, p. 5, relaciona IE2 con casos críticos y políticas de calidad, e IE3 con seguridad y gobernanza. La semana 8, p. 19 y 26, enseña `pytest-cov` y un umbral configurable; p. 21–23 enseña Branch Protection y Required Checks. La semana 9, p. 20, muestra varios checks obligatorios. La actividad `2.3.1 Pruebas Unitarias Jacoco.pdf`, p. 5–10, explica la medición y los reportes en Java; el proyecto mantiene la alternativa Python enseñada en semana 8.

Se adopta el 80% global como política del proyecto, con base en el ejemplo de clase y la medición inicial de 81,86% sobre la API. No es un porcentaje exigido por la pauta ni un objetivo de cobertura individual de todos los módulos. [POLITICA_CALIDAD.md](POLITICA_CALIDAD.md) fija alcance, casos críticos, tipos de pruebas, ejecución y condiciones de integración.

Este bloque no modifica parámetros de CPU/memoria ni incorpora réplicas. Esos controles corresponden al siguiente bloque, sustentado en `2.2.1 Docker Compose.pdf`, p. 3 y 13, y semana 7, p. 23 y 35.

## Base y despliegue ya verificado

El [PR #13](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/13) quedó integrado en `develop` mediante `1a366540083224e4eddcca4d60fbef2b232da9a9`. Su [CI/CD por push](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40877704856) aprobó los cuatro jobs y 63 pruebas. Se descargó y validó el [reporte de staging](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40877704856/artifacts/12899850116): evento `push`, ref `refs/heads/develop`, ambiente `staging-simulado`, imagen coincidente, ocho comprobaciones verdaderas y limpieza correcta.

## Casos críticos incorporados

- Stock: creación/lectura/actualización parcial/borrado, filtros, cambio de ubicación válido, referencias inexistentes, duplicados y conservación del dato ante rechazos.
- Proveedores: ciclo de vida, datos omitidos en una actualización parcial, correo inválido y protección frente a borrado con productos asociados.
- Ubicaciones: ciclo de vida, duplicados, renombrado, protección con stock e historial de movimientos.
- Autorización: rechazo de lecturas y escrituras anónimas en los tres recursos.
- JWT aislado: sujeto válido, entrada sin mutación, caducidad, firma con otra clave y formato inválido.

La primera ejecución local de los cuatro módulos de inventario encontró **2 fallos y 39 aprobaciones**: `PUT /stocks/{id}` aceptó con HTTP 200 un producto o ubicación inexistente. El comportamiento observado corresponde a SQLite de prueba. La corrección valida las referencias proporcionadas antes de modificar o confirmar la fila y devuelve HTTP 404, conservando el stock original. También se verificó el rechazo de identificadores nulos explícitos; omitirlos sigue permitiendo actualizar únicamente la cantidad.

## Protecciones configuradas

La revisión previa confirmó `protected: false` para `main` y `develop`. Se preparó [branch-protection.json](branch-protection.json) y se aplicó mediante la API de GitHub usando GitHub CLI, pues el conector no expone escrituras de administración.

La respuesta de GitHub y una lectura posterior independiente confirmaron en ambas ramas: cuatro checks obligatorios, rama actualizada, reglas para administradores, cero aprobaciones externas obligatorias, force push y borrado deshabilitados. La política exige PR y conversaciones resueltas. Los registros de lectura quedaron en `.pytest_cache/branch-main-verified.json` y `.pytest_cache/branch-develop-verified.json`, sin secretos y fuera de Git.

Las decisiones de incluir `develop`, conservar los cuatro nombres de jobs y no exigir una aprobación externa son adaptaciones al flujo del proyecto. La pauta no fija esos nombres ni cantidades.

## Bloqueos y corrección verificados

El [PR #14](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/14) se abrió inicialmente en borrador para registrar una regresión real. Su [primer CI 40930444193](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40930444193), sobre `410df83f6b7eb51863b6dc4297b9fe082e97080b`, terminó con **2 failed, 105 passed**, cobertura **92,68%** y código de salida **1**. Falló `pruebas`, aprobó `seguridad` y se omitieron `imagen` y `despliegue`. Se publicó el [artefacto de calidad 12922875852](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40930444193/artifacts/12922875852), incluso con las pruebas fallidas. El porcentaje suficiente no compensó los errores de regresión.

Después se quitó el estado borrador sin cambiar ese commit. GitHub informó `isDraft: false` y `mergeStateStatus: BLOCKED`, con `pruebas: FAILURE`. Así se comprobó que el fallo de los checks bloqueaba la integración independientemente del borrador. Se consultó el estado de merge; no se presentó esta lectura como un intento real de fusionar el código fallido.

Se comprobó por separado el umbral con la misma configuración del 80% y alcance completo de API: se ejecutaron solo las cinco pruebas JWT válidas. Todas aprobaron, pero la cobertura fue **61,76%** y PyTest devolvió **1**. JUnit confirmó cero errores/fallos de pruebas y el XML confirmó cobertura inferior al umbral. Esta comprobación local usó archivos distintos en `.pytest_cache` y no cambió la política ni reemplazó los informes de la suite completa.

Tras corregir la API, la suite completa local terminó con **109 passed, 4 warnings in 51.13s** y cobertura **92,74%**, sobre 923 sentencias con 67 sin ejecutar. Proveedores, ubicaciones y stock alcanzaron 100% de sentencias en esta medición; esto no equivale a cubrir todas sus entradas o ramas posibles. Los cuatro avisos SQLAlchemy del rollback ya existían y se conservan como observación pendiente de las fixtures.

La clasificación documentada comprende 9 comprobaciones aisladas y 100 de integración/configuración, más las auditorías Docker de los jobs posteriores. La API mantiene el alcance original de medición; no se excluyeron módulos de baja cobertura para cumplir el umbral.

Los checks y ejecuciones del commit corregido, su integración y su ejecución por push se consultan desde el PR #14. La transición del CI fallido a la versión corregida debe verificarse antes de integrar el bloque. Recursos, escalabilidad y cierre en `main` permanecen fuera de este bloque.

No se declara un 100% global de la evaluación por aprobar esta etapa.
