# Revisión inicial de la Evaluación 2 — DOY0101

Fecha: 26 de octubre de 2026.

Documento de asistencia y planificación generado con Codex a solicitud del usuario. Debe ser revisado por el equipo y no presentarse como su análisis académico, justificación técnica, conclusión o reflexión individual.

## Fuentes y alcance

- [Guía maestra](GUIA_MAESTRA_E2_DOY0101.md): copia íntegra del Markdown proporcionado por el usuario, conservada sin modificaciones.
- Pauta oficial consultada: `C:\Users\Admin\Downloads\EP2_DOY0101_Estudiante.pdf`, cinco páginas. Página 2: requisitos; página 3: uso de IA; páginas 4–5: rúbrica.
- Material de clase contrastado mediante extracción de los pasajes pertinentes de `semana-5.pdf` a `semana-11.pdf`, en Descargas. No se declara una revisión exhaustiva de todos los materiales enumerados en la guía.
- Repositorio local inspeccionado en `C:\proyectos\inventory-api`, rama `main`, commit `3dd4079c8cfb250be17e68114daee75f6b7cf8e7`.

El remoto `origin` corresponde a `D1E60-C4RR1LL0/despensa-inteligente-api`; `upstream` corresponde a `oscar503sv/inventory-api`. Esto explica la diferencia entre el nombre de la carpeta local y el de la guía.

Los PDF siguen fuera del repositorio. Si cambian de ubicación, habrá que localizar las fuentes antes de resolver discrepancias académicas. No se consultaron ejecuciones remotas de Actions, alertas de Dependabot, protecciones de ramas, secretos ni releases publicados. Las referencias Git locales no prueban el estado actual de GitHub.

## Requisitos confirmados con la pauta

Actualización posterior a esta revisión inicial: consultar [AUDITORIA_DOCKER.md](AUDITORIA_DOCKER.md) para el Dockerfile, la exclusión de archivos locales, la configuración JWT por entorno y el build incorporado al workflow. La tabla siguiente conserva el estado inicial de E1; no representa el estado actual de esta rama.

El bloque siguiente está registrado en [AUDITORIA_COMPOSE.md](AUDITORIA_COMPOSE.md): orquestación de API/MySQL con inicialización por Alembic, volumen, red y healthchecks. Docker y Compose ya se verificaron en CI, incluyendo el merge del PR #7. El bloque actual se registra en [AUDITORIA_SEGURIDAD.md](AUDITORIA_SEGURIDAD.md): configuración Dependabot/Snyk, correcciones de dependencias y autorización, con 61 pruebas aprobadas. La primera ejecución real de Snyk bloqueó la imagen por una incidencia crítica de certifi. Tras corregirla y ajustar la subida de informes ocultos, el [CI final del bloque](https://github.com/D1E60-C4RR1LL0/despensa-inteligente-api/actions/runs/40628651678) aprobó los tres jobs y se descargaron y verificaron los dos JSON de seguridad. La auditoría registra también la imagen probada y los identificadores del artefacto. Siguen pendientes la activación de la planificación Dependabot en main y el despliegue automático.

Cada indicador vale 20% de la E2. La evaluación completa tiene una ponderación de 45% en la asignatura, según la primera página de la pauta.

| Indicador | Exigencia confirmada | Estado local observado | Trabajo pendiente |
|---|---|---|---|
| IE1 | Dockerfile y construcción de imagen en GitHub Actions. | Sin Dockerfile ni `.dockerignore`; el CI solo ejecuta pruebas. | Contenerizar, verificar arranque y construir la imagen en CI. |
| IE2 | Pruebas unitarias automatizadas en CI, alineadas con las políticas de calidad. | PyTest configurado; 49 pruebas aprobadas localmente. La suite utiliza API y base de datos. | Distinguir pruebas unitarias de integración, revisar casos críticos, definir la política y verificarla en Actions. |
| IE3 | Dependabot, análisis de código con SonarQube o Snyk y alertas o bloqueos ante fallos de seguridad. La rúbrica también evalúa escalabilidad y gobernanza. | Sin configuración versionada de Dependabot ni análisis de seguridad en el workflow. | Configurar los controles, comprobar su ejecución y documentar parámetros de seguridad y escalabilidad con evidencia. |
| IE4 | Despliegue automático en entorno simulado y README que explique pipeline, trazabilidad y calidad. | El README describe CI y reconoce que no hay CD completo. | Implementar despliegue y validación funcional, relacionar commit, ejecución, imagen y despliegue. |
| IE5 | Orquestación con Kubernetes o Docker Compose. | Sin archivos de orquestación en el repositorio inspeccionado. | Elegir la alternativa y demostrar comunicación, persistencia, salud y funcionamiento estable. |

