# Cómo escribir un `prd.json` sólido para trabajo con el bucle Ralph

Guía práctica para ingenieros con visión de producto que quieran que los bucles de IA autónomos (Ralph, Ralph Zero, ralph-claude-code, ralph-copilot, etc.) realmente *terminen* el trabajo sin entrar en bucles improductivos.

> **Resumen** — El `prd.json` es el volante del bucle Ralph. El agente lo lee en cada iteración, escoge una tarea, la implementa, la marca como hecha y sale. Si el archivo está mal hecho, el bucle también lo estará. La parte más difícil de escribir un buen `prd.json` es **todo lo que haces antes de abrir el archivo.**

---

## 1. Contexto: qué es Ralph y por qué importa el `prd.json`

Ralph (la "técnica Ralph Wiggum" de Geoffrey Huntley) es un patrón deliberadamente sencillo: un bucle de bash reinicia un agente de codificación (Claude Code, Amp, Cursor CLI, etc.) una y otra vez con un contexto fresco. El estado vive en disco — normalmente `PROMPT.md`, `AGENTS.md`, `specs/*`, un `IMPLEMENTATION_PLAN.md` y un `prd.json` (o el equivalente como registro de tareas).

En cada iteración el agente:

1. Carga los mismos ficheros de forma determinista.
2. Escoge **una** tarea pendiente.
3. Investiga el código, implementa, ejecuta tests/typecheck/lint (la "contrapresión") y hace commit.
4. Actualiza el estado de la tarea y sale.
5. El bucle de bash arranca de nuevo con un contexto limpio.

`prd.json` es la lista de trabajo persistente y legible por máquina que sobrevive a esos reinicios. **No** es un documento de diseño en formato libre — es una cola de tareas atómicas y verificables. La calidad de este archivo determina si el bucle converge o gira eternamente en círculos.

---

## 2. PRD vs. BRD vs. MRD — y por qué importa antes de escribir JSON

Estos tres documentos parecen similares pero responden preguntas distintas. Un `prd.json` para Ralph es el *último* de ellos, no el primero. Saltarse el trabajo previo es la causa más común de bucles fallidos.

| Documento | Pregunta que responde | Audiencia | Responsable | Vive en |
|---|---|---|---|---|
| **MRD** — Market Requirements (Requisitos de Mercado) | *¿Deberíamos construir esto?* — tamaño de mercado, demanda, competencia, evidencia de cliente | Dirección / GTM / inversores | Marketing de producto | Slides, market research, Notion |
| **BRD** — Business Requirements (Requisitos de Negocio) | *¿Por qué lo hace el negocio y cómo medimos el éxito comercial?* — objetivos, KPIs, restricciones, presupuesto, deadlines, riesgos | Dirección / sponsors | Responsable de negocio / PM | Confluence, Google Docs |
| **PRD** — Product Requirements (Requisitos de Producto) | *¿Qué debe hacer el producto, para quién y con qué criterios de aceptación?* — features, user stories, alcance, no-objetivos | Ingeniería, diseño, QA | Product manager | Markdown spec → `prd.json` |

La secuencia natural es **MRD → BRD → PRD → `prd.json`**. Cada paso reduce el alcance:

- El **MRD** decide si la apuesta vale la pena.
- El **BRD** traduce esa apuesta en resultados de negocio medibles y restricciones (presupuesto, time-to-market, regulación, etc.).
- El **PRD** traduce esos resultados en comportamiento concreto del producto — personas, user stories, criterios de aceptación, dentro y fuera de alcance.
- El **`prd.json`** traduce el PRD en tareas atómicas y ejecutables por una máquina para un agente autónomo.

> Ralph no puede recuperarse de un MRD o BRD malo. Si la *cosa* está mal, ningún test verde te salvará. El bucle construirá fielmente el producto equivocado.

En equipos modernos y ágiles estos tres documentos a menudo colapsan en uno solo, pero el *pensamiento* sigue siendo necesario — solo se consolidan los artefactos.

---

## 3. Trabajo previo al PRD: la parte que nadie quiere hacer (y por la que fallan los bucles)

Esta sección es para leerla dos veces. Ralph amplifica lo que le des. Si las entradas son vagas, obtienes un producto vago, rápido y a escala.

### 3.1 Validar el problema (trabajo de nivel MRD)

Antes de cualquier JSON:

- **¿A quién le duele y cuánto?** Nombra 3–5 usuarios reales, su rol, su workaround actual y el coste del problema (tiempo, dinero, errores).
- **¿Hay un mercado o solo un pasatiempo?** Estima usuarios × frecuencia × disposición a pagar (o valor estratégico, si es una herramienta interna).
- **¿Qué existe ya?** Lista 3+ alternativas (build, buy, no hacer nada) y por qué se quedan cortas.
- **¿Qué evidencia tienes?** Entrevistas, tickets de soporte, analítica, motivos de churn. "Yo creo que a los usuarios les gustaría…" no es evidencia.

Salida: un planteamiento del problema de una página. Si no puedes escribirlo, no estás listo.

### 3.2 Plantear el caso de negocio (trabajo de nivel BRD)

- **Objetivos**: 2–4 resultados medibles ("reducir el tiempo de onboarding de 14 a 3 días", "recortar un 40% los tickets de soporte de la categoría X"). Defínelos *antes* de construir, no después. Combina métricas cuantitativas con cualitativas (p. ej., "los usuarios describen el flujo como 'sin fricción' en las entrevistas").
- **Apetito / inversión** (del Bet Template de Olivier Courtois, idea tomada de Shape Up): si tú fueras el inversor, ¿cuántos días de trabajo estarías dispuesto a gastar en *este* problema concreto antes de reevaluar? Fijar un presupuesto por adelantado obliga a priorizar con disciplina y evita que el bucle corra indefinidamente.
- **Restricciones**: presupuesto, deadlines, compliance, seguridad, headcount, dependencias de stack.
- **Pre-mortem (riesgos y asunciones)**: imagina que el proyecto ha fallado — escribe la post-mortem ahora. ¿Qué incógnitas técnicas, ambigüedades de diseño, interdependencias o tareas operativas lo mataron? Para cada una, anota la mitigación. Es muchísimo más barato que una post-mortem real.
- **Umbrales de éxito y fracaso**: ¿con qué número doblas la apuesta y con qué número lo matas? Un umbral de fracaso útil es la inversa del Sean Ellis test: *"menos del 40% de los usuarios beta estarían 'muy decepcionados' al perder esto — matar o pivotar."*
- **Stakeholders**: quién aprueba, quién debe ser informado, quién debe integrar.

### 3.3 Discovery: afina usuarios y alcance

Tres marcos que conviene aplicar antes de abrir editor alguno:

**Universal Idea Model** — rellénalo limpiamente o no estás listo:

> Un *[objeto]* para *[clase de usuarios]* que *[hace X]* con el fin de *[lograr Y]*. Los usuarios se benefician al *[ganar algo]* cuando *[situación]*.

Si algún hueco está difuso, vuelve a la fase de discovery.

**Problem Framing**:

- Entorno — ¿a quién afecta, quiénes son los stakeholders?
- Dinámica — ¿cuándo apareció esto, cómo ha evolucionado?
- Estado actual — ¿síntomas vs. causas raíz?
- Estado ideal — ¿qué aspecto tiene el éxito en términos de comportamiento concreto?

**Concepto de producto (seis dimensiones)** — contexto, usuarios y necesidades, formatos, estrategia y ejecución, monetización, preguntas abiertas.

### 3.4 Afina las personas

Sustituye "usuarios" por personas con nombre y específicas. "Madre o padre que gestiona la logística familiar desde el móvil entre reuniones" es mucho más útil que "usuario centrado en productividad". Cada persona lleva: rol, objetivos, frustraciones, contexto de uso, nivel técnico.

### 3.5 Define lo que está **fuera de alcance**

Esta es la sección más infrautilizada en los PRDs reales y la que evita que Ralph se vaya por las ramas. Cada feature que no excluyas explícitamente se convierte en alcance implícito en cuanto el agente empiece a inferir.

Para cada feature tentadora pero diferida, escribe una línea: *qué* se excluye, *por qué ahora*, *cuándo se reconsidera*.

### 3.6 Decide arquitectura y convenciones *antes* de arrancar el bucle

Ralph imita el código que ve. Lo que exista en el repo en la iteración 0 moldeará todas las iteraciones siguientes. Por tanto:

- Elige stack, versiones de framework y convenciones de lenguaje deliberadamente.
- Añade ficheros semilla: un endpoint funcional, un test pasando, una pasada de CI, la configuración de lint elegida.
- Redacta `AGENTS.md` (≤ 60 líneas) con los comandos reales de build/test/typecheck/lint. No es un changelog — es un manual operativo.
- Decide estilo de commits, naming de ramas, reglas de PR.

Esto es **upstream steering**: barato hacerlo una vez, imposible de retrofittear de forma limpia.

