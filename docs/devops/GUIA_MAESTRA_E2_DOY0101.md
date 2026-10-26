# Guía Maestra de Trabajo --- Evaluación 2 DOY0101 Ingeniería DevOps

> **Propósito:** documento de orientación técnica y académica para
> trabajar la Evaluación 2 sobre el repositorio
> `despensa-inteligente-api`.
>
> **Regla principal:** este documento distingue entre requisitos de la
> evaluación, contenidos enseñados en clases, estado real del
> repositorio y recomendaciones de implementación. No se debe convertir
> una recomendación en un requisito.
>
> **Regla anti-alucinación:** si un dato técnico, nombre de archivo,
> versión, puerto, secreto, servicio cloud, comando o configuración no
> está respaldado por la evaluación, los materiales de clase o el
> repositorio actual, **NO debe inventarse**. Debe inspeccionarse el
> repositorio, verificarse con documentación oficial de la herramienta o
> quedar marcado como `TODO / POR VERIFICAR`.

------------------------------------------------------------------------

## 0. Cómo utilizar este documento

Este Markdown está pensado para ser usado como documento de trabajo
dentro de un repositorio con Codex.

Codex debe utilizarlo como **guía de orientación**, no como autorización
para asumir que todo lo descrito ya existe.

Cada tarea debe seguir este orden:

1.  Leer este documento.
2.  Leer la evaluación oficial `EP2_DOY0101_Estudiante.pdf`.
3.  Revisar los materiales de clase correspondientes.
4.  Inspeccionar el estado real del repositorio.
5.  Comparar requisito vs. estado actual.
6.  Implementar solamente lo que esté respaldado por las fuentes.
7.  Probar localmente.
8.  Probar en GitHub Actions.
9.  Registrar evidencias.
10. Actualizar la documentación.
11. No declarar una tarea como terminada si no existe evidencia
    verificable.

### Jerarquía de fuentes

Cuando exista una contradicción o una duda, utilizar esta prioridad:

1.  **Evaluación oficial E2 (`EP2_DOY0101_Estudiante.pdf`)** ---
    determina qué se evalúa.
2.  **Materiales oficiales de clase** --- determinan conceptos,
    procedimientos y herramientas enseñadas.
3.  **Repositorio actual** --- determina qué existe realmente y cómo
    está implementado.
4.  **Documentación oficial de la herramienta** --- sirve para resolver
    detalles técnicos de implementación.
5.  **Conocimiento general** --- solamente como apoyo y nunca para
    inventar requisitos.

------------------------------------------------------------------------

# 1. Identificación de la evaluación

**Curso:** DOY0101 --- Ingeniería DevOps

**Evaluación:** Evaluación 2 / EP2

La evaluación busca automatizar el ciclo de vida del microservicio
mediante un pipeline CI/CD implementado en GitHub Actions.

La evaluación utiliza como base un microservicio existente desarrollado
anteriormente.

Los objetivos explícitos son incorporar:

-   pruebas automatizadas;
-   análisis de seguridad;
-   uso de contenedores;
-   despliegue automatizado;
-   orquestación.

El encargo se realiza en parejas y el documento de evaluación establece
cinco semanas para desarrollarlo.

La entrega se realiza mediante un enlace al repositorio GitHub, que debe
ser subido en AVA y enviado por correo al docente dentro del plazo
establecido.

------------------------------------------------------------------------

# 2. Requisitos explícitos de la E2

La evaluación oficial exige:

## 2.1 Dockerfile

Crear un `Dockerfile` para contenerizar el microservicio.

**Indicador:** IE1.

## 2.2 Pipeline en GitHub Actions

El pipeline debe incluir:

### Construcción de imagen Docker

**Indicador:** IE1.

### Pruebas unitarias

Pruebas automatizadas usando PyTest, JUnit o similares.

**Indicador:** IE2.

En nuestro proyecto corresponde utilizar **PyTest**.

### Escaneo de dependencias

La evaluación solicita **Dependabot**.

**Indicador:** IE3.

### Análisis de código

La evaluación solicita **SonarQube o Snyk**.

**Indicador:** IE3.

La evaluación utiliza literalmente la formulación:

> "Escaneo de dependencias con Dependabot y análisis de código con
> SonarQube o Snyk."

No reinterpretar esta frase como obligación de implementar herramientas
adicionales sin comprobar el criterio.

### Despliegue automático

Debe existir un despliegue automático en un entorno simulado, por
ejemplo:

-   Docker Compose;
-   o una nube de preferencia.

**Indicador:** IE4.

### Alertas o bloqueos de seguridad

Deben configurarse alertas o bloqueos cuando el análisis de seguridad
falle.

