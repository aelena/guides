# Desarrollo dirigido por especificación

### Una guía breve para gobernar el cambio cuando el código lo escribe un modelo

**Versión 0.3 · Borrador · agosto de 2026**

> Esta guía es una síntesis de varias fuentes, no investigación original.
> Las fuentes están al final. Donde discrepo de una fuente, lo digo.

---

## Para qué sirve esta guía

Hoy puedes describir una funcionalidad en una frase y obtener código que
funciona en segundos. Esa capacidad es real y no se va a ir. Lo que no te da es
una manera de responder, seis semanas después, por qué el sistema se comporta
como se comporta, cuáles de esos comportamientos acordó alguien de verdad, y qué
te va a avisar si el siguiente cambio rompe uno de ellos.

Esta guía trata de cerrar ese hueco sin renunciar a la velocidad. Es corta a
propósito. Si quieres el tratamiento completo, las fuentes del final son mejores
que un resumen de ellas.

**El ejemplo que recorre el texto** es una promoción de fidelización: una campaña
que triplica el saldo de puntos de un cliente, con un tope máximo. Es
deliberadamente pequeño, para ilustrar sin que la complejidad propia del caso
tape lo que se quiere ver, y aun así va a resultar que contiene al menos seis
decisiones que nadie tomó. Sirve de ejemplo de cuánto esconden dentro incluso las
funcionalidades pequeñas: la complejidad es fractal.

---

## 1. El problema no es la conversación

Pide a un modelo, sin más, un motor de promociones o un programa de fidelización
y desde luego lo vas a tener, derivado de sabe Dios dónde, que es lo que yo llamo
IA derivativa más que generativa. Pídele después niveles y multiplicadores de
temporada y también te los da. Nada de eso está mal en sí, pero no está completo,
ni es lo mejor, ni es lo que tú o tu cliente queríais o necesitabais realmente.

El problema es que la conversación es el único sitio donde vive la intención. Y
la conversación es imprecisa, ambigua, tiene una temperatura de comunicación baja
y no es un artefacto.

El término de Karpathy para esta forma de trabajar es *vibe coding*: construir
guiado sobre todo por intercambios informales, sin una especificación que
gobierne cada cambio. Como forma de averiguar si una idea merece la pena, es
excelente. Como forma de operar algo que tiene clientes, tiene una forma de fallo
concreta y predecible.

### Los cinco síntomas

Son invisibles mientras el proyecto es pequeño. Llegan todos juntos cuando crece,
o la primera vez que sale a producción.

**El contexto se dispersa.** Las reglas acaban repartidas entre historiales de
chat, tickets, un README, un comentario junto a la máquina de café y el propio
código. Cada sesión nueva las reconstruye desde cero, y las reconstruye
ligeramente distintas.

**Los huecos se rellenan sin acuerdo.** Ante una ambigüedad, un modelo elige algo
razonable. Razonable no es lo mismo que acordado, y no es necesariamente correcto
para este negocio. El modelo puede no saberlo mejor ni saber que debería
preguntar, y el propio usuario, en caliente, tampoco va a dar la respuesta mejor
ni la más pensada.

**El cumplimiento parcial pasa desapercibido.** El agente resuelve la parte
visible de lo que se le pide y deja caer en silencio una condición secundaria.
Haber pedido algo por escrito no es lo mismo que haberlo conseguido.

**La ejecución depende de la sesión.** Un límite de peticiones, una conexión
caída o una ventana de contexto agotada interrumpen el trabajo sin dejar claro
qué terminó y por dónde se retoma.

**Que funcione no es que esté bien construido.** La seguridad, la
mantenibilidad, la auditabilidad y el comportamiento en coste no aparecen solos.
Hay que pedirlos explícitamente, y luego comprobarlos.

Y un sexto que se escapa más fácilmente que todos los anteriores: el código puede
compilar, ejecutarse y tener buen aspecto mientras no hace lo que se pretendía.
Hacer lo correcto y hacerlo correctamente son dos cosas distintas.

### Otra manera de describir la misma pérdida

El blog de ingeniería de Microsoft plantea el problema de otro modo, y el
planteamiento merece tenerse en cuenta porque localiza el daño en un sitio más
concreto que "la conversación". Llama al fenómeno **pérdida de traducción**: la
pérdida de significado a medida que una idea pasa de necesidad de negocio a
requisito, de requisito a arquitectura, de arquitectura a implementación, y de
implementación a validación. Cuatro traspasos, y en cada uno se pierde algo.

Los dos diagnósticos son compatibles y sugieren remedios distintos, y por eso los
dos sirven. Si el problema es que la intención vive solo en una conversación, el
arreglo es un artefacto. Si el problema es la pérdida en cada traspaso, el arreglo
es un único artefacto del que leen las cuatro etapas, en lugar de cuatro
documentos que se parafrasean entre sí. La segunda es la afirmación más fuerte y
la más difícil de conseguir, y es la que justifica mantener la especificación en
el repositorio y no en una wiki.

---

## 2. "Funciona" no es "cumple"

Esta distinción organiza todo lo demás, así que merece la pena ponerse pedante
con ella.

| | **Funciona** | **Cumple** |
|---|---|---|
| Responde a | ¿El programa se ejecuta? | ¿Coincide con un comportamiento acordado de antemano? |
| Se observa | Mirando la pantalla | Comparando contra requisitos y evidencia |
| Necesita | Nada escrito previamente | Un artefacto persistente |
| Deja | Una demo | Una traza reproducible |

Cuando un agente informa de que ha terminado, esa frase por sí sola no lleva casi
información. Es una afirmación sobre la primera columna. El cierre pertenece a la
segunda.

La consecuencia operativa es todo el desarrollo dirigido por especificación en una
línea: **la especificación gobierna el cambio, y no al contrario.** Cualquier
código debería poder trazarse hasta ella, y debería pasar comprobaciones
reproducibles antes de contar como terminado.

---

## 3. Dónde está el límite de verdad

Las dos secciones anteriores defienden que la estructura se paga sola. No dicen
cuándo no lo hace, y una guía que solo argumenta en una dirección es un folleto.

### La palabra se ha desplazado

Lo que acuñó Karpathy describía algo estrecho y concreto: trabajo desechable en
el que "te entregas del todo a las vibraciones" y dejas de mirar el código
directamente. Proyectos de fin de semana. Cosas que borrarías antes que
depurarlas. Usado así no es una falta de disciplina, es exactamente la cantidad
de disciplina que corresponde a lo que hay en juego.

En el uso corriente se ha ensanchado hasta significar más o menos "escribir
software con un modelo", que hoy es casi todo el software. Ese desplazamiento
vuelve circular la discusión: se defiende la práctica señalando el significado
ancho y se la critica usando el estrecho, y los dos lados tienen razón sobre
cosas distintas. Todo lo que sigue se refiere al estrecho.

Lo mismo le está pasando a la palabra del otro lado. Böckeler cuenta que oye
usar "spec" como sinónimo de "prompt detallado", que es una actividad distinta
con el mismo nombre: un prompt largo se consume una vez y se tira, y escribirlo
no crea ningún artefacto con el que alguien pueda discrepar más adelante. Si
"especificación" acaba significando "un prompt que me tomé con calma", la
distinción de la que trata esta guía se disuelve en una preferencia de estilo.

### Qué se degrada, y en qué orden

La afirmación interesante no es que la calidad baje. Es que las pérdidas llegan
en un orden fijo, y que el código sigue funcionando a través de todas ellas, así
que la señal que te diría que pares no llega nunca.

1. **Pierdes el por qué.** El comportamiento está y la razón no. Nadie se da
   cuenta, porque todavía nadie pregunta.
2. **Pierdes el saber si sigue funcionando.** Hay tests, y se escribieron para
   estar de acuerdo con lo que el código ya hacía, así que no pueden fallar en la
   dirección que importa. Verde significa que el código no ha cambiado, no que
   sea correcto.
3. **Pierdes la capacidad de cambiarlo.** Ante una petición, nadie sabe cuáles de
   los comportamientos actuales se acordaron y cuáles fueron accidentes, así que
   cada cambio o es demasiado timorato o rompe algo que nadie sabía que sostenía
   el edificio.

Vuelve al ejemplo. Una frase sobre triplicar un saldo de puntos produjo seis
decisiones que nadie tomó. Eso es una funcionalidad. Diez funcionalidades después
hay sesenta, sin registro de cuál es cuál, y un sistema cuyo comportamiento es la
suma de sesenta monedas al aire que cayeron todas mientras alguien miraba la
pantalla y veía que funcionaba.