### 3.7 Dos plantillas de PRD que vale la pena estudiar

Dos plantillas públicas comprimen la mayor parte de la sabiduría anterior en formatos de una página y vale la pena pillarles ideas antes de escribir nada de JSON:

**Plantilla PRD de Kevin Yien (Square)** — estructura ligera en tres actos con puertas de aprobación:

1. **Problem Alignment** — Problema (1–2 frases), Enfoque a alto nivel, Narrativa (storytelling opcional), Goals, **Non-goals**. Acaba con una tabla de firmas; no se continúa hasta que los reviewers literalmente firman.
2. **Solution Alignment** — Key features (Plan of Record + Future Considerations), Key flows, **Key logic** (reglas y edge cases escritos como texto en vez de inferirse de los diseños). Acaba con una segunda tabla de firmas.
3. **Launch Plan** — Hitos clave con **criterios de salida** para cada fase (Pilot → Beta → Early Access → Launch). El criterio de salida del Beta es un Sean Ellis test disfrazado: *"al menos 10 clientes estarían decepcionados si lo retiráramos."* Más un **Operational Checklist** que cubre Analytics, Sales, Marketing, CS, PMM, Partners, Globalization, Risk y Legal.
4. **Appendix** — Changelog, Open Questions, FAQs, Impact Checklist (Permissions, Reporting, Pricing, API, Global).

Las ideas de mayor palanca: puertas de firma explícitas entre fases, criterios de salida nombrados por hito, un barrido operativo a través de equipos no-ingeniería, y una sección reservada únicamente a los non-goals.

**Bet Template de Olivier Courtois (Productverse / Comet)** — aún más ligero, todo en clave de apuestas:

- **Problem Alignment** — Problema, **Success measures** (cuantitativas + cualitativas, atadas a la métrica north-star), **Investment / appetite** (PM-como-inversor: ¿cuántos días de trabajo?).
- **Solution Alignment** — Bet (solución lean y testable), Risks & assumptions / pre-mortem, **No-gos** (fuera-de-alcance explícito).
- Bloque de notas con tres reglas que merecen un tatuaje en la pared del equipo: escribir en inglés/castellano llano sin codenames; el PM es dueño de la apuesta pero el desarrollador y el diseñador son dueños de la solución y los detalles; *"build the right thing, then build the thing right"* (construye lo correcto y, después, constrúyelo correctamente).

Las ideas de mayor palanca: cada solución es una *apuesta*, no un compromiso; la inversión pone tope al runtime del bucle; los no-gos son una sección de primera clase; "primero la cosa correcta, después hacerla bien" — Ralph no puede invertir este orden.

Para un `prd.json` no necesitas copiar ninguna de las dos plantillas tal cual, pero la tabla de firmas, los criterios de salida, el operational checklist, el apetito, el pre-mortem y los no-gos explícitos se pagan solos — escríbelos en el PRD markdown upstream y se traducirán limpiamente en `description`, `acceptanceCriteria` y valores de `effort` más estrictos en el JSON.

### 3.8 Cablea la contrapresión (backpressure)

Ralph solo se mantiene honesto si la realidad le contesta. Antes del primer bucle:

- Los tests deben ejecutarse con un solo comando y salir con código distinto de cero ante fallo.
- Typecheck y lint, igual.
- Para criterios subjetivos (tono, UX), prepara un LLM-como-juez con una rúbrica binaria pasa/no pasa.
- Asegúrate de que el agente no puede "tener éxito" borrando tests fallidos — protege los tests críticos o añade una guarda en el prompt.

Si no puedes articular "¿cómo sabe Ralph que ha fallado?" para cada tarea, esa tarea no está lista.

---

## 4. El esquema del `prd.json`

La forma exacta varía entre los forks de Ralph, pero la estructura canónica (según el `prd.json.example` de `snarktank/ralph`) es:

```json
{
  "project": "task-priority-system",
  "branchName": "feature/task-priority",
  "description": "Añadir un sistema de prioridad de tres niveles a las tareas con indicadores en UI, edición y filtrado.",
  "userStories": [
    {
      "id": "US-001",
      "title": "Añadir columna de prioridad a la tabla de tareas",
      "description": "Como backend, necesito un campo `priority` en la tabla `tasks` para que el resto de la feature pueda leerlo y escribirlo.",
      "acceptanceCriteria": [
        "La migración añade `priority` (enum: low, medium, high) a `tasks` con default 'medium'",
        "Las filas existentes se rellenan con 'medium'",
        "`bun run typecheck` pasa",
        "`bun run test:db` pasa, incluyendo un nuevo test que comprueba el valor por defecto"
      ],
      "priority": 1,
      "effort": 0,
      "deps": [],
      "passes": false,
      "notes": "No hay cambios de API en esta historia."
    },
    {
      "id": "US-002",
      "title": "Mostrar indicador de prioridad en la tarjeta de tarea",
      "description": "Como usuario que mira mi lista de tareas, quiero un punto coloreado en cada tarjeta para escanear las prioridades de un vistazo.",
      "acceptanceCriteria": [
        "La tarjeta muestra un punto: rojo=high, ámbar=medium, gris=low",
        "Existe una story de Storybook con snapshots de los tres estados",
        "Verificar en navegador con la skill dev-browser: la página de listado muestra los tres puntos correctamente"
      ],
      "priority": 2,
      "effort": 0,
      "deps": ["US-001"],
      "passes": false
    }
  ]
}
```

### Campos raíz

| Campo | Tipo | Propósito |
|---|---|---|
| `project` | string | Etiqueta legible, usada en commits y logs |
| `branchName` | string | Rama git a la que el bucle hace commit |
| `description` | string | Un párrafo con el *porqué* de este lote — se lee en cada iteración, mantenlo conciso |
| `userStories` | array | Lista ordenada de tareas atómicas |

### Campos de cada user story

| Campo | Tipo | Obligatorio | Propósito |
|---|---|---|---|
| `id` | string | sí | Identificador estable (`US-001`); nunca renumerar |
| `title` | string | sí | Una frase imperativa breve |
| `description` | string | sí | "Como *[persona]*, quiero *[acción]* para *[resultado]*" |
| `acceptanceCriteria` | string[] | sí | Afirmaciones concretas y comprobables — ver §6 |
| `priority` | number | sí | 1 = primero; los empates se rompen por orden de `id` |
| `effort` | number | recomendado | 0 = atómico, 1 = multi-archivo, 2 = arriesgado/ambiguo (dividir antes de arrancar) |
| `deps` | string[] | recomendado | IDs de historias que deben estar `passes: true` antes |
| `passes` | boolean | sí | Condición de salida del bucle; arranca en `false`, el agente lo pone a `true` |
| `notes` | string | opcional | Pistas, enlaces, gotchas — no son requisitos |

Si tu fork usa otros nombres, conserva la **forma** del contrato: id, intención, aceptación, dependencia, estado.

---

## 5. Granularidad de la tarea: la propiedad más importante

Una tarea de Ralph debe caber con holgura en **una ventana de contexto**. No es "un sprint", no es "una feature" — es una unidad de trabajo única y reiniciable.

**Tamaño correcto**:

- Añadir una columna a la BD + migración + un test.
- Añadir un dropdown de filtro a una página de listado existente.
- Cablear un nuevo endpoint que llama a un método de servicio existente.
- Reemplazar un string hardcodeado por un valor de configuración en ficheros conocidos.

**Demasiado grande** (dividir ya):

- "Construir el dashboard."
- "Añadir autenticación."
- "Implementar la feature de exportación."

**Heurística**: si no puedes escribir 3–6 criterios de aceptación que sean *todos* comprobables mecánicamente, la tarea es demasiado grande o demasiado vaga. Divídela.

Otro síntoma de tareas sobredimensionadas: el bucle "arregla" tests una y otra vez. Eso es el agente intentando ganar a una spec ambigua, no avanzando. Para el bucle y aprieta los criterios.

---

## 6. Escribir criterios de aceptación que generen contrapresión

Los criterios de aceptación no son aspiraciones. Son el contrato contra el que se medirán el agente y el test runner. Cada criterio debe ser uno de:

- **Mecánico** — un comando y su código de salida o salida esperada. *"`bun run typecheck` pasa."*
- **De comportamiento** — un resultado concreto y observable visible al usuario. *"Enviar el formulario vacío muestra el error inline 'El email es obligatorio' bajo el input."*
- **Verificable en navegador** — para frontend, nombra la skill/herramienta y la página. *"Verificar en navegador con la skill dev-browser: la página `/tasks` muestra 3 puntos coloreados."*
- **Negativo** — un resultado que *no* debe ocurrir. *"No se añaden nuevas dependencias a `package.json`."*

Evita: "funciona bien", "es performante", "se ve bien", "maneja edge cases". Sustituye por equivalentes medibles o muévelos a una historia de evaluación aparte.

