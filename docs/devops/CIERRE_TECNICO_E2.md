# Estado técnico para entrega — E2 DOY0101

Revisión: **1 de noviembre de 2026**. Documento de asistencia elaborado con Codex; el equipo debe validarlo. No sustituye su informe, justificaciones académicas, conclusiones ni reflexiones individuales.

La pauta oficial permite Compose y Snyk y exige README con pipeline, trazabilidad y calidad. Este cierre aplica a IE1–IE5 del PDF/DOCX ya contrastados en [REVISION_E2.md](REVISION_E2.md). Las decisiones concretas de Python, cobertura mínima del 80%, presupuestos y carga son adaptaciones del proyecto apoyadas en las clases citadas en la [matriz](MATRIZ_EVIDENCIAS_E2.md).

## Evidencia técnica verificada

El [PR #17](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/pull/17) integró la implementación en `main`, commit `ac9319e41eeed036f68a6a245fce9095c4a4bb47`. El [CI/CD 41137641760](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/41137641760) del push de ese commit aprobó los cuatro jobs. Esta revisión documental no cambia aplicación, pruebas, dependencias ni pipeline; consultar [Actions](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions) para el head de entrega posterior a la documentación.

| Indicador | Resultado comprobado |
|---|---|
| IE1 | Imagen Python slim, usuario no root, contexto restringido y build/auditoría de imagen aprobados. |
| IE2 | **134 pruebas aprobadas**, cero errores/fallos/omitidas; **92,74%** global de sentencias de API (856/923), mínimo del proyecto 80%. Se distinguen 34 comprobaciones aisladas y 100 de integración/configuración. |
| IE3 | Snyk Code y dependencias aprobados con umbral `high`; 52 dependencias, cero incidencias sobre ese umbral. Protecciones de `main`: PR, rama actualizada, cuatro checks y reglas para administradores. Dependabot en main; **0 alertas abiertas, 50 corregidas y 0 descartadas**, consultado el 01-11-2026. |
| IE4 | `push` de main desplegado automáticamente en `produccion-simulada`; mismo ID/revisión de imagen, nueve comprobaciones verdaderas, 40/40 consultas básicas y limpieza correcta. |
| IE5 | API/MySQL/migraciones con red, volumen y salud; persistencia y bloqueo ante migración fallida verificados. Comparación de capacidad con cuatro repeticiones y **9.600 lecturas correctas**, cuotas efectivas y limpieza. |

La comparación de producción observó medianas de **70,510 solicitudes/s** con API 0,5 CPU/192 MiB y **146,054** con 1 CPU/384 MiB; p95 por repetición **187,053/84,082 ms**. Relación observada 2,071 para esa carga en ese runner. La [auditoría de capacidad](AUDITORIA_CAPACIDAD.md) conserva método, resultados locales y límites: capacidad vertical en un host, sin acreditar autoscaling, SLA ni capacidad máxima. Aprobar los controles no garantiza una calificación de 100%.

## Dependabot: cierre de la discrepancia anterior

El 30 de octubre la API mantenía 50 alertas abiertas aunque el SBOM actualizado y la comparación de rangos no encontraban coincidencias vulnerables. Se conservó esa discrepancia sin descartar alertas. La lectura del 1 de noviembre confirmó **cero abiertas, 50 con estado `fixed` y cero `dismissed`**. El YAML pip/Actions semanal está en la rama predeterminada; los trabajos de actualización del grafo y seguridad constan en el PR #17. Configurar una programación no implica que cada ejecución genere un PR si las versiones ya están actualizadas.

## Informes y conservación

El [resumen versionado](evidencias/cierre-main-ac9319e.json) conserva commit, ejecución, resultados, identidad de imagen, artefactos y digests. Los cuatro ZIP locales se verificaron nuevamente por SHA-256 el 01-11-2026 contra los digests de GitHub.

| Informe | Artefacto | Vencimiento indicado por GitHub |
|---|---|---|
| Calidad: JUnit, XML/HTML | [13016379086](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/41137641760/artifacts/13016379086) | 29-11-2026 |
| Snyk Code y dependencias JSON | [13016114463](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/41137641760/artifacts/13016114463) | 13-11-2026 |
| Producción simulada | [13016359281](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/41137641760/artifacts/13016359281) | 29-11-2026 |
| Capacidad y cuatro repeticiones | [13017089424](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/41137641760/artifacts/13017089424) | 29-11-2026 |

Se conservaron copias completas en `deployment/e2-main-ac9319e/`, carpeta local ignorada por Git. Los resúmenes versionados no extienden la retención ni sustituyen los ZIP. La imagen de transferencia se retiene un día porque sirve a los jobs del mismo workflow; su vencimiento posterior no invalida el despliegue ya comprobado.

## Pendientes para declarar la entrega completa

- Equipo: revisar los contenidos y completar/confirmar el informe, sus justificaciones, conclusiones y la reflexión personal de cada integrante sin IA, conforme a la pauta. Permanecen pendientes según la última confirmación disponible del usuario.
- Declarar/citar la asistencia efectivamente utilizada y validar las fuentes. Confirmar integrantes y plazo.
- Verificar los checks del head final después de integrar esta actualización documental.
- Entregar el enlace [del repositorio](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api) por AVA y correo al docente. No se realizó ningún envío.

Un tag/release adicional puede mejorar la referencia de versión, pero no figura como requisito textual independiente de esta E2. Las auditorías fechadas conservan sus fotografías históricas; este documento centraliza el cierre técnico actual sin reescribir esos resultados.