El coste no solo se aplaza, se transfiere. Quien gana la velocidad no suele ser
quien la paga, y la factura llega a otra mesa, meses después y con prisa. Es una
observación contable más que moral, y es la razón de que la práctica siga
extendiéndose: en el momento de la decisión es gratis de verdad.

### La zona peligrosa es la de en medio

Ninguno de los dos extremos da muchos problemas. Un script desechable improvisado
en diez minutos está bien. Un flujo de pagos regulado con especificación y puerta
de control está bien. El daño le ocurre al prototipo que deja de ser un prototipo
sin que se anuncie.

Nadie decide promocionarlo. Simplemente deja de borrarse: una demo sale bien, un
compañero empieza a depender de él, una integración apunta ahí, y en ningún
momento se reúne nadie a decidir si eso ya necesita una especificación. Cuando la
pregunta se hace evidente, las seis decisiones por funcionalidad ya están
sosteniendo el edificio y sin documentar, y escribirlas es arqueología en vez de
autoría.

Si hay una sola recomendación operativa en esta guía, es esta: decide en voz alta,
una vez, que una cosa ha cruzado la línea. El cruce es barato de marcar y caro de
reconstruir.

### La prueba

No cuánto va a vivir el código, ni lo importante que es. Las dos son conjeturas
que la gente falla en la dirección optimista.

> **¿Va a tener que cambiar esto alguien que no lo escribió?**

Eso te incluye a ti en tres meses, que es una persona distinta con el mismo
nombre. Si la respuesta es genuinamente no, improvisa y disfruta. En el momento en
que la respuesta es sí, los artefactos cuestan menos que la arqueología, y cuestan
menos cuanto antes existan.

### Qué cuesta la estructura, honestamente

El desarrollo dirigido por especificación no es gratis, y el argumento a su favor
es más débil cuando se calla el precio.

- **Un paso antes del código.** Cada cambio empieza en un sitio que no es el
  editor. Para cambios pequeños esa sobrecarga es una fracción real del trabajo.
- **Artefactos que se podrirán si nadie los mantiene.** Una especificación que nadie
  actualiza es peor que ninguna, porque durante un tiempo se la cree la gente.
- **Tokens y tiempo.** Las plantillas, los planes y las revisiones consumen
  ambos, y en un cambio pequeño la proporción no favorece.
- **Un riesgo real de ceremonia.** El proceso tiene la costumbre de convertirse en
  su propia justificación, y en cuanto lo hace consume esfuerzo produciendo
  documentos en lugar de decisiones.
- **Compromiso prematuro.** Este es el que menos se admite. Cuando todavía no
  sabes lo que quieres, escribir primero una especificación puede empeorar el
  razonamiento en vez de mejorarlo: viste una conjetura de decisión y todo lo que
  va detrás la hereda. La exploración es donde el vibe coding no es un
  compromiso sino la herramienta correcta, y pretender lo contrario es como los
  equipos acaban especificando cosas que deberían haber tirado.

### Cómo falla cuando lo haces

Los costes son lo que pagas. Lo que viene ahora son las formas en que la práctica
sale mal mientras parece salir bien, y conviene leerlas como una lista de cosas a
vigilar y no como razones para no empezar. El informe de Piskala cataloga cinco, y
coinciden con lo que cuenta quien lo practica.

**Sobreespecificación.** La especificación acumula tanto detalle que se convierte
en pseudocódigo. La prueba es tosca y útil: *si tu especificación se lee como
código, te has pasado.* Has restringido la implementación sin decidir nada
adicional, y has perdido la única propiedad que hacía que el documento mereciera
la pena.

**Putrefacción de la especificación.** El fallo propio del modo anclado. El código
se mueve, la especificación no, y durante un tiempo la gente todavía se la cree.
La única respuesta fiable es mecánica: algo tiene que fallar cuando las dos
divergen, para que la deriva sea dolorosa en vez de silenciosa.

**La especificación como burocracia.** El documento se convierte en un formulario
que rellenar en vez de una herramienta para pensar. En cuanto eso pasa, la gente o
lo torea o lo deja discretamente, y las dos cosas parecen cumplimiento desde
lejos.

**Complejidad de herramientas.** Los equipos se ahogan en planes generados, listas
de tareas y documentos intermedios. Böckeler, después de recorrer tres de estos
kits a mano, lo dijo sin adornos: *"prefiero revisar código que todos estos
ficheros markdown."* No es pereza. La capacidad de revisión es finita, y un
proceso que la gasta en artefactos deja menos para lo que se pone en producción.

**Falsa confianza.** El más sutil, y el que conecta con el argumento de dos
secciones más adelante: un test de especificación en verde garantiza que el
código coincide con la especificación. No dice nada sobre si la especificación era
correcta. *Si la especificación está mal, el código implementará fielmente lo que
está mal*, y lo hará con la build en verde y una matriz de trazabilidad.

La posición de esta guía no es que la estructura gane siempre. Es que el punto de
cruce llega antes de lo que parece, que llega sin anunciarse, y que de cualquiera
de los cinco fallos de arriba se sale más fácilmente que de la arqueología que
estás evitando.

---

## 4. Contexto, procedimiento y automatización no son especificaciones

La mayoría de los equipos recurren a tres mecanismos antes de recurrir a las
especificaciones, y los tres merecen tenerse. Ninguno de ellos es una
especificación, y confundirlos es la manera más habitual de sentirse gobernado
sin estarlo.

### El fichero de proyecto

Un fichero markdown en la raíz del repositorio que hace de memoria del proyecto:
convenciones, estructura, reglas, prohibiciones, los comandos que importan.
`CLAUDE.md`, `AGENTS.md`, `.cursorrules`, el nombre varía.

Funciona mejor cuando contiene reglas cortas, locales y accionables. Funciona mal
como almacén de todo, porque uno grande infla el contexto, acumula
contradicciones y deja de estar claro qué artefacto tiene autoridad.

*Responde a:* ¿quién soy yo en este repositorio?
*No responde a:* cómo se supone que se comporta el producto.

### Las skills

Una forma empaquetada de hacer una clase de tarea: instrucciones, plantillas,
ejemplos. Lo que aportan es portabilidad entre proyectos. Una skill se selecciona
por significado, así que su descripción es parte de su diseño: "ayuda con
programación" no le dice al agente nada sobre cuándo recurrir a ella.

*Responde a:* ¿qué sé hacer en cualquier sitio?
*No responde a:* si el resultado satisface una regla de negocio.

### Los hooks

Un comando que el entorno ejecuta por su cuenta cuando llega un momento: después
de editar un fichero, antes de un commit, al empezar la sesión. A diferencia de
una skill, un hook no lo puede saltar el agente.

*Responde a:* ¿qué ocurre pase lo que pase?
*No responde a:* si lo que se ejecuta comprueba algo que importe. Un hook puede
ejecutar los tests. No puede escribirlos, y no puede juzgar si testean lo
correcto.

### Qué no te dice ninguno de los tres

Vuelve a la promoción. Ninguno de estos ficheros dice:

- qué pasa cuando el saldo triplicado supera el tope
- cómo se calculan los puntos
- qué comportamiento sigue vigente después del cambio
- qué se decidió, y por qué
- qué evidencia demuestra, hoy, que se cumple

Contexto, procedimiento, especificación y evidencia son cuatro artefactos
distintos. Mezclarlos facilita empezar. Separarlos es lo que hace posible
gobernar algo que no deja de cambiar.

---

## 5. La regla que parece sencilla

Aquí está el ejemplo enunciado con la misma vaguedad con la que suele llegar una
petición real.

> Cuando un cliente canjee un vale de Puntos Triples, triplica su saldo de
> puntos, sin pasar del máximo de la cuenta.

Cada cláusula está clara. Juntas obligan a decisiones que la frase no contiene.

- ¿Triplica el saldo, o solo los puntos ganados en el periodo actual?
- ¿Qué pasa cuando el resultado supera el máximo?
- Si se canjean dos vales en el mismo lote, ¿el tope se aplica una vez o dos?
- ¿Qué saldo lee el multiplicador, el de antes o el de después de otras
  acumulaciones pendientes?
- ¿En qué orden se resuelven los canjes simultáneos?
- ¿Reejecutar el mismo lote produce el mismo saldo final?