Especifica **qué verificar, no cómo construirlo.** Las prescripciones de implementación ("usa un `useMemo` aquí, coloca el botón a 20px de la esquina superior derecha") pertenecen al diseño o a la code review, no al PRD. Sobre-especificar la implementación elimina la capacidad de Ralph de usar los patrones existentes en el repo y vuelve la spec frágil.

---

## 7. Flujo: de la idea al `prd.json`

Pipeline fiable que usan la mayoría de los forks de Ralph:

1. **Discovery** (§3) — produce un planteamiento del problema de una página, lista de personas, métricas de éxito y lista de fuera-de-alcance.
2. **PRD en markdown** — escribe `tasks/prd-<feature>.md` con secciones: Resumen, Personas, Objetivos & Métricas, Dentro de alcance, Fuera de alcance, User Stories (a nivel epic), Criterios de aceptación, Asunciones & Restricciones, Preguntas abiertas.
3. **Revisión cross-functional** — comparte el draft markdown. Diez minutos de lectura en silencio y luego se recoge lo que falta, lo que está mal o lo que no está validado. *Compartir borradores invitando a mejorarlos, no finales pidiendo aprobación.*
4. **Convertir a `prd.json`** — divide cada user story en tareas atómicas con criterios de aceptación concretos. Muchos forks incluyen una skill `/ralph` o `/prd` que hace esta conversión; uses lo que uses, *revisa cada entrada a mano*.
5. **Iteración seca de prueba** — ejecuta una iteración del bucle a mano. Lee el diff, el commit, la salida de tests. Ajusta `AGENTS.md` y el prompt antes de dejarlo correr sin supervisión.
6. **Lanza el bucle** — observa las primeras 3–5 iteraciones en vivo. Después sal del bucle y déjalo trabajar.

---

## 8. Modos de fallo comunes (y cómo verlos en el JSON)

| Síntoma en el bucle | Causa probable en `prd.json` | Solución |
|---|---|---|
| El agente edita y reedita el mismo fichero | Dos historias se solapan o contradicen | Fusiónalas o secuéncialas con `deps` |
| Se borran o saltan tests | Criterio de aceptación es "tests pasan" sin alcance | Nombra los tests/ficheros concretos; añade un criterio "no se borran tests" |
| El bucle gira y nunca converge | Historias demasiado grandes | Divide hasta que cada una sea `effort: 0` |
| La implementación se aleja de la intención | La descripción es un título de feature, no una user story | Reescribe como "Como… quiero… para…" |
| Aparecen features fuera de alcance | Falta sección `nonGoals` / fuera de alcance en `description` | Añade exclusiones explícitas a `description` |
| El agente inventa personas o métricas | El PRD upstream era vago | Vuelve al §3, no parchees en el JSON |
| "Hecho" pero el producto está mal | Las métricas de éxito no se cablean a los criterios | Liga al menos un criterio por epic a un resultado de negocio medible |

---

## 9. Señales de calidad — ¿está listo este `prd.json`?

Antes de arrancar el bucle, el archivo debe pasar todas estas pruebas:

1. **Un ingeniero puede estimar cada historia** sin hacer preguntas.
2. **Un diseñador puede prototipar cada historia de UI** solo a partir de la descripción.
3. **Cada criterio de aceptación es comprobable mecánicamente o visualmente.**
4. **La lista de fuera de alcance no sorprende a nadie** del equipo.
5. **Ninguna historia tiene `effort: 2`** — todo lo arriesgado se divide, se hace spike o se mueve a otra fase.
6. **`AGENTS.md` lista los comandos exactos** referenciados en los criterios de aceptación.
7. **La primera historia es entregable de forma independiente** si el bucle se mata tras una iteración.

Si alguna falla, no estás listo para arrancar el bucle. Iterar sobre la spec es mucho más barato que iterar sobre código malo.

---

## 10. El PRD es un documento vivo

Ralph corre durante horas o días. La realidad cambia:

- Una user story resulta inviable — márcala `passes: true` con un `notes` explicando por qué, o elimínala y añade una sustituta.
- El descubrimiento durante el build revela un prerequisito faltante — añade una historia nueva y reordena `priority`.
- La contrapresión señala un fallo recurrente — añade una guarda global a `description` en vez de repetirla en cada historia.
- Los planes se quedan obsoletos — regenéralos. El coste de una iteración de planning es pequeño comparado con dejar a Ralph dando vueltas.