**Indicador:** IE3.

### Orquestación

Debe utilizarse:

-   Kubernetes;
-   o Docker Compose.

**Indicador:** IE5.

### Documentación

El `README.md` debe documentar el pipeline y describir cómo se
garantiza:

-   trazabilidad;
-   calidad.

**Indicador:** IE4.

------------------------------------------------------------------------

# 3. Indicadores y ponderación

  Indicador   Tema                                     Ponderación
  ----------- -------------------------------------- -------------
  IE1         Contenedores                                     20%
  IE2         Pruebas automatizadas en CI                      20%
  IE3         Escalabilidad y seguridad                        20%
  IE4         Despliegue automático y trazabilidad             20%
  IE5         Orquestación                                     20%
  **Total**                                               **100%**

Categorías:

  Categoría                Logro
  ---------------------- -------
  Muy buen desempeño        100%
  Buen desempeño             80%
  Desempeño aceptable        60%
  Desempeño incipiente       30%
  Desempeño no logrado        0%

La categoría de 100% exige demostrar todos los aspectos evaluados del
indicador.

------------------------------------------------------------------------

# 4. Rúbrica resumida

## IE1 --- Contenedores --- 20%

### 100%

-   contenedores incorporados eficazmente;
-   imágenes optimizadas;
-   configuraciones adecuadas;
-   facilidad para trabajar con aplicaciones modernas en entornos de
    nube.

### 80%

-   contenedores adecuados;
-   despliegue funcional;
-   alineación con soluciones en nube.

### 60%

-   contenedores básicos;
-   ejecución funcional;
-   configuración limitada.

### 30%

-   implementación parcial;
-   errores importantes;
-   dificultades de uso.

### 0%

No incorpora contenedores.

------------------------------------------------------------------------

## IE2 --- Pruebas automatizadas --- 20%

### 100%

-   casos críticos cubiertos;
-   ejecución correcta dentro del pipeline;
-   cumplimiento de políticas de calidad.

### 80%

Pruebas funcionales automatizadas, con cobertura parcial o pequeñas
desviaciones.

### 60%

Pruebas existentes pero incompletas o poco relacionadas con políticas de
calidad.

### 30%

Implementación mínima o poco coherente con CI.

### 0%

No hay pruebas automatizadas en el pipeline.

------------------------------------------------------------------------

## IE3 --- Escalabilidad y seguridad --- 20%

### 100%

-   parámetros de escalabilidad y seguridad ajustados de forma precisa;
-   alineación con estándares de desempeño;
-   gobernanza;
-   entrega continua segura en arquitectura basada en contenedores.

### 80%

Parámetros clave de escalabilidad y seguridad correctamente
configurados, con leves áreas de mejora.

### 60%

Parámetros básicos, pero cumplimiento incompleto.

### 30%

Configuración superficial o incorrecta.

### 0%

No se ajustan parámetros de escalabilidad ni seguridad.

------------------------------------------------------------------------

## IE4 --- Despliegue automático y trazabilidad --- 20%

### 100%

-   despliegue automático;
-   aplicación funcional;
-   proceso completo;
-   trazabilidad;
-   pipeline bien configurado;
-   entorno cloud simulado.

### 80%

Despliegue automático funcional, con trazabilidad parcial o detalles
menores.

### 60%

Automatización limitada o errores en trazabilidad.

### 30%

Intento de automatización con fallas significativas.

### 0%

No existe despliegue automático.

------------------------------------------------------------------------

## IE5 --- Orquestación --- 20%

### 100%

-   orquestación eficiente;
-   escalabilidad;
-   funcionamiento estable;
-   soluciones complejas.

### 80%

Orquestación correcta, con diseño funcional y adaptable.

### 60%

Orquestación existente, pero con limitaciones técnicas o estructurales.

### 30%

Orquestación básica o ineficiente.

### 0%

No existe orquestación.

------------------------------------------------------------------------

# 5. Estado real actual del repositorio

Repositorio:

`D1E60-C4RR1LL0/despensa-inteligente-api`

## Stack

-   Python;
-   FastAPI;
-   SQLAlchemy;
-   Pydantic;
-   MySQL;
-   Alembic;
-   PyTest;
-   Git;
-   GitHub;
-   GitHub Actions.

## Funcionalidades existentes

-   autenticación;
-   JWT;
-   roles;
-   categorías;
-   proveedores;
-   ubicaciones;
-   productos;
-   stock;
-   movimientos de inventario;
-   alertas de stock bajo;
-   lista de compras;
-   exclusión de productos inactivos en alertas;
-   migraciones Alembic;
-   pruebas automatizadas;
-   CI. 

## Git

Existen:

-   `main`;
-   `develop`;
-   `feature/*`;
-   `hotfix/*`.

También existen Pull Requests y release `v1.0.0`.

## CI

Existe:

`.github/workflows/ci.yml`

El pipeline actual ejecuta las pruebas.

## Tests

La versión estable documenta 49 pruebas automatizadas exitosas.

## Configuración

La conexión de base de datos utiliza variables de entorno, incluyendo
`DATABASE_URL`.

------------------------------------------------------------------------

# 6. Estado E2 al comenzar

  Indicador   Estado inicial   Observación
  ----------- ---------------- ---------------------------------
  IE1         PENDIENTE        No asumir Docker implementado
  IE2         AVANZADO         PyTest + CI ya existen
  IE3         PENDIENTE        Verificar/implementar seguridad
  IE4         PENDIENTE        No existe CD completo
  IE5         PENDIENTE        No asumir Compose existente

La evaluación debe medirse por la rúbrica, no por cantidad de archivos
creados.

------------------------------------------------------------------------

# 7. Contenido clase por clase

## Semana 1 --- DevOps, Git y branching

### DevOps

El material presenta DevOps como un conjunto de prácticas que integra
desarrollo y operaciones mediante automatización y colaboración
continua.

No debe entenderse simplemente como:

-   una herramienta;
-   un cargo;
-   automatización aislada;
-   reemplazo de Agile/Scrum.

### Las Tres Vías

1.  **Flujo:** optimizar el trabajo de Dev hacia Ops y producción.
2.  **Retroalimentación:** detectar y corregir problemas rápidamente.
3.  **Aprendizaje continuo:** experimentar y mejorar.

### Ecosistema

Se presentan:

-   Git / GitHub;
-   GitHub Actions;
-   Docker;
-   Docker Compose;
-   Kubernetes;
-   Terraform;
-   AWS/Azure/Google Cloud.

### Branching

Se revisan:

-   GitFlow;
-   GitHub Flow;
-   TBD;
-   Feature Branch.

### Pull Request

Sirve para:

-   revisión;
-   discusión;
-   comentarios;
-   ejecución de pruebas;
-   trazabilidad.

### Aplicación

El proyecto ya utiliza una estrategia de ramas y PR. No modificarla sin
una razón relacionada con E2.

------------------------------------------------------------------------

# 8. Semana 2 --- GitHub Actions y CI/CD

## Pipeline como código

El pipeline vive dentro del repositorio.

GitHub Actions permite definir workflows en YAML.

Ventajas:

-   versionamiento;
-   revisión;
-   auditoría;
-   reproducibilidad.

## GitHub Secrets

Los secretos no deben quedar en código.

Aplicar esto a:

-   Snyk;
-   Sonar;
-   registries;
-   cloud;
-   cualquier token.

Nunca escribir credenciales reales dentro de archivos versionados.

------------------------------------------------------------------------

# 9. Semana 3 --- Documentación

Contenido:

-   código autoexplicado;
-   documentación cercana al código;
-   Markdown;
-   archivos estándar;
-   documentación del proceso;
-   documentación automatizada.

Aplicación a E2:

El README debe evolucionar junto con el pipeline y explicar:

-   ejecución;
-   tests;
-   Docker;
-   Compose;
-   CI;
-   seguridad;
-   CD;
-   trazabilidad;
-   calidad.

------------------------------------------------------------------------

# 10. Semana 4 --- Material no disponible

No se encontró en los materiales disponibles un archivo claramente
identificado como `semana-4.pdf`.

Por lo tanto:

**NO INVENTAR EL CONTENIDO DE LA SEMANA 4.**

Si se incorpora posteriormente el material oficial, debe agregarse aquí.

------------------------------------------------------------------------

# 11. Semana 5 --- Docker, Dockerfile y Multi-stage

## Docker

Resuelve problemas de diferencias entre ambientes.

Un contenedor empaqueta:

-   aplicación;
-   dependencias;
-   configuración de entorno.

## Docker no es

Según el material:

-   una máquina virtual;
-   un sistema operativo completo;
-   un orquestador;
-   sustituto de seguridad del host;
-   solución automática a una mala arquitectura.

## Conceptos

-   imagen;
-   contenedor;
-   registry;
-   networking.

## Dockerfile

Se estudian:

-   `FROM`;
-   `RUN`;
-   `COPY`;
-   `ENV`;
-   `EXPOSE`;
-   `WORKDIR`;
-   `CMD`;
-   `ENTRYPOINT`;
-   `VOLUME`.

No todas deben aparecer en nuestro Dockerfile.

## Multi-stage

Se enseña para optimizar imágenes y separar etapas.