Un modelo al que se le pida implementar esto va a responder a las seis. No tiene
más remedio, para poder emitir código. Las responderá en silencio, de forma
razonable, y sin decirte qué respuestas eran tuyas y cuáles suyas.

Ese es el hueco que rellenan las especificaciones. No "documentación". La
distinción entre lo que se pidió y lo que se dio por supuesto.

### Hacer que el modelo diga lo que no sabe

El mecanismo más directo para esto viene de Spec Kit, de GitHub, y es casi
vergonzosamente simple. La plantilla de especificación le indica al modelo que
escriba `[NEEDS CLARIFICATION: la pregunta concreta]` donde la petición no
determine una respuesta, y le prohíbe rellenar el hueco: *"no adivines. Si el
prompt no especifica algo, márcalo."*

Funciona porque invierte un incentivo. Un modelo al que se le pide una
especificación producirá, si no se le dice otra cosa, una que parece completa, porque completo es el
aspecto que tienen las especificaciones, y un documento sin agujeros se lee como
trabajo terminado. Si en cambio se le dice que marque los huecos, produce un
documento en el que los agujeros son la parte útil: esas seis preguntas de arriba,
por escrito, antes de que nadie se haya comprometido a una respuesta.

El límite merece enunciarse, porque esto es fácil de adoptar y fácil de volver
decorativo. Un marcador solo ayuda si algo se niega a continuar mientras quede
uno. Spec Kit pone *"no quedan marcadores [NEEDS CLARIFICATION]"* en una lista de
comprobación, y una lista de comprobación es un recordatorio. Si tu proceso trata
una especificación marcada como lista para construir sobre ella, has añadido una
sintaxis para registrar incertidumbre, no un mecanismo para resolverla.

### Las reglas estables, una vez que alguien decide

| ID | Regla |
|---|---|
| FR-001 | Canjear un vale de Puntos Triples deja el saldo en `min(3 × n, MAX_BALANCE)` |
| FR-002 | `MAX_BALANCE` no se supera nunca |
| FR-003 | Cada vale se consume una sola vez, incluso dentro de un mismo lote |
| FR-004 | El mismo lote y el mismo saldo de partida producen el mismo saldo final |
| FR-005 | El tope se aplica después de todas las acumulaciones del lote, no antes |
| ADR-001 | Los canjes simultáneos se ordenan por `(timestamp, account_id, token_id)` para que los resultados sean reproducibles |

Seis reglas y una decisión registrada, a partir de una frase. Esa proporción es
normal, y es el argumento para escribirlas en vez de descubrirlas en producción.

---

## 6. Esto no empezó con la IA

Merece la pena saberlo, porque cambia cómo lees las herramientas de hoy. Casi
ninguna de las ideas es nueva. Lo nuevo es la razón por la que de repente
importan.

**2004.** "Specification-Driven Development" aparece en trabajo académico de
Ostroff y colegas, combinando desarrollo dirigido por tests con diseño por
contrato. La motivación era la misma que ahora: los tests demuestran que pasan
casos concretos; los contratos enuncian lo que debe cumplirse en general.

**2009.** EARS, Easy Approach to Requirements Syntax, sale de trabajo hecho en
Rolls-Royce. Es un conjunto pequeño de patrones de frase que restringen cómo se
puede redactar un requisito, para reducir la ambigüedad. No eliminarla, reducirla.
Esa modestia es característica del buen trabajo en esta área.

**2021.** Un estándar interno de APIs que escribí como responsable de
arquitectura en una multinacional enuncia la posición sin nada del vocabulario
actual:

> Be API-First. Define your API properly before start implementation. The API
> first principle is an extension of contract-first principle. Therefore,
> development of an API MUST always start with API design without any upfront
> coding activities. **The design of the API is the source of truth, not the
> implementation.** The contract represents the agreement between API
> stakeholder, implementers, and consumers.

Eso es desarrollo anclado en la especificación, obligatorio en un estándar
corporativo, cuatro años antes de que nadie lo llamara desarrollo dirigido por
especificación. Está en la cronología por dos razones. La primera es que una
afirmación sobre lo viejas que son estas ideas es más fuerte con una fuente
primaria fechada que con una cita prestada. La segunda es más útil: el estándar se
adoptó, y lo que lo hizo adoptable no tenía nada que ver con la idea. Tenía número
de documento, historial de revisiones, propietarios con nombre, un apartado de
cumplimiento y una vía para las excepciones. La idea era la parte fácil.

**2025.** "The New Code", de Sean Grove, sostiene que las especificaciones, y no
el código, son el artefacto en el que merece la pena invertir cuando generar es
barato.

**2025.** Birgitta Böckeler, escribiendo en el sitio de Martin Fowler, separa la
práctica actual en tres posiciones en vez de una: spec-first, spec-anchored y
spec-as-source. Esa distinción es lo más útil de la literatura actual y la
sección 7 se construye sobre ella.

**2026.** Los preprints y las herramientas proliferan. Trátalos como señales, no
como consenso.

El patrón de toda la cronología merece nombrarse, porque predice lo que viene
después. Cada una de estas cosas llegó como respuesta local a un problema local:
los contratos para una comunidad de verificación, los patrones de frase para
requisitos aeronáuticos, el API-first para equipos a los que se les rompían las
integraciones. Ninguna llegó como metodología, y las dos que se convirtieron en
metodología, el desarrollo dirigido por modelos y en cierta medida lo ágil, son
las dos que hoy se describen como fracasadas. No es casualidad, y es el argumento
más fuerte para adoptar los mecanismos de esta guía de uno en uno, contra un
problema que sepas nombrar, y no como programa.

Por debajo, el desarrollo dirigido por especificación es un paquete de prácticas
más antiguas que responden a tres preguntas:

| Pregunta | Prácticas |
|---|---|
| ¿Qué debería hacer el sistema? | Requisitos, historias de usuario, EARS, ejemplos |
| ¿Cómo sabremos que lo hace? | TDD, BDD, contratos, testing basado en propiedades |
| ¿Por qué se construyó así? | Registros de decisiones de arquitectura |

En un flujo de trabajo con agentes este vocabulario adquiere una segunda función.
Se convierte en un sistema de contención: acota lo que el agente tiene permitido
decidir por su cuenta.

---

### El precedente que debería ponerte nervioso

Un paralelismo histórico es más afilado que los demás, y es una advertencia y no
un consuelo. El desarrollo dirigido por modelos, en la década de 2000, intentó
exactamente esto: modelos formales como artefacto principal, y código generado a
partir de ellos. Böckeler, que trabajó en eso al principio de su carrera, hace la
autopsia en una línea. Fracasó porque ocupaba *"un nivel de abstracción incómodo
y no crea más que sobrecarga y restricciones."*

La lectura optimista es que los modelos de lenguaje eliminan justo lo que lo mató:
ya no necesitas una sintaxis rígida y parseable, ni un generador que alguien tenga
que mantener, y el lenguaje natural se sitúa en el nivel de abstracción que
quieras. Es verdad, y es la razón de que la idea haya vuelto.

La lectura pesimista es la que conviene no perder de vista. Lo que el desarrollo
dirigido por modelos también tenía era soporte de herramientas: un modelo era
comprobable por un programa en validez, completitud y consistencia interna,
porque no había otra manera. Las especificaciones en lenguaje natural no tienen
nada de eso. La advertencia de Böckeler es que spec-as-source podría llegar con
*"las desventajas de MDD y de los LLM a la vez: inflexibilidad y no
determinismo"*, lo que sería un mínimo genuinamente nuevo: la rigidez del código
generado más la impredecibilidad de lo que lo genera.

No es una predicción. Es el modo de fallo que hay que vigilar, y la razón de que
las precondiciones de la sección siguiente estén escritas como precondiciones y
no como consejos.

---

## 7. El espectro: quién edita qué

Esto no es un modelo de madurez y no tienes que escalarlo. Es una manera de
hacerle una sola pregunta a tu propio proyecto: **si la especificación y el
código no coinciden, ¿cuál de los dos está mal?**

### spec-first

La especificación se escribe primero, para pensar con más claridad. En cuanto
existe código, lo que se edita es el código.

- **En caso de conflicto:** gana el código, que es lo que se mantiene.
- **Cómo aparece la deriva:** la especificación envejece en silencio.
- **Uso honesto:** herramienta para pensar, revisión de diseño, incorporación de
  gente nueva.