Trata el `prd.json` como código fuente: commits pequeños, mensajes claros y nunca lo edites mientras el bucle corre, salvo que estés guiándolo deliberadamente. Mantén un **changelog** en la cabecera del PRD markdown upstream — fecha, cambio, quién decidió — para que la spec sea auditable. Y graba a fuego el mantra: *build the right thing, then build the thing right.* El bucle es muy bueno en lo segundo; el changelog es tu evidencia de que sigues haciendo lo primero.

---

## 11. Checklist mínimo antes de arrancar

Antes de pulsar Go en el bucle:

- [ ] Planteamiento del problema de una página validado con ≥3 usuarios reales
- [ ] Objetivos y umbrales de fracaso por escrito
- [ ] Universal Idea Model completamente relleno
- [ ] Personas con nombre (no "usuarios")
- [ ] Lista explícita de fuera de alcance
- [ ] Stack, convenciones y ficheros semilla en su sitio
- [ ] `AGENTS.md` con comandos reales de build/test/lint
- [ ] Contrapresión (tests, typecheck, lint) en verde sobre `main`
- [ ] PRD en markdown revisado por ingeniería y diseño
- [ ] `prd.json` con `effort: 0` en cada historia, criterios de aceptación reales y `deps` declaradas
- [ ] Una iteración manual ejecutada y revisada diff a diff
- [ ] Entorno aislado (sin credenciales ni claves SSH expuestas)
- [ ] Firmas registradas de ingeniería + diseño + (cuando aplique) PMM, soporte, legal, seguridad
- [ ] Barrido operativo hecho: tracking de analítica, contenido de soporte, GTM, partners, globalización, riesgo/legal — marcados o N/A, no en silencio
- [ ] Apetito acordado: máximo de días de trabajo antes de pausar el bucle para revisión humana
- [ ] El documento está en lenguaje llano — sin codenames ni jerga interna que un agente recién arrancado tendría que adivinar

Cuando los dieciséis estén marcados, arranca el bucle y sal de él.

---

## Fuentes y lecturas adicionales

- [Ralph: bucle de agente IA autónomo hasta completar todos los items del PRD (snarktank/ralph)](https://github.com/snarktank/ralph)
- [How to Ralph Wiggum — Geoffrey Huntley](https://github.com/ghuntley/how-to-ralph-wiggum)
- [Inventing the Ralph Wiggum Loop — Dev Interrupted](https://devinterrupted.substack.com/p/inventing-the-ralph-wiggum-loop-creator)
- [The Ralph Loop: When Your PRD Becomes the Steering Wheel — Valentin Nagacevschi](https://medium.com/@ValentinNagacevschi/the-ralph-loop-when-your-prd-becomes-the-steering-wheel-5abf6b1345c0)
- [Ralph — Ry Walker Research](https://rywalker.com/research/ralph)
- [Ralph Zero — orquestador sobre Ralph (davidkimai/ralph-zero)](https://github.com/davidkimai/ralph-zero)
- [ralph-claude-code (frankbria)](https://github.com/frankbria/ralph-claude-code)
- [ralph-copilot (giocaizzi)](https://github.com/giocaizzi/ralph-copilot)
- [PRD Writing Best Practices — Ainna](https://ainna.ai/resources/faq/prd-guide-faq)
- [Figma's approach to Product Requirement Docs — Yuhki Yamashita en Coda](https://coda.io/@yuhki/figmas-approach-to-product-requirement-docs/prd-name-of-project-1)
- [PRD Template — Kevin Yien (Square)](https://docs.google.com/document/d/1mEMDcHmtQ6twzNlpvF-9maNlAcezpWDtCnyIqWkODZs/edit)
- [Bet Template — Olivier Courtois (Productverse / Comet)](https://docs.google.com/document/d/1QI7QX0ARPUeYklOKouEpeEr5AcnkUdcr6tkm1n8dV_A/edit)
- [Understanding PRD, BRD, MRD and SRD — Findernest](https://www.findernest.com/en/blog/understanding-prd-brd-mrd-and-srd-a-quick-guide)
- [BRD vs. MRD — Blackblot](https://www.blackblot.com/brd-versus-mrd)
- [Breaking Down BRD, PRD, SRD, and MRD — Brucira](https://blog.brucira.com/breaking-down-brd-prd-srd-and-mrd/)
- [What is a Product Requirements Document — Airtable](https://www.airtable.com/articles/product-requirements-document)
- [Product Requirements Document: Templates and Examples — AltexSoft](https://www.altexsoft.com/blog/product-requirements-document/)