La pauta confirma el trabajo en parejas y las cinco semanas de desarrollo. También exige entregar el enlace de GitHub por AVA y correo; no se verificó una fecha límite concreta. No se realizó ninguna entrega ni envío.

## Precisiones necesarias al usar la guía

1. **La sección 2 refleja correctamente los requisitos principales.** Las listas posteriores de evidencias y Definition of Done amplían algunas decisiones de implementación; no todas sus casillas son obligaciones textuales de la pauta.
2. **Seguridad:** se exige Dependabot más una alternativa de análisis de código: SonarQube o Snyk. Las secciones 30 y 38 enumeran SCA y SAST por separado; eso no obliga a instalar simultáneamente Snyk y SonarQube. Los materiales de semanas 10–11 presentan Snyk para dependencias y SonarCloud para código. Al elegir herramienta, verificar el tipo de análisis que realmente se ejecutará. El uso de SonarCloud como equivalente de la alternativa textual SonarQube debe contrastarse con el criterio docente.
3. **Alertas o bloqueos:** la pauta admite ambas alternativas. Convertir seguridad en una puerta que impida desplegar es una decisión de implementación coherente con las clases, pero no debe describirse como la única opción literal permitida.
4. **Cobertura:** la pauta no fija 80%. Ese número aparece en ejemplos de clase. El 82% medido aquí es cobertura global de sentencias; no equivale a cobertura de código nuevo ni garantiza por sí solo la cobertura de todos los casos críticos.
5. **Pruebas unitarias:** usar PyTest no convierte todas las pruebas en unitarias. La suite inspeccionada incluye pruebas con `TestClient`, sesiones SQLAlchemy y SQLite. La semana 8, páginas 9–10, distingue explícitamente pruebas aisladas de las que interactúan con base de datos.
6. **Escalabilidad:** IE3 e IE5 la incluyen en la rúbrica. La guía debe utilizarse para planificar cómo demostrarla, no solo para marcar la presencia de escáneres y un archivo Compose. No hay valores de réplicas o recursos definidos por la pauta que se puedan copiar automáticamente.
7. **Opciones adicionales:** Kubernetes, cloud de pago, DAST con ZAP, hadolint, actionlint, multi-stage, pruebas negativas y un porcentaje fijo de cobertura no son requisitos textuales independientes de esta pauta. Su inclusión requiere una necesidad o decisión documentada del equipo.
8. **Uso de IA:** la sección 40 de la guía afirma que Codex puede ayudar con análisis e implementación. La página 3 de la pauta no concede expresamente ese alcance: permite apoyo de redacción, referencias y diagramas; exige ideas, análisis y justificaciones propios del equipo; prohíbe redactar con IA conclusiones, justificaciones técnicas y reflexiones individuales. La autorización académica para generar implementación con IA queda por verificar. No debe inferirse del Markdown. Todo uso debe declararse y citarse.

Estas precisiones acompañan la guía original sin alterar su contenido ni sustituir la pauta oficial.

## Hallazgos técnicos del repositorio

Comprobación y corrección posterior: la [auditoría de arranque](AUDITORIA_ARRANQUE.md) confirmó siete tablas pendientes y documenta su resolución mediante la revisión `f3171e47e124`. Las migraciones ya reconstruyen el esquema completo en SQLite y MySQL temporales, y la aplicación dejó de crear tablas al importar. Los hallazgos que siguen describen la fotografía inicial de E1; consultar la auditoría para el estado de esta corrección.

### Base aprovechable de la E1

- FastAPI y SQLAlchemy; dependencias fijadas en `requirements.txt`.
- PyTest y `pytest-cov` ya incluidos; configuración de descubrimiento en `pytest.ini`.
- `DATABASE_URL` se obtiene del entorno tanto en la aplicación como en Alembic.
- CI configurado con Python 3.12. El entorno virtual local utiliza Python 3.12.6.
- Existen referencias locales de `main`, `develop`, `feature/*`, `hotfix/*` y el tag `v1.0.0`.

### Aspectos a resolver antes de automatizar despliegues