También se estudia la caché de capas.

### Regla

No utilizar Multi-stage solamente para cumplir una lista. Debe tener
sentido para el proyecto.

------------------------------------------------------------------------

# 12. Semana 6 --- Docker Compose

Docker Compose permite definir aplicaciones compuestas por múltiples
contenedores mediante YAML.

Conceptos:

-   servicios;
-   redes;
-   volúmenes;
-   dependencias.

`depends_on` establece dependencia de inicio, pero no garantiza por sí
mismo que el servicio esté listo.

Por eso deben evaluarse:

-   healthchecks;
-   condiciones de salud;
-   inicialización.

------------------------------------------------------------------------

# 13. Semana 7 --- Compose avanzado

Se estudian:

-   `build`;
-   variables de entorno;
-   `env_file`;
-   volúmenes;
-   redes;
-   `restart`;
-   `ulimits`;
-   dependencias;
-   healthchecks.

Comandos enseñados:

``` bash
docker compose up --build
docker compose down -v
docker compose config
docker compose top
docker compose stats
```

También se muestra la posibilidad de archivos Compose separados por
ambiente.

## Compose vs Kubernetes

Compose sirve bien para:

-   desarrollo local;
-   CI/CD en un solo nodo;
-   despliegues simples.

Kubernetes entra cuando se necesitan capacidades como:

-   múltiples nodos;
-   alta disponibilidad;
-   autoscaling;
-   rolling updates.

Para E2, la pauta permite Docker Compose o Kubernetes.

------------------------------------------------------------------------

# 14. Semana 8 --- Pruebas unitarias y cobertura

## Commit Stage

Es la primera puerta de calidad.

Si falla, el pipeline debe detenerse.

## Pirámide

-   unitarias: muchas, rápidas;
-   integración: intermedias;
-   E2E: pocas, lentas.

## AAA

Las pruebas se estructuran conceptualmente como:

``` text
Arrange
Act
Assert
```

## Cobertura

El material presenta como referencia un rango de 70--80% y ejemplos con
`pytest-cov`.

Ejemplo de clase:

``` bash
pytest tests/ --cov=src --cov-fail-under=80
```

**Importante:** ese comando es un ejemplo del material. No asumir que
nuestro proyecto debe usar exactamente 80% sin medir y definir la
política correspondiente.

## Proyecto actual

Ya existen:

-   PyTest;
-   pytest-cov;
-   49 pruebas;
-   ejecución en CI.

------------------------------------------------------------------------

# 15. Semana 9 --- Pruebas del pipeline y "todo como código"

El material amplía el concepto de calidad a otros artefactos.

  Artefacto    Herramienta            Función
  ------------ ---------------------- ----------------------------
  Código       pytest/Jest/JUnit      detectar errores
  Dockerfile   hadolint               malas prácticas
  IaC          fmt/validate/checkov   sintaxis/formato/seguridad
  Workflow     actionlint             sintaxis del workflow

## Principio

Todo lo que está como código puede:

-   versionarse;
-   revisarse;
-   probarse.

## Actionlint

Puede validar:

``` bash
actionlint .github/workflows/*.yml
```

## Hadolint

Puede revisar Dockerfiles.

No es un requisito textual independiente de la rúbrica, sino una
herramienta enseñada que puede reforzar IE1.

------------------------------------------------------------------------

# 16. Semana 10 --- DevSecOps

## Shift-left

La seguridad debe incorporarse temprano.

## DevSecOps

Integra:

-   Dev;
-   Security;
-   Ops.

La seguridad pasa a ser responsabilidad compartida.

## Tres categorías

### SCA

Analiza dependencias.

Herramienta enseñada:

**Snyk**

Alternativas mostradas:

-   Trivy;
-   OWASP Dependency-Check.

### SAST

Analiza código fuente.

Herramienta enseñada:

**SonarCloud**

Alternativa:

**SonarQube Community Build**

### DAST

Analiza la aplicación en ejecución.

Herramienta enseñada:

**OWASP ZAP**

------------------------------------------------------------------------

# 17. Snyk, CVE y CVSS

Snyk se enseña como herramienta SCA.

El material muestra integración mediante GitHub Actions y un umbral de
severidad.

Principio:

``` text
SCA
 |
 +-- hallazgo sobre umbral --> FAIL
 |
 +-- sin hallazgo bloqueante --> PASS
```

### CVE

Identificador de vulnerabilidad conocida.

### CVSS

Escala de severidad.

No inventar vulnerabilidades.

Si aparece una vulnerabilidad:

1.  identificar dependencia;
2.  identificar CVE;
3.  revisar severidad;
4.  revisar versión afectada;
5.  revisar versión corregida;
6.  corregir;
7.  volver a ejecutar;
8.  conservar evidencia.