La mayoría de los equipos que dicen hacer desarrollo dirigido por especificación
están aquí. No tiene nada de malo, siempre que nadie finja que el documento es
normativo.

### spec-anchored

La especificación sigue siendo normativa. Un cambio empieza ahí, y después el
código se modifica o se regenera para coincidir.

- **En caso de conflicto:** gana la especificación ratificada, y el código se
  corrige.
- **Cómo aparece la deriva:** la detectan la comparación, la revisión y los tests.
- **Coste:** cada cambio tiene un paso antes del código.

### spec-as-source

Nadie edita la salida generada. Cambiar el sistema significa cambiar la
especificación y reconstruir.

- **En caso de conflicto:** ganan la especificación y el proceso de generación.
- **Cómo aparece la deriva:** en la reconstrucción, más la detección de ediciones
  manuales.
- **Precondición:** regeneración repetible, detección de ediciones manuales, e
  integración continua que proteja el comportamiento. Sin las tres, esto es una
  aspiración, no una posición.

Lo sensato por defecto es empezar en spec-anchored y mover un único módulo a
spec-as-source solo cuando esas tres precondiciones estén de verdad en su sitio.
Mover el sistema entero de golpe es como los equipos acaban editando ficheros
generados a escondidas.

### La regla para elegir

El informe de Piskala plantea la elección con más nitidez que nada de lo que he
leído al respecto, y es la frase que hay que recordar si no sobrevive nada más de
aquí:

> **Usa el nivel mínimo de rigor de especificación que elimine la ambigüedad en
> tu contexto.**

Mínimo, y en tu contexto. Spec-first mientras un modelo hace la construcción
inicial y la ambigüedad está sobre todo en tu propia cabeza. Spec-anchored para
cualquier cosa lo bastante longeva como para que la mantenga otra persona.
Spec-as-source solo donde las herramientas de generación estén maduras y sean de
fiar, lo que para la mayoría de los equipos y para la mayor parte de esta década
significa todavía no.

Vale la pena notar que esta taxonomía llega ahora desde dos direcciones
independientes: Böckeler definió los tres niveles desde el trabajo práctico con
las herramientas, y Piskala llega a los mismos tres desde un repaso de la
práctica. Dos fuentes convergiendo en una distinción es evidencia débil de que la
distinción es real, que es más de lo que tiene casi todo el vocabulario de este
campo.

### La afirmación de que no hay hueco

El manifiesto de Spec Kit enuncia la versión maximalista de spec-as-source, y
merece citarse porque es la posición con la que discute esta guía. El hueco entre
especificación e implementación, dice, *"ha atormentado al desarrollo de software
desde sus inicios"*, y los enfoques anteriores solo intentaron estrecharlo. Ahora:
*"cuando las especificaciones y los planes de implementación generan código, no
hay hueco, solo transformación."*

La primera mitad es verdad. La segunda mueve el hueco en lugar de cerrarlo.

Lo que desaparece, cuando la generación es de verdad repetible, es la distancia
entre la especificación y el código. Lo que queda intacto es la distancia entre la
especificación y lo que alguien quería realmente. Cada una de las seis preguntas
de la sección anterior se puede responder mal en una especificación, generarse
fielmente en código, y pasar todos los tests derivados de esa misma
especificación. La consistencia interna no es corrección. Un sistema que se
regenera limpiamente a partir de una especificación equivocada es un sistema que
está equivocado más rápido y más a fondo que antes.

Esto no es un argumento contra la posición, y la posición no es una afirmación
comercial: se sigue de tomarse la generación en serio. Es un argumento sobre qué
problema resuelve la posición. Spec-as-source elimina la deriva, que es un
problema real y caro. No elimina la necesidad de que alguien tenga razón, y
concentra todo el coste de equivocarse en un único artefacto que ya no tiene nada
aguas abajo que le pueda discrepar.

Que es la razón de que el resto de esta guía trate de ratificación y de puertas de
control, y no de generación. Cuanto mejor es la generación, más se concentra el
riesgo que queda en el único sitio que nadie está comprobando.

---

## 8. La puerta de control

Una puerta no es una comprobación. Una puerta es:

> **comprobación ejecutable + política obligatoria + bloqueo efectivo**

Conviene desmontar las tres, porque la mayoría de los "ya tenemos CI" falla en
alguna de ellas.

**Ejecutable.** La ejecuta una máquina y produce un veredicto reproducible, no una
opinión. Un modelo revisando su propio diff e informando de que "parece correcto"
no es ejecutable, por útil que sea la revisión.

**Obligatoria.** Está conectada a la integración y no se puede sortear. Una
comprobación que existe pero no es requerida es una sugerencia.

**Bloqueante.** El rojo detiene el cambio. Un rojo que solo avisa es una
notificación.

Instalar un validador no crea una puerta. Una ejecución en verde en un portátil no
protege la rama principal.

### El trinquete

La imagen mental útil es un trinquete: deja que la carga avance y no deja que se
escurra hacia atrás por su cuenta.

Un test se convierte en un diente de ese trinquete cuando se cumplen cuatro cosas:

1. Expresa una regla que una persona ha ratificado.
2. Está versionado.
3. Quien implementa el cambio no puede alterar el resultado esperado sin una
   revisión aparte.
4. Se ejecuta como comprobación requerida antes de la integración.

El punto 3 es el que se salta, y es el que importa. Si el mismo agente puede
escribir la implementación y relajar el test, no hay trinquete, solo un ritual.

El trinquete protege lo que el equipo consiguió expresar. No todo lo que quería. Y
no impide el cambio: si el multiplicador de la promoción debe pasar de tres a
cuatro, abres un cambio, editas la especificación, ratificas la nueva expectativa,
y cierras la puerta detrás.

### Puertas que restringen la forma, no solo el cumplimiento

Todo lo anterior trata de verificar un cambio después de que exista. Hay un
segundo tipo de puerta, dirigido a un modo de fallo que la verificación no puede
atrapar y que es específico de trabajar con modelos: la respuesta es correcta y
cuatro veces más grande que la pregunta.

Spec Kit ejecuta tres comprobaciones antes de que empiece la implementación:

- **Simplicidad.** ¿Tres proyectos o menos? ¿Hay algo aquí que sea prepararse para
  un futuro que no ha llegado?
- **Antiabstracción.** ¿El framework se usa directamente o envuelto? ¿Una sola
  representación de cada modelo, o una paralela al lado?
- **Integración primero.** ¿Están definidos los contratos? ¿Los tests de contrato
  se escriben antes de la implementación que describen?

Ningún test falla cuando esto se incumple. Un modelo al que se le pida una
promoción de puntos producirá una interfaz, una factoría, una abstracción sobre la
base de datos y una capa de servicio, todo funcionando, todo pasando, todo
revisado por alguien que lee buscando corrección, porque para eso está la revisión.
Nada del resultado está mal excepto su tamaño, y el tamaño es la propiedad que
nadie tiene asignada comprobar.

Lo que merece copiarse no son las tres preguntas. Esas son opiniones, y las tuyas
pueden diferir con razón. Es la válvula de escape. Una puerta que no puedes
suspender es teatro; una puerta sin excepciones se sortea en un mes. Spec Kit
permite el incumplimiento y exige que se escriba, en un apartado que llama
**seguimiento de complejidad**: quien quiera el cuarto proyecto explica por qué,
en el artefacto, donde lo va a encontrar la siguiente persona. Eso convierte una
prohibición en un registro, que es el mismo intercambio que hace el trinquete, y la
razón de que los dos sobrevivan al contacto con el trabajo real.

### La separación que hace que esto funcione

| Responsabilidad | Dónde vive | Contiene |
|---|---|---|
| Autoridad | Especificaciones ratificadas y registros de decisión | Juicio humano |
| Comprobación reproducible | Build, validación de esquemas, análisis estático, tests con semillas controladas | Ningún juicio |
| Aplicación | CI, protección de ramas, permisos | Política, aplicada mecánicamente |

La propiedad más importante de este montaje: **ningún mecanismo autoriza al modelo
a ratificar su propia salida.** El agente propone, una persona ratifica, un
programa comprueba. Colapsa dos cualesquiera de esos tres en uno y las garantías se
van con ello.