- **Clave de JWT:** `utils/utils.py` define `SECRET_KEY` como literal. La configuración de base de datos por entorno no implica que todos los secretos estén externalizados. Debe revisarse esta configuración para E2; el valor no se reproduce aquí.
- **Arranque y base de datos:** `app.py` llama a `Base.metadata.create_all(bind=engine)` al importar el módulo. El arranque requiere que la base de datos esté disponible y puede crear tablas. La secuencia de disponibilidad, migraciones y arranque debe verificarse antes de preparar Compose.
- **Migraciones:** `96d6a5dc9e44_initial_migration.py` crea `users` y `token_blacklist`; `0c11a0e481fc_create_tables.py` tiene un `upgrade()` vacío. No puede afirmarse que `alembic upgrade head` por sí solo reconstruya todo el esquema de inventario. Conservar las migraciones y validar la estrategia contra una base vacía antes de modificarla.
- **Aislamiento de pruebas:** `tests/conftest.py` importa la aplicación antes de crear las fixtures, y usa después `sqlite:///./test.db`. Para esta auditoría se fijó `DATABASE_URL=sqlite:///:memory:` antes de importar, evitando que `create_all` se conectara al MySQL del `.env` local.
- **Eventos del CI:** el workflow se activa por `push` a `develop` y por PR hacia `main`. No contiene eventos de PR hacia `develop` ni de despliegue tras integrar en `main`. Revisar los eventos al diseñar E2 respetando el flujo de ramas existente.
- **Políticas de calidad:** `pytest-cov` está instalado, pero el workflow solo ejecuta `pytest`; no genera cobertura ni impone un umbral. Tampoco se verificaron protecciones de rama que requieran los checks para permitir merge.

## Evidencia local de pruebas

Comando ejecutado desde la raíz en PowerShell:

```powershell
$env:DATABASE_URL = 'sqlite:///:memory:'
.\venv\Scripts\python.exe -m pytest -q -o log_cli=false --cov=app --cov=config --cov=models --cov=routes --cov=schemas --cov=utils --cov-report=term-missing
```

Resultado: **49 passed, 4 warnings in 11.52s**, código de salida 0. Cobertura de sentencias: **82%**, sobre 912 sentencias, con 167 sin ejecutar. Esta medición incluye los módulos indicados y no incluye migraciones ni archivos de pruebas. No se estableció un umbral de aprobación.

| Módulo | Cobertura observada |
|---|---:|
| `app.py` | 100% |
| `routes/productos.py` | 94% |
| `routes/categorias.py` | 93% |
| `routes/movimientos.py` | 88% |
| `routes/profile.py` | 58% |
| `routes/tipos_movimiento.py` | 51% |
| `routes/stocks.py` | 46% |
| `routes/ubicaciones.py` | 46% |
| `routes/proveedores.py` | 40% |

Los cuatro avisos son `SAWarning: transaction already deassociated from connection`, originados en el rollback de la fixture durante pruebas de restricciones de modelos. No produjeron fallos; queda pendiente revisar su causa al trabajar sobre las fixtures.

Esta evidencia acredita la ejecución local sobre SQLite. No acredita ejecución actual en GitHub Actions, compatibilidad de despliegue con MySQL, análisis de seguridad ni funcionamiento de contenedores.

## Secuencia de trabajo propuesta para el equipo

1. Resolver las precisiones académicas: alcance del uso de IA y, si corresponde, equivalencia de la herramienta elegida para análisis de código.
2. Revisar arranque, configuración JWT y reconstrucción del esquema desde una base vacía. Fijar las decisiones de configuración con evidencia del proyecto.
3. Preparar Dockerfile y `.dockerignore`; comprobar construcción y arranque. No fijar versiones de imágenes o configuraciones sin verificarlas al implementar.
4. Implementar orquestación. Compose es una alternativa admitida por la pauta para representar la API y MySQL existentes; falta acordar la elección. Verificar salud, inicialización y persistencia.
5. Ampliar CI: política de pruebas y cobertura, casos críticos y construcción de imagen. Distinguir unitarias de integración y revisar los eventos del workflow.
6. Incorporar Dependabot y el análisis de código elegido. Definir alertas o bloqueos y comprobar su comportamiento. Evaluar también los parámetros de escalabilidad exigidos por la rúbrica.
7. Automatizar despliegue y comprobación funcional del entorno simulado, conservando la relación entre commit, imagen y ejecución.
8. Actualizar README y reunir evidencias por IE1–IE5. El equipo debe elaborar sus análisis, justificaciones y reflexiones académicas según la pauta.

La documentación y las evidencias deben actualizarse durante cada etapa. Crear archivos no equivale a completar un indicador. Esta revisión inicial se conserva como línea base. La corrección posterior del esquema y del arranque está registrada en la auditoría enlazada; el pipeline de despliegue sigue pendiente.

## Integridad de las fuentes iniciales

SHA-256 del Markdown original y de la copia inicial antes de incorporarla a Git:

```text
8674068E118A92623D1BF9A8DC5E93A5863A3D1B0BD037ADFA8BA4E442F4F8D1
```

Git puede normalizar los finales de línea al hacer checkout en Windows y cambiar ese hash de bytes. Tras el checkout de la rama Docker se comprobó que el contenido textual sigue siendo idéntico al original al normalizar LF/CRLF, y que la guía no tiene modificaciones en el diff.

SHA-256 de la pauta oficial consultada:

```text
BAAF0C3C02FB61FA881F76E4DAEA3A226408C24185CF72E0510F30C9E658E59D
```