------------------------------------------------------------------------

# 18. Semana 11 --- SonarCloud, Quality Gate y DAST

## SonarCloud

Permite analizar:

-   bugs;
-   vulnerabilidades;
-   cobertura;
-   code smells;
-   deuda técnica.

## Quality Gate

Actúa como compuerta.

El material muestra como ejemplo:

-   nuevas vulnerabilidades: 0;
-   nuevos bugs: 0;
-   cobertura de código nuevo \>= 80%;
-   deuda técnica de código nuevo \<= A.

Estos son valores del ejemplo de clase. No asumir que deben copiarse sin
revisar la configuración real.

Si el Quality Gate falla:

``` text
Quality Gate FAIL
       ↓
Job FAIL
       ↓
Pipeline detenido
```

## `fetch-depth`

El material advierte que SonarCloud requiere historial suficiente para
ciertos análisis y muestra `fetch-depth: 0`.

No copiar configuraciones sin verificar el workflow real.

## DAST

DAST requiere la aplicación ejecutándose.

El material lo ubica conceptualmente como:

``` text
CI:
build → test → SCA → SAST

CD:
deploy staging → DAST → producción
```

OWASP ZAP es la herramienta enseñada.

**Importante:** DAST forma parte de los contenidos del curso, pero la
pauta E2 no lo establece explícitamente como requisito obligatorio. No
convertirlo en requisito sin instrucción adicional.

------------------------------------------------------------------------

# 19. Arquitectura objetivo

La arquitectura debe derivarse del repositorio real.

Conceptualmente:

``` text
GitHub
   |
   v
GitHub Actions
   |
   +--> Tests
   |
   +--> Calidad
   |
   +--> Seguridad
   |
   +--> Docker Build
   |
   +--> Deploy
            |
            v
       Docker Compose
          |
          +--> API
          |
          +--> Base de datos
```

No inventar servicios como Redis, Nginx, frontend u otros si no son
necesarios.

------------------------------------------------------------------------

# 20. Pipeline objetivo

Una estructura conceptual posible:

``` text
Checkout
   |
   v
Validación
   |
   v
Instalación
   |
   v
Tests
   |
   v
Cobertura / calidad
   |
   v
Seguridad
   |
   v
Docker build
   |
   v
Deploy
   |
   v
Validación
```

La secuencia final debe derivarse de dependencias reales.

No crear jobs artificialmente encadenados.

------------------------------------------------------------------------

# 21. Contenerización del proyecto actual

Antes de crear Dockerfile, inspeccionar:

-   `requirements.txt`;
-   `app.py`;
-   configuración de DB;
-   variables;
-   comando de inicio;
-   tests;
-   Alembic;
-   README.

Determinar con evidencia:

-   imagen base;
-   versión de Python;
-   `WORKDIR`;
-   instalación;
-   archivos;
-   comando;
-   variables.

El workflow actual utiliza Python 3.12, pero antes de fijar esa versión
en Docker debe verificarse que sea realmente la versión objetivo del
proyecto.

------------------------------------------------------------------------

# 22. `.dockerignore`

Evaluar exclusión de:

-   `.git`;
-   entornos virtuales;
-   cachés;
-   temporales;
-   resultados de tests;
-   archivos locales;
-   secretos.

No copiar secretos a la imagen.

------------------------------------------------------------------------

# 23. Docker Compose del proyecto

El Compose debe representar la arquitectura real.

Debe analizar:

-   `build`;
-   `image`;
-   `environment`;
-   `env_file`;
-   `ports`;
-   `depends_on`;
-   `healthcheck`;
-   `volumes`;
-   `networks`;
-   `restart`.

No agregar propiedades solamente porque aparecen en ejemplos de clase.

------------------------------------------------------------------------

# 24. Base de datos y Alembic

La aplicación utiliza MySQL, SQLAlchemy y Alembic.

Antes de configurar Compose hay que comprobar:

-   cómo se construye `DATABASE_URL`;
-   host;
-   nombre de DB;
-   usuario;
-   contraseña;
-   proceso de migración.

No inventar valores.

Las migraciones no deben modificarse o eliminarse para "hacer funcionar"
el pipeline.

Cualquier cambio destructivo debe revisarse antes.

------------------------------------------------------------------------

# 25. Variables y secretos

Separar:

### Configuración no sensible

Puede documentarse mediante ejemplos.

### Secretos

Utilizar:

-   GitHub Secrets;
-   variables de entorno;
-   mecanismos equivalentes.

Nunca versionar:

-   passwords;
-   tokens;
-   API keys;
-   credenciales cloud;
-   tokens Snyk;
-   tokens Sonar.