La objeción a esto es lo bastante común como para merecer respuesta, y aparece en
los comentarios del artículo de Microsoft en forma casi pura: los agentes ya son
lo bastante buenos como para que los puntos de control humanos sean ceremonia. La
respuesta que se da allí es la mejor versión breve que he visto, y es una
distinción más que una defensa. La **autonomía de implementación** es cuánto del
trabajo hace el agente sin que se le pida, y debería subir a medida que las
herramientas mejoran; no hay ninguna virtud en teclear código que un modelo
teclearía mejor. La **autonomía de decisión** es quién responde por el resultado, y
no se transfiere, porque no puede: un agente no puede rendir cuentas, y un equipo
que se comporta como si pudiera no ha delegado la responsabilidad, la ha
extraviado.

Por eso la puerta no es un comentario sobre lo capaz que es el modelo. Sube la
autonomía de implementación tan lejos como te lleven tus herramientas. La puerta
existe porque alguien tiene que seguir respondiendo por el resultado.

---

## 9. Las capas adyacentes

El desarrollo dirigido por especificación se encuentra normalmente junto a otros
tres o cuatro nombres, y conviene tener claro cómo se relacionan, porque se
presentan de forma rutinaria como rivales y no lo son. Operan en capas distintas,
y la pregunta que responde cada uno es distinta.

| Capa de interés | Unidad | Pregunta que responde | Dónde vive el estado |
|---|---|---|---|
| Inferencia | La llamada individual | ¿Qué forma tiene esta invocación? | En la petición y en la decodificación |
| Contexto | La ventana | ¿Qué ve el modelo, y qué se desaloja? | En el contexto |
| Bucle | El flujo de control | ¿Cuándo paramos, reintentamos o escalamos? | En el arnés |
| El bucle Ralph | La iteración | ¿Puede ser tonto el bucle exterior si el sistema de ficheros es listo? | En disco |
| Especificación | El cambio | ¿Quién decide, y qué lo demuestra? | En artefactos ratificados |

Cuatro de esas cinco tratan de hacer que la máquina funcione mejor. Solo la última
trata de quién decide. Esa diferencia de naturaleza es la razón de que el trabajo
de especificación no compita con las otras y pueda tomar prestado de todas.

### Cada capa tiene un modo de fallo que la capa de encima no puede ver

Esta es la razón práctica para que te importen todas en vez de elegir una.

**La inferencia bien hecha** te da una respuesta estructuralmente válida y
semánticamente equivocada. Un esquema no sabe nada de tu negocio.

**El contexto bien hecho** te da un agente exhaustivamente informado que está
seguro y equivocado sobre una regla que nadie escribió.

**El bucle bien hecho** te da convergencia. Convergencia hacia algo que nadie
acordó.

**Un bucle Ralph bien hecho** deja un repositorio lleno de decisiones acumuladas y
ninguna de ellas ratificada. Es el más eficaz de los cuatro produciendo código,
que es exactamente por lo que acumula intención sin examinar más rápido que
ninguno.

**Y el trabajo de especificación sin los otros cuatro** te da un documento
precioso que es caro de ejecutar.

### Qué debería tomar de cada uno el trabajo de especificación

**De la ingeniería de inferencia**, dos cosas, y la primera es la más barata
mejora disponible en toda esta pila. La decodificación restringida o guiada por
esquema convierte un contrato validado en un contrato inexpresable. Si el paso de
propuesta exige que el modelo devuelva un objeto conforme a un esquema, validar la
respuesta y rechazar las malas está bien; hacer que las malas sean imposibles de
emitir está mejor. Mover una comprobación de *rechazada* a *no se puede decir*
elimina toda una clase de reintentos.

La segunda es el coste. Un flujo anclado en la especificación reenvía la misma
especificación ratificada en cada llamada, y los proveedores facturan los prefijos
en caché a una fracción de la tarifa normal. Pon delante las secciones invariables
y detrás las variables y la mayor parte de ese contexto es casi gratis. La
literatura sobre especificaciones suele callar sobre el coste, y es un hueco,
porque "esto es más lento y más caro" es la primera objeción que plantea
cualquiera.

**De la ingeniería de contexto**, la práctica de recuperar justo a tiempo en vez de
precargar. El instinto, cuando las especificaciones se vuelven normativas, es
darle al agente la especificación entera. La ingeniería de contexto dice que le
des los identificadores y le dejes traer lo que necesite, que es precisamente lo
que hace posible un repositorio organizado en torno a identificadores y relaciones
tipadas.

Hay además una convergencia que merece nombrarse. La ingeniería de contexto llegó
a "saca el estado de la ventana y ponlo en ficheros" porque la ventana es escasa.
El trabajo de especificación llega al mismo sitio porque la ventana no es
autoritativa. La misma práctica, dos razones independientes, que suele ser señal
de que la práctica es correcta.

Y el aislamiento en subagentes, que aparece en las herramientas de especificación
como roles con permisos de escritura distintos, está justificado por duplicado: la
ingeniería de contexto lo quiere por higiene de contexto, y el trabajo de
especificación lo quiere por separación de funciones.

**De la ingeniería de bucles**, los presupuestos y los límites de turnos, y un
patrón que merece robarse más agresivamente de lo que se roba: *un reintento solo
se concede cuando la entrada contiene una hipótesis nueva*. Si un fallo reproduce
la misma firma sin ningún cambio identificable, eso no es progreso y no debería
presentarse como progreso. Esta sola regla es la diferencia entre un bucle que
converge y un bucle que gasta dinero.

**Del bucle Ralph**, la idea que más útilmente presiona todo lo anterior. Ralph es
un bucle exterior deliberadamente poco inteligente: vuelve a ejecutar el agente
contra las mismas instrucciones, y deja que relea el estado del sistema de
ficheros cada vez. Como el estado está en disco y no en el arnés, el bucle
sobrevive al agotamiento del contexto, a un cuelgue y a una sesión perdida.

Una máquina de fases del tipo que describe la sección 14 es un bucle *listo*, y
los bucles listos guardan estado. La lectura de Ralph sugiere que las fases
deberían poder reconstruirse desde disco en vez de vivir en la memoria de un
orquestador, y que un punto de control local no es una ejecución duradera. Es una
restricción real de diseño, no una preferencia estilística.

Ralph aporta además la variable que determina si algo de esto funciona: la
granularidad de las tareas. Una obligación de un tamaño tal que ninguna iteración
individual pueda cerrarla es una obligación que se va a quedar en `pending` para
siempre, y va a parecer un problema del agente cuando es un problema de
descomposición.

### Un mecanismo, dos nombres

Si has escrito sobre bucles Ralph ya te habrás encontrado con la
*contrapresión*: los tests, las comprobaciones de tipos y los linters que empujan
contra el bucle y evitan que se desmande. La contrapresión y la puerta de la
sección 8 son el mismo mecanismo nombrado desde extremos opuestos. La mirada del
bucle nombra lo que empuja de vuelta; la mirada de la especificación nombra las
tres propiedades que hacen efectivo el empujón, y añade la asimetría que la mirada
del bucle deja implícita: quien implementa el cambio no debe poder debilitar el
oráculo.

### Una nota sobre los nombres

Trata esta tabla como capas de interés y no como cinco disciplinas establecidas.
"Ingeniería de contexto" es un término consolidado. "Ingeniería de bucles" e
"ingeniería de inferencia" no lo son, al menos no en el mismo grado, y la segunda
se usa en dos sentidos distintos: la infraestructura de servir modelos, es decir
agrupación de peticiones, gestión de caché y cuantización, y la forma de una
invocación individual, es decir decodificación restringida, muestreo y política de
reintentos. Aquí solo es relevante el segundo.

Presentar las cinco como campos con nombre propio sería afirmar demasiado.
Presentarlas como capas, cada una con su unidad de interés y su punto ciego
característico, es defendible y más útil.

La razón de que esta sección vaya antes de las herramientas es que explica qué
esperar de ellas. La mayoría de las herramientas de este espacio son fuertes en
una o dos capas y callan sobre el resto, y ningún producto cubre la capa donde
vive la autoridad, porque la autoridad no es una funcionalidad.

---

## 10. La plantilla es un prompt

Esta es la idea de las herramientas actuales que se transfiere mejor, y es fácil
que se te pase porque llega con aspecto de papeleo.

Cuando Spec Kit distribuye una plantilla de especificación, la plantilla no es un
formulario para que lo rellene una persona. Es un conjunto de instrucciones
dirigido al modelo que lo va a rellenar, y sus cláusulas están escritas para
contrarrestar cosas concretas que los modelos hacen de forma fiable.

