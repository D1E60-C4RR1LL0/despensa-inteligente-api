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

La primera ejecución local de los cuatro módulos de inventario encontró **2 fallos y 39 aprobaciones**: `PUT /stocks/{id}` aceptó con HTTP 200 un producto o ubicación inexistente. El comportamiento observado corresponde a SQLite de prueba. La corrección debe validar ambas referencias antes de modificar o confirmar la fila y devolver HTTP 404, conservando el stock original.

## Protecciones configuradas

La revisión previa confirmó `protected: false` para `main` y `develop`. Se preparó [branch-protection.json](branch-protection.json) y se aplicó mediante la API de GitHub usando GitHub CLI, pues el conector no expone escrituras de administración.

La respuesta de GitHub confirmó en ambas ramas: cuatro checks obligatorios, rama actualizada, reglas para administradores, cero aprobaciones externas obligatorias, force push y borrado deshabilitados. La política exige PR y conversaciones resueltas. La confirmación de lectura y la prueba con un CI fallido deben registrarse antes de declarar validado el bloqueo.

Las decisiones de incluir `develop`, conservar los cuatro nombres de jobs y no exigir una aprobación externa son adaptaciones al flujo del proyecto. La pauta no fija esos nombres ni cantidades.

## Evidencia y pendientes de este bloque

- Configuración de cobertura y subida de reportes preparada; pendiente su ejecución completa en CI.
- Regresión de referencias de stock reproducida localmente; pendiente la corrección y su validación.
- Protecciones aplicadas; pendiente demostrar el rechazo de un PR con checks fallidos y su habilitación al corregirlos.
- Recursos, escalabilidad y cierre en `main` permanecen fuera de este bloque.

No se declara un 100% global de la evaluación por aprobar esta etapa.