------------------------------------------------------------------------

# 26. Dependabot

La evaluación menciona Dependabot.

Debe comprobarse la configuración y comportamiento real en GitHub.

Objetivo:

-   detectar dependencias;
-   generar alertas o actualizaciones según configuración.

No afirmar que está implementado hasta verificarlo.

------------------------------------------------------------------------

# 27. Seguridad como puerta del pipeline

Modelo:

``` text
Código
  |
  v
Tests
  |
  v
Security
  |
  +---- FAIL --> detener
  |
  +---- PASS --> continuar
```

Esto debe quedar demostrado para IE3.

------------------------------------------------------------------------

# 28. Trazabilidad

Debe poder relacionarse:

``` text
Cambio
  ↓
Commit
  ↓
Branch
  ↓
Pull Request
  ↓
GitHub Actions
  ↓
Tests
  ↓
Security
  ↓
Build
  ↓
Deploy
```

No basta con una captura del pipeline.

Debe existir relación verificable entre código, commit, ejecución y
despliegue.

------------------------------------------------------------------------

# 29. Calidad

Los controles deben demostrar calidad.

Evaluar como mínimo:

-   tests;
-   cobertura;
-   workflow;
-   Dockerfile;
-   seguridad;
-   build;
-   deploy.

No escribir "el proyecto tiene calidad" sin explicar qué control lo
demuestra.

------------------------------------------------------------------------

# 30. Evidencias por indicador

## IE1

-   Dockerfile;
-   build exitoso;
-   imagen;
-   contenedor funcionando;
-   Docker build dentro de Actions.

## IE2

-   tests;
-   cantidad;
-   ejecución local;
-   ejecución en Actions;
-   cobertura si se implementa;
-   fallo controlado de prueba.

## IE3

-   Dependabot;
-   SCA;
-   SAST;
-   resultado;
-   alerta/bloqueo;
-   corrección.

## IE4

-   workflow;
-   deploy;
-   entorno simulado;
-   aplicación funcionando;
-   commit → pipeline → deploy.

## IE5

-   Compose/Kubernetes;
-   servicios;
-   redes;
-   volúmenes;
-   dependencias;
-   healthchecks;
-   stack funcionando.

------------------------------------------------------------------------

# 31. Pruebas negativas

No demostrar solamente que todo pasa.

## Test

Provocar temporalmente un fallo controlado:

``` text
test FAIL
→ pipeline FAIL
```

Revertir después.

## Seguridad

Cuando la herramienta y configuración lo permitan:

``` text
hallazgo sobre umbral
→ security FAIL
→ pipeline detenido
```

Después corregir.

## Docker

Puede realizarse una validación controlada de fallo de build.

No dejar el repositorio roto.

------------------------------------------------------------------------

# 32. Definition of Done

## Código

-   [ ] API funciona.
-   [ ] Tests funcionan.
-   [ ] No se eliminaron funcionalidades.
-   [ ] No hay secretos.

## Docker

-   [ ] Dockerfile existe.
-   [ ] Build funciona.
-   [ ] Imagen arranca.
-   [ ] API funciona dentro del contenedor.
-   [ ] Build está integrado al CI.

## Compose

-   [ ] Compose existe.
-   [ ] API y DB levantan.
-   [ ] Variables funcionan.
-   [ ] Persistencia está resuelta cuando corresponde.
-   [ ] Dependencias funcionan.
-   [ ] Healthcheck fue evaluado.

## CI

-   [ ] GitHub Actions funciona.
-   [ ] Tests corren automáticamente.
-   [ ] Tests fallidos bloquean.
-   [ ] Cobertura fue evaluada.
-   [ ] Workflow validado.
-   [ ] Docker build está integrado.

## Seguridad

-   [ ] Dependabot configurado.
-   [ ] SCA/SAST implementado según la evaluación.
-   [ ] Secrets configurados.
-   [ ] Umbral definido cuando corresponda.
-   [ ] Fallo de seguridad bloquea cuando corresponde.
-   [ ] Análisis real ejecutado.

## CD

-   [ ] Deploy automático.
-   [ ] Entorno simulado.
-   [ ] Pipeline conectado.
-   [ ] Trazabilidad.
-   [ ] Aplicación operativa.

## Orquestación

-   [ ] Compose/Kubernetes funciona.
-   [ ] Servicios se comunican.
-   [ ] Dependencias resueltas.
-   [ ] Stack reproducible.

## Documentación

-   [ ] README actualizado.
-   [ ] Arquitectura explicada.
-   [ ] Pipeline explicado.
-   [ ] Seguridad explicada.
-   [ ] Deploy explicado.
-   [ ] Trazabilidad explicada.
-   [ ] Comandos reproducibles.