| La cláusula | El comportamiento que contrarresta |
|---|---|
| Céntrate en qué necesitan los usuarios y por qué. Evita el cómo implementarlo: sin stack tecnológico, sin APIs, sin estructura de código | Un modelo al que se le piden requisitos está eligiendo base de datos en el segundo párrafo |
| Marca todas las ambigüedades. No adivines | Rellenar los huecos con la respuesta más plausible, en silencio |
| Una lista de comprobación de completitud al final del documento | Producir algo con aspecto de completo y no volver a leerlo nunca |
| Crea primero los contratos, luego los tests, luego el código | Escribir la implementación y después tests que estén de acuerdo con lo que haya hecho |
| Sin funcionalidades especulativas ni de "puede que haga falta" | Construir para el requisito que imagina que vas a tener después |
| Los ejemplos de código y los algoritmos largos van a un fichero de detalle aparte | Una especificación que degenera en un volcado de código ilegible |

Leído como documentación, eso es una guía de estilo. Leído como lo que es, es un
conjunto de restricciones aplicadas en el momento de la escritura en vez de en la
revisión, que es el único momento en el que son baratas.

La generalización, y la razón de que esto pertenezca a una guía y no a una
comparativa de herramientas: **los artefactos de un proceso dirigido por
especificación son el prompt.** Sus encabezados deciden sobre qué se piensa. Su
orden decide sobre qué se piensa primero. Sus prohibiciones explícitas son la única
parte de todo el proceso que opera antes de que exista un error y no después. Un
equipo que escribe sus propias plantillas está escribiendo el comportamiento de su
modelo, lo piense así o no.

### Qué pasó cuando alguien lo probó

Todo eso es la teoría. Böckeler recorrió tres de estos kits a mano y encontró que
el mecanismo se sostiene mucho menos firmemente de lo que su diseño da a entender.
Los agentes ignoraron las plantillas. En una ejecución, el propio paso de
investigación de Spec Kit identificó correctamente las clases que ya existían, y el
agente generó después unas nuevas al lado, produciendo los duplicados que la
investigación se había añadido para evitar. En otras fueron en la dirección
contraria y *"se pasaron muchísimo por seguir las instrucciones con demasiado
entusiasmo."*

Así que la plantilla es un prompt, y un prompt es una petición. Esa es la versión
honesta de esta sección. Las plantillas elevan la probabilidad del comportamiento
que quieres; no lo producen, y una ventana de contexto más grande no significa que
el modelo haya leído lo que hay dentro. El nombre que le pone Böckeler a la
sensación resultante merece tomarse prestado: un flujo de trabajo cargado de
listas de comprobación puede crear *la apariencia de rigor sin aportar ninguno*, y
la apariencia es más peligrosa que la ausencia, porque hace que la gente deje de
mirar.

Eso no vuelve inútiles a las plantillas. Las convierte en la mitad barata de una
pareja. Todo lo que ellas solo piden, una puerta tiene que exigirlo, y cualquier
cosa que no puedas expresar como puerta sigue siendo una esperanza por
enfáticamente que la formule la plantilla. Ella tiene una palabra para toda esta
clase de intervención que empeora las cosas intentando mejorarlas, y merece
sobrevivir a la traducción: *Verschlimmbesserung*.

### La versión más fuerte de la idea, y lo que cuela de contrabando

El artefacto más distintivo de Spec Kit lleva esto más allá de una plantilla. Lo
llama **constitución**: un fichero de artículos numerados contra el que se
comprueba cada especificación y cada plan. Algunos son afirmaciones fuertes sobre
cómo debería construirse el software, y merecen nombrarse, porque instalar la
herramienta las adopta.

Cada funcionalidad empieza su vida como biblioteca independiente. Cada biblioteca
expone una interfaz de línea de comandos que toma texto y devuelve texto. Los
tests se escriben y se confirman en rojo antes de que exista ninguna
implementación, algo que el documento califica de no negociable. Tres proyectos
como máximo sin justificación escrita. Usar los frameworks directamente en vez de
envolverlos. Bases de datos reales en los tests de integración, no dobles.

Vuelve a leer esa lista como lo que es: un conjunto de opiniones arquitectónicas,
sostenidas por una organización, que llegan a tu repositorio como configuración.
Varias son defendibles y un par son discutibles, y la cuestión no es cuáles. Es que
un proyecto que adopta la herramienta las hereda todas y las va a imponer en cada
funcionalidad posterior, las haya leído alguien o no.

La decisión de diseño que merece robarse en cualquier caso es que varios artículos
se dejan deliberadamente en blanco, para que el proyecto los rellene con sus
propias líneas rojas. Una constitución que llega escrita del todo es la
constitución de otro.

Así que lee las que adoptes. Las tres puertas de la sección anterior y los
artículos de arriba no son andamiaje neutral. Codifican una visión concreta sobre
estructura de proyecto, abstracción y testing, y las partes que estén equivocadas
para ti se van a aplicar en silencio todo el tiempo que nadie se dé cuenta.

---

## 11. Cómo se sirven de esto los requisitos legales

Las restricciones legales y éticas son la clase de requisito más desatendida del
software, y la que casualmente encaja mejor con esta maquinaria. Las dos mitades de
esa frase merecen argumentarse.

Nada de esto es asesoramiento jurídico, y la distinción importa más de lo que
suele importar el descargo: todo lo que sigue trata de *dónde se toma una decisión
y quién responde de ella*, que es una cuestión de ingeniería. Cuál debería ser la
regla no lo es, y todo el sentido de este montaje es que los ingenieros dejen de
responder a eso por accidente.

### El único requisito que llega ya especificado

La mayoría de los requisitos hay que extraerlos de alguien que no ha terminado de
pensar. Los legales llegan ya escritos, por otra persona, y no son negociables.
Eso debería convertirlos en la entrada más fácil que reciba nunca este proceso.

No lo son, porque llegan a la altitud equivocada. "Los datos personales serán
adecuados, pertinentes y limitados a lo necesario" es un principio, y un principio
no es algo que un test pueda suspender. El trabajo es el descenso: de un principio
que nadie discute, a una regla sobre este sistema, a una comprobación que se
ejecuta.

Para el ejemplo del texto, un motor de promociones que lee saldos de clientes:

| Nivel | Enunciado |
|---|---|
| Principio | No recojas más de lo que exige la finalidad |
| Regla para este sistema | El evaluador de promociones recibe identificador de cuenta y saldo, y ningún otro atributo del cliente |
| Comprobación | Un test de contrato sobre la entrada del evaluador, que falla si el payload gana un campo |

Solo la tercera fila sobrevive al contacto con una base de código, y solo la
primera fila es lo que te va a decir alguien en una conversación de cumplimiento.
Todo lo útil pasa en la fila de en medio, y esa fila es la que nadie escribe.

### Dónde el encaje es inusualmente bueno

El trabajo regulado necesita tres cosas que de otro modo son un ejercicio aparte y
mal recibido: un enunciado del comportamiento previsto, evidencia de que el
sistema lo hace, y un registro de quién decidió. Eso son la especificación, la
puerta de control y el registro de decisión. Un equipo que ya trabaja así produce
evidencia de cumplimiento como subproducto y no como proyecto.

Ese es el argumento práctico más fuerte de esta guía, y merece enunciarse con
cuidado, porque lo que suele pasar es lo contrario. La evidencia de cumplimiento
montada a posteriori es arqueología hecha con la fecha encima por quien esté
disponible, y su calidad lo refleja. La misma evidencia cayendo de un proceso que
iba a ejecutarse de todas formas cuesta aproximadamente nada.

### Las decisiones con peso legal que se toman en silencio

Estas son las que aparecen en una revisión de código como elecciones técnicas
corrientes, y en un incidente como otra cosa. El patrón es el mismo que el de las
seis preguntas de la sección 5: nadie se niega a decidir, alguien decide
calladamente.

- **Retención.** Una duración es una decisión de diseño con consecuencia legal, y
  suele ser un valor por defecto de configuración que alguien tecleó una vez.
- **Logs.** El olvido más fiable de todos. Los logs son datos personales, se copian
  a más sitios que la base de datos, se retienen más tiempo, y los lee más gente.
- **Base jurídica.** No es un párrafo de una política. Se corresponde con una rama
  del código, y la pregunta "bajo qué base está operando esta rama" tiene
  respuesta, la haya escrito alguien o no.
- **Transferencia internacional.** La elige una región de despliegue, en un fichero
  de Terraform, quien montara el entorno.
- **Borrado.** Un problema de sistemas distribuidos disfrazado de cumplimiento.
  Cachés, réplicas, copias de seguridad, índices de búsqueda, el almacén analítico,
  y los logs de arriba.
- **Valores por defecto de telemetría.** Donde el suelo que pone la ley y el
  interés de un producto divergen de la forma más visible, decidido por el valor
  por defecto de un booleano.

Ninguna de esas necesita un abogado para *decidirse*. Todas necesitan que alguien
se dé cuenta de que se está tomando una decisión, y que encamine las que importan
hacia quien pueda ratificarlas. Ese es todo el mecanismo: lo jurídico ratifica la
regla, la ingeniería ratifica el mecanismo que la impone, y el registro de decisión
guarda la conversación para que la siguiente persona no la reabra desde cero.

El modo de fallo tiene nombre y merece decirse sin rodeos: **decidió el
desarrollador.** No con mala intención y normalmente ni siquiera con consciencia.
Es el mismo fallo que el del tope de la promoción, con una consecuencia externa
enganchada.

### Qué hay aquí genuinamente nuevo

Una cosa de todo esto no es un problema viejo con ropa nueva.

Un modelo que escribe código toma estas decisiones a un ritmo para el que no se
diseñó ningún proceso de revisión, y las toma igual que toma todas las demás: de
forma razonable, plausible, y sin decirlo. Un valor de retención por defecto, una
línea de log con una dirección de correo, un campo añadido a un payload porque
estaba disponible. Cada una es defendible por separado y ninguna fue ratificada.

Y una categoría genuinamente nueva, que es la que hay que pensar con más cuidado:
**qué sale del edificio dentro de un prompt.** Enviar el registro de un cliente al
proveedor de un modelo es una transferencia de datos a un tercero, y la inicia una
línea de código de aplicación que parece una llamada a función. El proveedor es un
encargado del tratamiento. El contenido de la ventana de contexto son datos
comunicados. Casi ninguna herramienta de este espacio lo trata así, y casi nada del
vocabulario de cumplimiento existente se escribió pensando en esto.

El trabajo de especificación correspondiente es poco lucido y pequeño: enuncia qué
puede aparecer en un prompt, como regla, y hazlo comprobable. Un test que afirma
que el payload montado para un modelo no contiene ningún campo de una lista de
denegación es un instrumento tosco. También es la diferencia entre una política y
un control.

### Donde la ley se detiene

La ley es un suelo. Las decisiones interesantes son las que son lícitas y aun así
están mal, y las deciden los mismos valores por defecto.

Un consentimiento técnicamente obtenido y prácticamente ilegible. Un periodo de
retención puesto en el máximo que permite la ley porque el máximo era lo más
fácil. Una inferencia que el sistema tiene permitido hacer y a la que la persona se
opondría si supiera que se hace. Un patrón oscuro que sobrevive a la revisión
porque ninguna regla lo prohíbe.

Para esto no hay puerta de control, y fingir lo contrario es peor que admitirlo. Lo
que sí ofrece la maquinaria es más pequeño y real: hace la decisión visible y
atribuible. Un periodo de retención escrito en una especificación, con un nombre al
lado, es una decisión sobre la que se puede preguntar a alguien. El mismo valor
como parámetro por defecto sin registrar no es de nadie.

Que es el resumen honesto de toda esta sección. El desarrollo dirigido por
especificación no vuelve lícito ni ético un sistema. Convierte las decisiones que
determinan si lo es en cosas que existen, tienen dueño, y se pueden cuestionar
antes en vez de después.

---

## 12. Un repositorio, cuatro representaciones

Si las especificaciones van a ser normativas, necesitan vivir en algún sitio que no
sea una wiki. El montaje que aguanta son ficheros planos en el mismo repositorio
que el código, con cada cosa en exactamente un sitio.

| Representación | Pregunta | Contiene |
|---|---|---|
| Intención | ¿Por qué queremos cambiar? | La petición literal, sin resumir |
| Especificación | ¿Qué debería ocurrir? | Las reglas ratificadas en vigor, y las propuestas aisladas |
| Evidencia | ¿Qué se comprueba? | Casos de aceptación, contratos, tests |
| Implementación | ¿Qué ocurre hoy? | El código, y el registro de lo que se ejecutó |

No son cuatro niveles de verdad ordenados por autoridad. Son cuatro
representaciones del mismo proyecto, cada una respondiendo a una pregunta
distinta. Lo que las convierte en un sistema y no en cuatro carpetas es que los
identificadores te permiten recorrer la cadena:

```
INT-001 → CHG-001 → FR-001 → CP-014 → TEST-001 → src/promotions.js → RUN-042
```

Poder recorrer esa cadena en los dos sentidos es de lo que va todo esto. Hacia
delante responde a "¿está implementado y comprobado?". Hacia atrás responde a la
pregunta que se hace de verdad en los incidentes: "¿por qué hace esto, y quién lo
aprobó?"

### Dos capas en un fichero

La convención que hace que esto funcione con herramientas corrientes es
frontmatter para las máquinas, cuerpo para las personas.

```markdown
---
schema_version: 1
type: requirement
id: FR-001
status: ratified
capability: promotions
relations:
  derives_from: [INT-002]
  decided_by: [ADR-001]
  verified_by: [TEST-001, PBT-002]
---

# Vale de Puntos Triples

## FR-001 - Multiplicación del saldo

WHEN a Triple Points token is redeemed, THE SYSTEM SHALL set the
balance to min(3 × n, MAX_BALANCE).

### Ejemplos
- 2.000 puntos pasan a 6.000
- 40.000 puntos con un tope de 50.000 pasan a 50.000
```

El mismo fichero sirve a cuatro consumidores: una persona que lee el cuerpo, un
agente que monta contexto a partir de las relaciones, un validador que comprueba
que los identificadores citados existen, y Git manteniendo la regla junto con su
estado y su historia.

La prueba de si has construido esto bien: **si desinstalas la aplicación de notas,
¿sigue funcionando todo?** Los artefactos deberían ser legibles como markdown
plano, validables por un script, versionables con Git y comprobables en
integración continua. Si no lo son, has construido una wiki personal con pasos
extra.

---

## 13. Cuando los artefactos no coinciden

Van a no coincidir. La regla es que ningún artefacto gana por su formato. Gana la
decisión ratificada en vigor.

| Situación | Respuesta |
|---|---|
| El código incumple una especificación ratificada | Corrige el código. La norma acordada es la referencia |
| Un test contradice la especificación | Desconfía primero del test: puede estar protegiendo una expectativa equivocada |
| El comportamiento revela que la intención estaba mal | Abre un cambio y discútelo a la vista, no parchees en silencio |
| Lo que debe cambiar es el requisito | Una persona ratifica primero la norma nueva, y después se ajusta la evidencia |

Un ejemplo resuelto. Alguien baja el tope en el código de 50.000 a 25.000 y no
toca nada más. El test que espera 50.000 falla.

Ese fallo no resuelve nada. Informa de que dos capas han dejado de coincidir.

- Si nadie ratificó un tope nuevo, la norma en vigor sigue siendo FR-002, y lo que
  se corrige es el código.
- Si el negocio quiere de verdad 25.000, el problema está más arriba: abre un
  cambio, ratifica el nuevo FR-002, y solo entonces actualiza el test y el código.

Fíjate en lo que esto *no* exige. No exige que un humano teclee físicamente cada
fichero. Un agente puede redactar propuestas, escribir requisitos y proponer tests.
Lo que sigue siendo humano es ratificar el significado. Lo que sigue siendo
mecánico es comprobar.

---

## 14. El bucle

Juntándolo todo, un cambio pasa por fases. Son estados internos, no once
pantallas.