------------------------------------------------------------------------

# 33. Reglas para Codex

## Antes de modificar

1.  Buscar si el archivo ya existe.
2.  Leer configuración relacionada.
3.  Revisar dependencias.
4.  Revisar tests.
5.  Revisar workflow.
6.  Revisar README.
7.  Comparar con E2.

## No hacer

No:

-   inventar archivos;
-   inventar secretos;
-   inventar puertos;
-   inventar servicios;
-   inventar resultados;
-   inventar requisitos;
-   afirmar que algo funciona sin probarlo;
-   modificar endpoints sin necesidad;
-   reescribir la API;
-   eliminar tests;
-   eliminar migraciones;
-   eliminar datos;
-   copiar literalmente ejemplos de otro lenguaje.

## Antes de afirmar "listo"

Debe existir evidencia de:

-   implementación;
-   ejecución;
-   resultado;
-   documentación.

------------------------------------------------------------------------

# 34. Clasificación de información

Usar estas etiquetas internamente:

### `[E2-OBLIGATORIO]`

Está explícitamente en la evaluación.

### `[CLASE]`

Fue enseñado.

### `[RECOMENDACIÓN]`

Es una decisión técnica útil, pero no un requisito textual.

### `[POR VERIFICAR]`

Debe comprobarse.

Esto evita que Codex transforme una sugerencia en una obligación.

------------------------------------------------------------------------

# 35. Herramientas

  Herramienta      Fuente              Uso
  ---------------- ------------------- ------------------------------
  Git              Clase               versionamiento
  GitHub           Clase/E1            repositorio
  GitHub Actions   Clase/E2            CI/CD
  Docker           Clase/E2            contenedores
  Docker Compose   Clase/E2            orquestación/deploy simulado
  PyTest           Proyecto/Clase/E2   pruebas
  pytest-cov       Clase               cobertura
  actionlint       Clase               validación workflow
  hadolint         Clase               validación Dockerfile
  Dependabot       E2                  dependencias
  Snyk             Clase/E2            seguridad
  SonarCloud       Clase               SAST
  SonarQube        E2/Clase            alternativa SAST
  OWASP ZAP        Clase               DAST
  Kubernetes       Clase/E2            alternativa a Compose

------------------------------------------------------------------------

# 36. Herramientas que no deben agregarse por defecto

No implementar automáticamente:

-   Kubernetes;
-   Terraform;
-   AWS;
-   Azure;
-   GCP;
-   Trivy;
-   Checkov;
-   Argo CD;
-   Jenkins;
-   Redis;
-   Nginx;
-   observabilidad adicional.

Primero debe existir una razón basada en:

-   evaluación;
-   clase;
-   arquitectura;
-   necesidad técnica.

------------------------------------------------------------------------

# 37. Plan de implementación

## Fase 0 --- Auditoría

Revisar:

-   estructura;
-   `ci.yml`;
-   requirements;
-   tests;
-   DB;
-   Alembic;
-   README.

Resultado: mapa real.

## Fase 1 --- Docker

-   Dockerfile;
-   `.dockerignore`;
-   build;
-   ejecución local.

## Fase 2 --- Compose

-   API;
-   DB;
-   variables;
-   red;
-   persistencia;
-   dependencias;
-   healthcheck si corresponde.

## Fase 3 --- CI

-   tests;
-   cobertura;
-   validación;
-   Docker build.

## Fase 4 --- Seguridad

-   Dependabot;
-   SCA/SAST según E2;
-   secrets;
-   umbral;
-   bloqueo.

## Fase 5 --- CD

-   despliegue automático;
-   entorno simulado;
-   validación.

## Fase 6 --- Orquestación

-   servicios;
-   redes;
-   persistencia;
-   dependencias;
-   salud.

## Fase 7 --- Trazabilidad

-   branch;
-   commit;
-   PR;
-   workflow;
-   build;
-   deploy;
-   versión.

## Fase 8 --- Documentación

Actualizar README y evidencias.

------------------------------------------------------------------------

# 38. Matriz requisito → evidencia

  Requisito       Archivo/configuración      Evidencia
  --------------- -------------------------- ------------------------------
  Docker          `Dockerfile`               build exitoso
  Docker CI       workflow                   job Docker
  Tests           `tests/`                   PyTest
  Cobertura       workflow/config            reporte
  Dependabot      `.github/dependabot.yml`   configuración/alertas
  SCA             workflow                   análisis
  SAST            workflow/config            análisis
  Bloqueo         workflow                   ejecución fallida controlada
  Compose         `docker-compose.yml`       stack funcional
  Deploy          workflow                   ejecución CD
  Trazabilidad    GitHub                     commit → workflow → deploy
  Documentación   `README.md`                explicación

------------------------------------------------------------------------

# 39. Revisión final de la rúbrica

## IE1

¿Puedo demostrar que usamos contenedores correctamente?

## IE2

¿Puedo demostrar que las pruebas son parte real del pipeline?

## IE3

¿Puedo demostrar que seguridad puede bloquear la entrega?

## IE4

¿Puedo demostrar un despliegue automático y trazable?

## IE5

¿Puedo demostrar que los contenedores están correctamente orquestados?

Si la respuesta es sí a las cinco, existe una base sólida para apuntar a
"Muy buen desempeño".

------------------------------------------------------------------------

# 40. Uso de IA en la E2

La evaluación establece:

## Permitido

IA como apoyo para:

-   mejorar redacción;
-   buscar referencias;
-   crear diagramas.

## Obligatorio

Declarar:

-   qué herramientas de IA se utilizaron;
-   cómo fueron utilizadas.

## Prohibido

No utilizar IA para redactar:

-   conclusiones;
-   justificaciones técnicas;
-   reflexiones individuales.

## Reflexión individual

Cada integrante debe redactar personalmente su reflexión sobre:

-   aprendizaje;
-   contribución;
-   experiencia.

Debe hacerse sin apoyo de IA.

### Regla para Codex

Codex puede ayudar con:

-   análisis;
-   implementación;
-   revisión;
-   documentación técnica.

Pero no debe redactar la reflexión individual que será presentada como
aprendizaje personal.

Todo contenido generado debe ser revisado y validado.

------------------------------------------------------------------------

# 41. Prueba final extremo a extremo

Antes de entregar:

``` text
Cambio
  ↓
Commit
  ↓
Push
  ↓
GitHub Actions
  ↓
Tests
  ↓
Calidad
  ↓
Seguridad
  ↓
Docker Build
  ↓
Deploy
  ↓
Compose
  ↓
API funcionando
```

Luego comprobar que GitHub permita rastrear:

``` text
commit
  ↓
workflow
  ↓
resultado
  ↓
versión/deploy
```

------------------------------------------------------------------------

# 42. Fuentes utilizadas

## Evaluación

-   `EP2_DOY0101_Estudiante.pdf`

## Material de clases

-   `semana-1.pdf`
-   `semana-2.pdf`
-   `semana-3.pdf`
-   `semana-5.pdf`
-   `semana-6.pdf`
-   `semana-7.pdf`
-   `semana-8.pdf`
-   `semana-9.pdf`
-   `semana-10.pdf`
-   `semana-11.pdf`

## Materiales complementarios

-   `1.1.1 Introducción a la cultura Devops.pdf`
-   `1.1.2 Git y modelos de trabajo.pdf`
-   `1.2.1 introduccion a Github Action.pdf`
-   `1.3.1 Documentación de Buenas Prácticas en versionamiento.pdf`
-   `2.1.1 Docker-Dockerfile-docker multi stage.pdf`
-   `2.2.1 Docker Compose.pdf`
-   `2.3.1 Pruebas Unitarias Jacoco.pdf`
-   `2.4.1 Añadiendo seguridad a nuestro Pipeline CI.pdf`

## Repositorio

`D1E60-C4RR1LL0/despensa-inteligente-api`

------------------------------------------------------------------------

# 43. Limitaciones deliberadas

No se debe inventar contenido de semanas para las cuales no existe
material disponible.

En particular:

-   no se encontró una fuente claramente identificada como
    `semana-4.pdf`;
-   no se debe inventar su contenido;
-   no se debe asumir que una semana posterior a la 11 es necesaria para
    E2 salvo instrucción oficial.

La evaluación oficial es la fuente definitiva para saber qué debe
entregarse.

------------------------------------------------------------------------

# 44. Regla final de trabajo

El objetivo no es crear "muchas cosas".

El objetivo es construir una cadena verificable:

``` text
Código
  ↓
Versionamiento
  ↓
CI
  ↓
Tests
  ↓
Calidad
  ↓
Seguridad
  ↓
Contenedor
  ↓
CD
  ↓
Orquestación
  ↓
Aplicación funcionando
```

Cada etapa debe:

-   existir;
-   ejecutarse;
-   poder fallar cuando corresponde;
-   producir evidencia;
-   ser trazable;
-   estar documentada.

**No implementar por intuición.**

**No asumir.**

**No inventar.**

**Inspeccionar → implementar → probar → verificar → documentar.**

Este es el criterio de trabajo que debe utilizar Codex durante toda la
construcción de la E2.