| Fase | Persona | Sistema | Agente |
|---|---|---|---|
| Captura | Enuncia el problema | Guarda la petición literal, abre un cambio | Todavía no participa |
| Propuesta | Corrige malas lecturas | Monta el estado actual y la política | Redacta requisitos y preguntas |
| Cobertura | Comprueba que no falta nada | Convierte requisitos en filas de matriz | Propone la descomposición |
| Clarificación | Responde a las preguntas bloqueantes | Valida esquema, identificadores y relaciones | Encuentra ambigüedades y contradicciones |
| Ratificación | Aprueba alcance y significado | Registra quién, cuándo y qué hashes | Puede explicar, no puede aprobar |
| Evidencia | Aprueba el resultado esperado | Protege las expectativas aprobadas | Propone casos y propiedades |
| Confirmar el rojo | Decide si una sorpresa cambia la lectura | Ejecuta la evidencia nueva antes de cualquier código | Ayuda a interpretar el fallo |
| Implementación | Autoriza el comienzo | Fija permisos, presupuesto y punto de control | Escribe solo en las rutas permitidas |
| Verificación | Resuelve los fallos reales | Ejecuta validadores, build y tests | Arregla, en una sesión distinta de la de revisión |
| Integración | Aprueba la fusión | Comprueba CI y aprobaciones sobre el mismo commit | Resume, no fusiona |
| Archivo | Lee el cierre | Publica el nuevo estado en vigor | Ya no participa |

Tres cosas de esa tabla trabajan más que el resto.

**Confirmar el rojo.** Ejecuta la evidencia nueva *antes* de que exista la
implementación, y exige que falle. Si pasa, para: o el comportamiento ya existía, o
el test no observa lo que dice observar, o la especificación describe mal el
sistema actual. Las tres cosas conviene saberlas antes de escribir código.

**La matriz de cobertura.** Una fila por obligación, arrastrada desde la propuesta
hasta el cierre. Una fila empieza en `pending`, que no es un error, significa que la
obligación tiene identidad y todavía no tiene evidencia. El valor está en que una
petición pequeña que contiene seis obligaciones no puede convertirse
discretamente en cuatro. La matriz no se sustituye al final por un resumen escrito
para justificar lo que haya salido.

**Cierre calculado.** Nadie declara terminado el cambio. El cierre se calcula:

```
cerrado = todas las filas requeridas verificadas
        Y ninguna fila pendiente ni bloqueada
        Y CI en verde sobre este commit exacto
        Y los hashes ratificados todavía vigentes
        Y las aprobaciones requeridas presentes
```

Fíjate en que el agente informa de lo que *cree* haber atendido, y esa afirmación
nunca pone una fila en verificada. La distinción entre una afirmación y un
veredicto es justo lo que se está diseñando.

---

## 15. Qué llevarse

Si te vas a quedar con cinco cosas.

1. **La conversación no puede ser el único sitio donde vive la intención.**
   Cualquier cosa que deba sobrevivir a una sesión tiene que ser un fichero del
   repositorio.

2. **Contexto, procedimiento, especificación y evidencia son cuatro artefactos.**
   Los ficheros de proyecto, las skills y los hooks mejoran al agente. Ninguno de
   ellos es una especificación.

3. **"Funciona" no es "cumple."** El cierre se mide contra requisitos y evidencia,
   nunca contra una afirmación.

4. **Una puerta es una comprobación ejecutable más una política obligatoria más un
   bloqueo efectivo.** Dos de tres es una notificación.

5. **El agente propone, una persona ratifica, un programa comprueba.** Ningún
   mecanismo autoriza a un modelo a ratificar su propia salida.

Y una cosa de la que desconfiar, también en esta guía: nada de esto está
demostrado. La estructura es barata de añadir y sus beneficios son sobre todo
costes evitados, que son invisibles a menos que los midas. Si un equipo añade
trazabilidad y le empeoran a la vez la tasa de defectos y el tiempo de ciclo, la
trazabilidad no se ha ganado su sitio. Merece medirse antes de creérselo.

---

## Fuentes

Están listadas para comprobarlas, no para decorar. Toda afirmación de procedencia
de la sección 6 debería verificarse contra el original antes de publicar esta guía
en ninguna parte.

- Roberto Canales Mora, *Desarrollo de Software Basado en Especificaciones: del
  vibe coding a un sistema verificable*, edición preliminar, agosto de 2026. La
  columna estructural de esta guía, y la fuente de las formulaciones de la puerta
  de control, el trinquete, la matriz de cobertura y el cierre calculado.
- J. S. Ostroff y otros, trabajo sobre desarrollo dirigido por especificación
  combinando desarrollo dirigido por tests y diseño por contrato, 2004.
- EARS, Easy Approach to Requirements Syntax, originado en trabajo hecho en
  Rolls-Royce, 2009.
- Sean Grove, "The New Code", 2025.
- Birgitta Böckeler, la serie *Exploring Gen AI* en martinfowler.com, de 2025 a
  2026, incluida la entrega sobre las herramientas. La fuente del espectro de tres
  niveles, del paralelismo con el desarrollo dirigido por modelos, de la
  observación de que los agentes ignoran las plantillas, y de
  *Verschlimmbesserung*. La fuente más escéptica de esta lista y la que hizo más
  trabajo práctico, lo que no es casualidad.
- Deepak Babu Piskala, *Spec-Driven Development: From Code to Contract in the Age
  of AI Coding Assistants*, arXiv 2602.00180, febrero de 2026. Leído completo. Un
  informe técnico y una síntesis de la práctica, con un marco de decisión, cinco
  trampas con nombre y la regla del "rigor mínimo". Conviene ser preciso sobre lo
  que no es: un informe de un solo autor sin experimento, sin conjunto de datos y
  sin medición, así que es un argumento bien organizado y no evidencia, y citarlo
  como investigación sería un error de categoría. Además, de paso, atribuye el
  artículo de martinfowler.com a Fowler en vez de a Böckeler y adopta su taxonomía
  sin nombrarla, que es la propia advertencia de esta guía sobre las citas
  heredadas ocurriendo delante de nosotros.
- Microsoft, *Spec-driven development and AI-native engineering*, blog de
  desarrolladores, 2026. La fuente de la "pérdida de traducción" y de la
  distinción entre autonomía de decisión y de implementación. Es un post de
  fabricante: sus tres casos de estudio citan resultados como que la incorporación
  a un sistema heredado baja de dos o tres semanas a unos pocos días, sin nada
  publicado que permita a nadie comprobarlo.
- Andrej Karpathy, sobre vibe coding, 2025.
- GitHub, *Spec Kit* y su manifiesto `spec-driven.md`, de 2025 a 2026. Leído
  completo; la fuente de la constitución, de las puertas previas a la
  implementación, de los marcadores de clarificación, de la idea de las plantillas
  como restricciones, y de la tesis de la "inversión de poder" con la que discute
  esta guía en la sección 7.

---

## Preguntas abiertas para la siguiente revisión

- Verificar todas las citas de arriba. Las citas heredadas son la vía por la que se
  propagan los errores, y la entrada de Piskala contiene ahora un ejemplo resuelto
  de ello.
- Carlos Azaustre tiene un texto en español sobre desarrollo dirigido por
  especificación con agentes que debería estar aquí; su sitio devolvió 403 a una
  petición automática, así que hay que leerlo a mano antes de poder citarlo o
  discutirlo.
- La guía tiene ahora tres fuentes a favor de la práctica y una que discute con
  ella. Esa proporción favorece a la práctica. Encontrar el mejor argumento
  disponible de que esto es una moda, y responderlo o concederlo.
- La comparativa de herramientas ya no está, desde esta revisión. Era la sección
  que iba a envejecer más rápido, los hallazgos prácticos de Böckeler ya habían
  empezado a contradecir partes de ella, y una guía que envejece mal en una
  sección hace que se desconfíe de todas. Lo que valía la pena de ahí, la
  constitución como ejemplo de una herramienta que llega con opiniones, se movió a
  la sección 10.
- El capítulo legal necesita que lo contradiga alguien que se dedique a esto. Está
  escrito desde el lado de la ingeniería de una conversación que tiene dos lados.
- Añadir un ejemplo resuelto de principio a fin, completo, en vez de en fragmentos.
- Considerar una sección corta sobre coste: la estructura no es gratis, y el
  argumento honesto a su favor tiene que incluir la sobrecarga en tokens y en
  tiempo. La propia comparación de Spec Kit, unas doce horas de trabajo de
  documentación contra quince minutos de comandos, es la afirmación con la que
  tendría que enfrentarse esa sección. No es obviamente falsa y no está midiendo lo
  mismo en los dos lados: los quince minutos compran artefactos que nadie ha leído
  todavía.
- La idea de la constitución merece más que un párrafo dentro de una entrada sobre
  herramientas. Si las líneas rojas de un proyecto van en un fichero, las preguntas
  son quién ratifica un cambio en él, y qué lo diferencia de una guía de estilo que
  nadie sigue.
