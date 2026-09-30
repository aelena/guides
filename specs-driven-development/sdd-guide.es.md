# Desarrollo dirigido por especificación

### Una guía breve para gobernar el cambio cuando el código lo escribe un modelo

**Versión 0.5 · Borrador · septiembre de 2026**

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

Funciona mejor cuando contiene reglas cortas, locales y que se puedan aplicar. Funciona mal
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

Dos detalles de la práctica ayudan a que el marcador sea mecanismo y no
sintaxis. El primero es de Fontoura: el estado que desbloquea la fase siguiente
vive en un fichero aparte, de una sola línea, que solo escribe una persona, y
la regla es plana: *que el fichero exista no implica aprobación*. Un documento
de diseño en disco no es luz verde; solo lo es el token de estado. Con eso, un
marcador sin resolver deja de ser una nota y pasa a ser la razón por la que el
token no cambia. El segundo es más barato todavía: antes de escribir código,
pídele al modelo que reformule las reglas con sus propias palabras. Si ha leído
mal la FR-002, te enteras ahora, a coste cero, y no tres sesiones después.

Y un dato sobre lo poco que se sabe de esto. SpecMine, el censo de la Carnegie
Mellon sobre 470.795 ficheros de especificación en GitHub, cuenta los
marcadores de clarificación y los huecos sin rellenar como rasgos de cada
documento. Es la primera vez que alguien puede medir cuántos marcadores se
resuelven antes de que exista el código y cuántos se quedan ahí. Nadie ha
publicado todavía esa cifra.

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

**2026.** Llegan las primeras mediciones, en dos direcciones. Un censo de GitHub
cuenta 470.795 ficheros de especificación en 73.030 repositorios, el 99,7 %
creados desde 2025: la práctica tiene un año. Y un estudio sobre 100.247 pull
requests no encuentra ninguno de los beneficios que anuncian los fabricantes.
La sección 19 trata de los dos.

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

Alenezi, en el modelo de referencia más formal que se ha publicado sobre esto,
describe la misma frontera con otro vocabulario, y merece tenerlo porque hace
explícita una afirmación que la sección 2 deja implícita. En el vibe coding la
aceptación es *por observación*: se ejecuta el artefacto sobre unas cuantas
entradas y se juzga lo que se ve. Con especificación la aceptación es *por
verificación*: el artefacto pertenece al conjunto de lo que un validador
determinista acepta. Y el validador tiene una propiedad que el generador no
tiene: es monótono. Endurecer cualquier comprobación estrecha lo que se acepta
sin tocar el modelo. Las mejoras de calidad se componen a través de la frontera
determinista, no a través del reentrenamiento. Eso es la sección 16 en una
frase, y es la razón de que esta guía hable tan poco de qué modelo usar.

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

## 9. Los principios de fondo

Todo lo anterior han sido mecanismos: marcadores de clarificación, trinquetes,
puertas de control, tres posiciones en un espectro. Los mecanismos caducan. Las
herramientas que los llevan dentro habrán cambiado dos veces antes de que acabe
la década, y una guía que no es más que un inventario de la práctica actual
envejece hasta convertirse en pieza de museo.

Así que merece la pena separar los mecanismos de aquello que los genera. Lo que
sigue son siete principios de los que el resto de esta guía es un caso
particular. Ninguno menciona una herramienta, y ninguno deja de ser cierto si los
modelos se vuelven el doble de buenos. Quédate con estos y pierde todas las
herramientas que se nombran aquí, y podrás reconstruir la práctica. Quédate con
todas las herramientas y pierde estos, y tendrás la apariencia de rigor de la que
las secciones anteriores no dejan de avisar.

### Uno: la intención tiene que ser un artefacto, no un acontecimiento

Una conversación es un acontecimiento. Ocurre, termina, y lo que resolvió
sobrevive solo en lo que alguien acertó a escribir después. Un artefacto
persiste, tiene una dirección, se puede citar en una discusión, y lo puede
contradecir una persona que no estaba en la sala.

*Genera:* el repositorio de la sección 13, la insistencia en que un historial de
chat no es una especificación, y la mayor parte de la sección 1.

*Lo que cuesta:* escribir las cosas, y la disciplina de hacerlo en el momento en
que se toma la decisión y no en el momento en que alguien pregunta.

### Dos: un sistema que no puede registrar incertidumbre fabricará certeza

Es la generalización de `[NEEDS CLARIFICATION]`, y no es un hecho sobre los
modelos. Cualquier proceso cuyo formato de salida no tiene una casilla para "sin
decidir" produce documentos sin partes sin decidir, porque el formato exige una
respuesta y alguien, o algo, la pone. Los modelos lo hacen rápido y visible. No
lo inventaron: un documento de requisitos sin apartado de preguntas abiertas no
ha significado nunca, en toda la historia de la práctica, que no las hubiera.

*Genera:* los marcadores de clarificación, la pregunta bloqueante de la fase de
clarificación, la fila `pending` de la matriz de cobertura.

*La prueba:* ¿puede tu artefacto decir "no lo sé", y hay algo aguas abajo que se
niegue a moverse mientras lo diga?

### Tres: la autoridad va con las decisiones ratificadas, no con los formatos

Ningún documento es normativo por dónde vive ni por cómo se llama. Es normativo
porque alguien con la potestad de decidir lo ha ratificado y la ratificación
está registrada. Por eso la sección 14 se niega a dejar que un test gane una
discusión por el hecho de ser ejecutable, y por eso una página de wiki puede ser
autoritativa mientras un fichero YAML es un rumor.

*Genera:* el paso de ratificación, los registros de decisión, las reglas de
conflicto.

*Dónde se equivocan los equipos:* instalan un formato y creen que la autoridad
ha venido con él.

### Cuatro: quien hace el trabajo no puede ser dueño del oráculo

La única propiedad estructural que separa un trinquete de un ritual. Si el
mismo actor puede producir la implementación y ajustar la cosa que la juzga, el
juicio no lleva información, y da igual que ese actor sea un modelo o una
persona con prisa un viernes.

*Genera:* el punto tres del trinquete, la tabla de separación de la sección 8,
los límites de permisos de la sección 16.

*Fíjate en lo general que es:* es la idea más vieja de la guía. La contabilidad
por partida doble, la revisión por pares y la separación de poderes son el mismo
principio, y ninguna se diseñó pensando en software.

### Cinco: el cierre se calcula, no se declara

"Terminado" es una afirmación. El cierre es un veredicto, derivado de
condiciones que un programa puede evaluar. La distinción sobrevive a cualquier
mejora de quien hace la afirmación, porque el problema nunca fue que quien
afirma sea poco fiable. Es que una afirmación y un veredicto son cosas de clases
distintas.

*Genera:* la fórmula de cierre de la sección 15, la puerta de control, confirmar
el rojo.

*El corolario que la gente se salta:* si no lo puedes calcular, no has definido
"terminado". Has descrito una sensación sobre lo terminado.

### Seis: usa el mínimo rigor que elimine la ambigüedad

La regla de Piskala, ascendida aquí a principio porque es la que impide que los
otros seis hagan metástasis. El rigor es un coste que se paga para eliminar una
ambigüedad concreta. Donde no hay ambigüedad no hay nada que comprar, y el fallo
por ceremonia de la sección 3 es lo que pasa cuando un equipo olvida el "mínimo"
y se queda con el "rigor".

*Genera:* el espectro de la sección 7, y el permiso para no hacer casi nada de
esto en la mayoría de los cambios.

*Su enemigo:* es el único principio de la lista que no se puede imponer
mecánicamente, porque una puerta que comprueba si tienes demasiadas puertas es
un chiste con coste de mantenimiento.

### Siete: los artefactos son el prompt

Todo lo que escribes lo lee la cosa que escribe el código. Los encabezados
deciden sobre qué se piensa, el orden decide sobre qué se piensa primero, y las
prohibiciones son la única parte del proceso que actúa antes de que exista el
error. La sección 11 lo desarrolla; como principio significa algo incómodo, y es
que tus plantillas son comportamiento del modelo y tus documentos de proceso son
ejecutables, tanto si los pensaste así como si no.

*Genera:* las plantillas como restricciones, la constitución, toda la sección
11.

*La trampa:* un prompt es una petición. En la sección 11 también se dice eso.

### Los principios no son todos compatibles

Una lista de principios que nunca entran en conflicto es una lista que nadie ha
usado. Dos tensiones merecen nombrarse, porque te encuentras con las dos en el
primer mes.

**Uno contra seis.** Toda decisión merece un artefacto, y la mayoría de las
decisiones no merecen el artefacto. No hay fórmula que lo resuelva, solo la
prueba de la sección 3: ¿va a tener que cambiar esto alguien que no lo escribió?

**Tres contra cinco.** La autoridad es humana y el cierre es mecánico, así que
siempre hay una franja de cosas que una persona ha ratificado y ningún programa
puede comprobar. La respuesta honesta es hacer esa franja visible en vez de
fingir que está vacía. Un requisito sin oráculo calculable no es un requisito
defectuoso, es un requisito cuya verificación es una persona, y la fila debería
decirlo en vez de quedarse en `pending` para siempre con aspecto de
automatización sin terminar.

| Principio | Mecanismo que genera | Lo que tienes sin él |
|---|---|---|
| La intención es un artefacto | El repositorio, el registro del cambio | Arqueología |
| La incertidumbre se puede representar | Marcadores de clarificación, filas `pending` | Conjeturas seguras, invisibles |
| La autoridad se ratifica, no se formatea | La ratificación, las reglas de conflicto | Gana quien editó el último |
| Quien trabaja no es dueño del oráculo | El trinquete, los límites de permisos | Una build en verde que no significa nada |
| El cierre se calcula | La fórmula de cierre, la puerta | "Terminado" como estado de ánimo |
| Rigor mínimo | El espectro | Ceremonia |
| Los artefactos son el prompt | Las plantillas, la constitución | Las opiniones de otro, impuestas en silencio |

---

## 10. Las capas adyacentes

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

La objeción de moda va en la dirección contraria: si el código entero cabe en
la ventana, ¿para qué escribir una especificación? Fontoura da la respuesta
corta, y es la buena. La longitud del contexto y la precisión del contexto son
problemas distintos. Un millón de tokens de código le dicen al modelo lo que el
sistema *es*. No le dicen nada de lo que debería *ser*: la intención, las
restricciones, lo que queda fuera a propósito. Una ventana más grande hace al
agente más informado sobre el presente y no más sabio sobre el objetivo, y le
da más superficie de la que copiar el precedente equivocado. El contexto hace
al agente consciente. La especificación lo alinea.

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

Una máquina de fases del tipo que describe la sección 15 es un bucle *listo*, y
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
característico, es defendible y más útil. La casilla de la tercera fila, el
arnés, es a la que esta guía vuelve: la sección 16 trata de construirlo.

La razón de que esta sección vaya antes de las herramientas es que explica qué
esperar de ellas. La mayoría de las herramientas de este espacio son fuertes en
una o dos capas y callan sobre el resto, y ningún producto cubre la capa donde
vive la autoridad, porque la autoridad no es una funcionalidad.

---

## 11. La plantilla es un prompt

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

Palacio le pone nombre a la categoría, y el nombre ayuda a defenderla ante quien
lee "documentación" y piensa en el Manifiesto Ágil. Hasta ahora la
documentación de un proyecto era de dos clases: informativa, para que una
persona entienda el sistema, o administrativa, para satisfacer un proceso. La
especificación que consume un agente es una tercera cosa, *documentación
operativa*. No informa a nadie sobre el software; lo produce. El segundo valor
del Manifiesto se escribió contra las dos primeras clases, y esta, en 2001, no
existía.

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

Hay además una razón medida para que una plantilla más larga no compre más
cumplimiento. El trabajo sobre la *maldición de las instrucciones*, que Palacio
recoge en su guía, midió lo que pasa cuando se apilan instrucciones verificables
en un mismo prompt: la probabilidad de cumplirlas todas se ajusta bastante bien
a la probabilidad de cumplir una sola elevada al número de instrucciones. Con
diez reglas y un noventa por ciento de fiabilidad por regla, el conjunto se
cumple una de cada tres veces. La consecuencia para las plantillas es directa:
descomponer en vez de acumular, y poner primero lo que no puede fallar. La
consecuencia para la sección 16 es la misma: la colisión de instrucciones no es
solo un problema de contradicción, es un problema de cantidad.

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

La palabra, además, ya se usa para dos cosas, y conviene saber cuál se está
oyendo. En la guía de Scrum Manager, "constitución del proyecto" es el fichero
de contexto de la sección 4: convenciones, stack, estructura, lo que en Spec Kit
sería el fichero de proyecto. En Spec Kit son artículos numerados contra los que
se comprueba cada plan. Alenezi le da a la segunda acepción su sitio exacto: en
su modelo, una especificación tiene cuatro componentes, y uno de ellos son las
*restricciones constitucionales*, reglas no negociables de seguridad, privacidad
y regulación que comprueba el analizador estático, no una persona. Esa es la
respuesta a la pregunta que quedó abierta en la revisión anterior, qué
distingue una constitución de una guía de estilo que nadie sigue: que algo la
ejecuta. Una constitución que solo lee el modelo es una guía de estilo con otro
nombre. Una que comprueba un validador es un artículo de la puerta de control.
Marri publica una reducción del 73 % en defectos de seguridad con ese montaje;
es un solo proyecto, con el mismo desarrollador en las dos condiciones, y la
sección 19 dice qué peso darle.

Así que lee las que adoptes. Las tres puertas de la sección 8 y los
artículos de arriba no son andamiaje neutral. Codifican una visión concreta sobre
estructura de proyecto, abstracción y testing, y las partes que estén equivocadas
para ti se van a aplicar en silencio todo el tiempo que nadie se dé cuenta.

---

## 12. Cómo se sirven de esto los requisitos legales

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

## 13. Un repositorio, cuatro representaciones

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

Fontoura llega a una partición parecida desde la práctica, y la coincidencia es
la parte útil. Tres capas, cada una con una vida distinta: un fichero de entrada
de menos de treinta líneas que solo enruta, un directorio de contexto duradero
que cambia cuando se toma una decisión de arquitectura, y una carpeta por
funcionalidad con los documentos del cambio y su estado. Cada capa falla sin las
otras dos. Y una regla de precedencia que la sección 14 hace suya: el contexto
duradero no sobrescribe en silencio una especificación aprobada; si chocan, el
agente para y pregunta cuál de los dos artefactos hay que actualizar.

La prueba de si has construido esto bien: **si desinstalas la aplicación de notas,
¿sigue funcionando todo?** Los artefactos deberían ser legibles como markdown
plano, validables por un script, versionables con Git y comprobables en
integración continua. Si no lo son, has construido una wiki personal con pasos
extra.

---

## 14. Cuando los artefactos no coinciden

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

Fontoura lo enuncia como regla de supervivencia del método, y merece la forma
imperativa: *nunca parchees el código y dejes atrás la especificación.* No es
solo que la especificación envejezca. Es que, si el módulo se regenera, el
parche desaparece y el error vuelve, porque la restricción vivía en tu cabeza y
no en el documento. El ejemplo que da es el que mejor enseña lo que es una
ratificación: una especificación de cobros pasó la revisión de requisitos y
llegó al diseño sin la restricción de unicidad sobre la clave de idempotencia.
El diseño era coherente y estaba mal. Lo atrapó una persona leyendo el
documento, no una comprobación, y ese es el sentido de que la ratificación de
la sección 15 sea una fase y no una casilla: es una lectura.

---

## 15. El bucle

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

La fila "verificada" necesita un formato, o vuelve a ser una afirmación con otro
nombre. El que usa Fontoura cabe en cinco líneas y es el que hay que exigir: la
afirmación que se comprueba, el comando que se ejecutó, el código de salida, un
resumen de una línea y el veredicto. Tres reglas lo mantienen honesto. El
alcance de la verificación es proporcional a la afirmación: una afirmación
estrecha ejecuta un test; "la funcionalidad está terminada" ejecuta todo. Si no
hay comando, se dice: "verificado a mano en el navegador, sin test
automatizado" es un informe honesto y "funciona" no lo es. Y ninguna fila se
cierra con evidencia de ayer: el código ha cambiado desde entonces, que es lo
que la fórmula de arriba quiere decir con "sobre este commit exacto".

---

## 16. Ingeniería del arnés

La sección 10 le dio al bucle una sola fila de una tabla y dijo que su estado
vive "en el arnés". Esta sección trata de esa casilla, porque es donde está la
mayor parte de la distancia entre una demostración y un sistema.

Primero una advertencia sobre el nombre, en el espíritu de la sección 10.
"Arnés" es uso asentado: es como la comunidad de herramientas para agentes llama
al programa que rodea al modelo, y nadie lo discute. "Ingeniería del arnés" como
disciplina con nombre no lo es, y presentarla como tal sería afirmar de más
exactamente en el sentido contra el que avisa aquella sección. Léelo como un
ámbito de trabajo y no como un campo.

> **El arnés es todo lo que decide qué ve el modelo, qué puede hacer y qué pasa
> con lo que produce.**

La afirmación que le vale una sección: **el modelo es el componente menos
controlable del sistema, y es el que todo el mundo intenta controlar primero.**
Retocar el prompt y cambiar de modelo son las dos palancas que quedan a mano, y
tienen la peor relación entre esfuerzo y varianza eliminada. Todo lo demás es
software corriente, lo que significa que se puede especificar, testear,
versionar y razonar, y casi nadie hace nada de eso con él.

### Qué contiene un arnés

| Componente | Decide | A qué se parece su ausencia |
|---|---|---|
| Montaje del contexto | Qué ve el modelo en este turno | Reglas obedecidas el martes y olvidadas el miércoles |
| Superficie de herramientas | Qué acciones existen siquiera | Soluciones ingeniosas a problemas que no sabías que estaban al alcance |
| Permisos | Dónde pueden aterrizar las escrituras | Una batería de tests que está de acuerdo con la implementación |
| Bucle de control | Continuar, reintentar, parar, escalar | Ejecuciones que terminan cuando se termina el dinero |
| Oráculos | Quién dice que ha funcionado | "Terminado" |
| Estado | Qué sobrevive a un cuelgue | Trabajo que no se puede retomar, solo reiniciar |
| Presupuesto | Qué cuesta antes de que mire una persona | La factura como primera señal |
| Registro | Qué pasó, reconstruible después | Un resultado que nadie sabe explicar |

Dos cosas sobre esa tabla. Solo una fila trata del modelo. Y todas las filas son
ingeniería corriente que, aun así, no revisa nadie en la mayoría de los equipos,
porque un arnés llega como pegamento, y el pegamento no se percibe como
componente. Un arnés es un programa. Tiene especificación o tiene comportamiento
sin documentar, y la sección 1 ya describió lo que pasa después.

### Diseñar uno desde cero

El instinto es empezar por el bucle, porque el bucle es la parte interesante. Es
el extremo equivocado. Un bucle se define por su condición de salida y su
condición de salida es un oráculo, así que un arnés diseñado empezando por el
bucle acaba en un bucle que corre hasta que el modelo dice que ha terminado.

Constrúyelo en este orden.

**1. Nombra la unidad de trabajo.** Una unidad es lo que se espera que cierre
una iteración. Acierta mal con esto y todo lo que va encima se comporta mal de
maneras que parecen problemas del modelo: una unidad demasiado grande no cierra
nunca y se queda en `pending` para siempre, una unidad demasiado pequeña gasta
todo su presupuesto en reconstruir el contexto. Es la variable de Ralph de la
sección 10, y va primero porque todas las decisiones posteriores dependen de
ella.

**2. Escribe el oráculo de una unidad.** Antes de que exista ninguna
orquestación, responde a esto: ¿qué programa, ejecutado por alguien que no se
fía de mí, decide si esta unidad está terminada? Si no hay respuesta, para. No
tienes un problema de arnés, tienes un problema de especificación, y construir
primero el arnés produce una máquina eficiente para llegar a ninguna parte en
concreto.

**3. Pon el estado en disco.** Lo que la siguiente iteración necesite saber
tiene que poder leerse del sistema de ficheros y no vivir en la memoria de un
orquestador. Es el argumento de Ralph de la sección 10 y es un requisito de
durabilidad, no una preferencia: un arnés cuyo estado vive en un proceso pierde
un día de trabajo con una conexión caída.

**4. Define la superficie de herramientas, y mantenla pequeña.** Cada
herramienta es una decisión que el modelo pasa a poder tomar. Las herramientas
no son capacidad gratis, son factor de ramificación.

**5. Fija los permisos antes de la primera ejecución, no después del primer
incidente.** Qué rutas son escribibles en qué fase. La que la gente olvida no es
producción, de esa se acuerda todo el mundo, es el oráculo, que sigue siendo
escribible hasta que alguien ha visto una batería ponerse en verde por la razón
equivocada.

**6. Ahora escribe el bucle.** Condición de entrada, condición de salida,
política de reintentos, salida por escalado. Debería ser aburrido. Si tu bucle
es interesante, parte de esa inteligencia es estado que debería estar en disco.

**7. Añade presupuestos, y después el registro.** Un límite de turnos y un
presupuesto de tokens por unidad, y un registro de solo escritura de qué se
ejecutó, sobre qué entradas, con qué veredicto. El registro es lo que hace que
un incidente tenga respuesta seis semanas después, que es lo que la sección 1
dice que se pierde primero.

La nota honesta para terminar: un arnés mínimo viable es un script de shell, un
directorio de ficheros y un comando de tests. La mayoría de los equipos que
recurren a un framework de orquestación no han escrito todavía su oráculo, y un
framework no lo aporta. Aporta reintentos, que es como un oráculo ausente se
convierte en un oráculo ausente y caro.

### Reducir errores sin cambiar el modelo

Los mismos pesos, menos defectos. Es la parte del trabajo con mejor retorno y
menos literatura. Las palancas van, más o menos, en orden de lo que compran por
lo que cuestan.

**Haz que la salida mala sea indecible.** Decodificación restringida o guiada
por esquema, de la sección 10. Mover una restricción de *rechazada* a *no se
puede emitir* elimina una clase de reintentos en vez de gestionarla. Se aplica
en cualquier sitio donde el modelo tenga que elegir de un conjunto conocido, y
los conjuntos conocidos son más frecuentes de lo que parecen: estados,
identificadores, rutas de fichero, nombres de fase.

**Reduce la superficie de decisión.** Menos herramientas, cada una más
estrecha. Una herramienta que hace lo correcto gana a una herramienta con una
opción que elige entre lo correcto y un tiro en el pie. Lo mismo vale para
cualquier configuración que el modelo pueda ver: cada opción es una oportunidad
de elegir la otra.

**Haz que los fallos instruyan.** La mayor ganancia barata al alcance de casi
todos los equipos y la que más sistemáticamente se salta. Cuando una
comprobación falla, lo siguiente que lee el modelo es tu mensaje de error, y ese
mensaje es un prompt tanto si alguien lo escribió como tal como si no. Un código
de salida 1 produce conjeturas. *"FR-002 incumplida: el saldo 60000 supera
MAX_BALANCE 50000, ver specs/FR-002.md"* produce un arreglo, porque nombra la
regla, la observación y dónde mirar. El texto de los errores es el prompt con
más tráfico del sistema y normalmente el único que nadie ha editado.

**Pon lo invariable primero y lo variable al final.** Ordenar para la caché de
prefijos del proveedor, de la sección 10, y para la relevancia al mismo tiempo.
Ahorra dinero, y convierte las reglas estables en lo que el modelo ha visto más
veces.

**Separa las sesiones que tienen que discrepar.** Una revisión hecha en la
sesión que escribió el código hereda el razonamiento que produjo el error.
Sesión distinta, y donde importe permisos distintos: el principio cuatro,
implementado con límites de proceso.

**Haz que los reintentos se ganen su sitio.** La regla de la sección 10,
reformulada como ajuste del arnés: un reintento solo se concede cuando la
entrada contiene algo nuevo. La misma firma de fallo y ninguna hipótesis nueva
significa escalar, no repetir. Sin esta regla, un bucle con presupuesto es una
manera más lenta de gastarlo.

**Punto de control en cada frontera de unidad.** Un fallo debería costar una
unidad de trabajo y no una sesión. Estado en disco otra vez, visto desde el lado
del coste.

**Toma determinismo allí donde lo haya.** No del modelo, de todo lo que lo
rodea: dependencias fijadas, relojes fijos, generadores con semilla, fixtures
grabadas. El objetivo no es la generación reproducible, es el fallo atribuible.
Si un arnés es no determinista en seis sitios, ningún fallo se puede localizar
en el único sitio que es no determinista a propósito.

Ahora el contrapeso, porque esto se lee demasiado fácilmente como la promesa de
que el andamiaje sustituye a la capacidad. No lo hace. La prueba de si has
tocado techo es: **¿una persona competente, con este contexto y estas
herramientas, lo conseguiría?** Si sí y el agente falla, es un problema de arnés
y se aplican las palancas de arriba. Si no, tienes un problema de descomposición
disfrazado de problema de arnés, y más andamiaje compra un fallo más caro.

Hay además una manera de que un arnés empeore las cosas activamente, y tiene una
forma reconocible: la **colisión de instrucciones.** Un fichero de proyecto dice
una cosa, una skill dice una segunda, una plantilla inyectada dice una tercera, y
ninguno de los tres autores sabe que existen los otros dos. El síntoma es un
comportamiento que varía entre sesiones sin razón visible, y el reflejo, añadir
una cuarta instrucción que le diga al modelo cómo priorizar las tres primeras,
es la *Verschlimmbesserung* de Böckeler llegando a su hora. El arreglo es
aburrido: una autoridad por pregunta, y una lectura periódica de todo lo que se
le envía de verdad al modelo, que es algo que llamativamente pocos equipos han
mirado alguna vez entero.

### Validar el trabajo de un agente automáticamente

"Automáticamente" carga con mucho peso en esa pregunta, así que conviene
partirla. La comprobación automática del *cumplimiento de algo ya acordado* es
en gran medida un problema de ingeniería resuelto, y el resto de esta sección
trata de hacerlo bien. La comprobación automática de *si lo acordado era
correcto* no está resuelta, no está cerca, y cualquier herramienta que afirme lo
contrario ha movido el juicio a algún sitio donde no puedes verlo.

Un oráculo es lo que produzca el veredicto. Se diferencian en lo que pueden
atrapar.

| Oráculo | El veredicto que da | Su punto ciego |
|---|---|---|
| Esquema o contrato | La forma es legal | No dice nada del significado |
| Ejemplo ratificado | Este caso con nombre coincide con una respuesta acordada | Solo los casos que alguien escribió |
| Propiedad | Una regla se cumplió sobre entradas generadas | Fácil de enunciar de forma vacía, difícil de enunciar bien |
| Metamórfico | Dos ejecuciones relacionadas se relacionan como deben | Necesita una relación que sepas nombrar |
| Diferencial | Lo nuevo coincide con una referencia | Hereda los errores de la referencia |
| Repetición | Las mismas entradas produjeron las mismas salidas | Consistencia no es corrección |
| Tipos y análisis estático | Una clase de defecto está ausente | Ausencia de una clase, no presencia de intención |
| Un modelo como juez | Una opinión rápida y barata | No es ejecutable en el sentido de la sección 8 |

La última fila es la tentadora y la que más se usa mal. Un modelo revisando un
diff es útil de verdad: buen triaje, atrapa cosas que la gente se salta al leer
por encima, cuesta casi nada. No es una puerta. No es reproducible, se le puede
convencer de que cambie de posición desde la cosa misma que está revisando, y
una comprobación que devuelve un veredicto distinto el martes es una
notificación con pasos extra. Úsalo para decidir qué mira una persona. No lo
uses para decidir qué se fusiona.

Hay una versión más fuerte del principio cuatro que la tabla no recoge y que
merece conocerse aunque casi nadie pueda pagarla. Ryan describe el montaje de
StrongDM, que desde 2024 produce software con tres ingenieros y sin nadie que
escriba ni revise código: los escenarios de evaluación viven *fuera* del
repositorio y el agente no los ve nunca. No es que no pueda editar el oráculo;
es que no sabe qué contiene, como el conjunto de validación que un modelo no ha
visto durante el entrenamiento. Un agente que puede leer los tests puede, por
presión de optimización y sin mala intención, escribir código que los pasa sin
hacer lo que pretendían. Con el oráculo oculto esa vía no existe. El segundo
componente es lo que hace posible el primero: réplicas de comportamiento de
cada servicio externo, para que el agente desarrolle contra entornos simulados y
no toque datos reales. Para la mayoría de los equipos eso es una dirección, no
una receta. La receta mínima sigue siendo la regla anterior: que el oráculo no
sea escribible mientras se implementa.

Tres reglas hacen que funcione el resto.

**Un oráculo que el agente puede editar no es un oráculo.** El principio cuatro,
expresado en permisos de fichero. Durante la implementación las expectativas no
son escribibles. Un cambio que toca una implementación y sus expectativas en un
mismo commit dispara la revisión por construcción y no por la vigilancia de
alguien. Todo lo demás de esta sección depende de esta regla, y es la primera
que se relaja, porque relajarla hace desaparecer una build en rojo.

**Confirmar el rojo es como se prueba el oráculo.** La disciplina de la sección
15 suele leerse como una regla de tests primero. En términos de arnés es más
precisa que eso: es la única comprobación barata de que el oráculo observa lo
que dice observar. Una expectativa que pasa antes de que exista la
implementación no es evidencia, y las tres explicaciones posibles, que el
comportamiento ya existía, que el test no observa lo que dice, o que la
especificación describe mal el sistema, son cosas que conviene aprender antes de
escribir el código y no después de ponerlo en producción.

**Da por hecho que la batería es decorativa hasta que algo demuestre lo
contrario.** "¿Estos tests valen algo?" tiene una respuesta mecánica: cambia una
constante en la implementación y mira si algo se pone en rojo. El testing por
mutación automatiza exactamente eso, y es lo más parecido que hay a un oráculo
para tus oráculos. Caro sobre toda una base de código, barato sobre los veinte
ficheros que implementan tus reglas ratificadas, que es el único sitio donde la
respuesta importa.

Y el límite, dicho sin rodeos, porque una sección sobre validación automática
que lo omita está vendiendo algo. Ningún oráculo te dice si la especificación
era correcta. Ninguno te dice si una abstracción tiene el tamaño adecuado, que
es la razón de que las puertas de forma de la sección 8 sean preguntas que se le
hacen a una persona y no aserciones que ejecuta un programa. Ninguno te dice si
un requisito legal se leyó bien. El trabajo del arnés con los tres no es
decidirlos. Es encaminarlos a quien decide, mientras todavía es barato, y
negarse a cerrar mientras estén abiertos.

### Construir flujos con agentes

La primera pregunta es la que la gente se salta, porque las dos respuestas se
llaman igual en el material de marketing.

> **Enumera los puntos de decisión. Si puedes enumerarlos, escribe un flujo de
> trabajo. Si no puedes, necesitas un agente, y entonces necesitas acotarlo.**

El flujo de control de un flujo de trabajo lo escribes tú y se puede inspeccionar
antes de ejecutarlo. El de un agente se decide en tiempo de ejecución, lo que
compra adaptabilidad y te cuesta la capacidad de saber de antemano qué va a
pasar. La mayoría de los sistemas en producción que se describen como agénticos
son flujos de trabajo con uno o dos pasos genuinamente agénticos dentro, y esa
suele ser la forma correcta y no una confesión de timidez.

Tengas el que tengas, cinco reglas evitan que se descomponga.

**Las fases son estados, con condiciones de entrada y de salida.** No etapas de
un diagrama. Una fase en la que puedes entrar sin cumplir una condición es una
etiqueta, y a menos que la condición de salida sea un oráculo la fase no
termina, se abandona.

**Los traspasos llevan artefactos, no conversación.** La fase siguiente lee
ficheros. Si necesita el razonamiento de la fase anterior, ese razonamiento es
ahora un artefacto, y se aplica el principio uno. Pasar hacia delante una
transcripción parece continuidad y es la manera en que un flujo adquiere una
dependencia de una ventana de contexto que nadie controla.

**Los roles tienen permisos de escritura distintos.** Quien propone escribe
especificaciones, quien implementa escribe código, ninguno de los dos escribe
evidencia. Justificado por partida doble, como señala la sección 10: la higiene
de contexto lo quiere y la separación de funciones lo exige.

**Los puntos de control humanos son estados, no interrupciones.** La
ratificación es una fase de la tabla de la sección 15 exactamente por esto. Un
punto de control modelado como interrupción se optimiza hasta desaparecer por
ser fricción, porque eso es lo que parece en un cuadro de mando. Un punto de
control modelado como estado tiene una condición de entrada, una cola y una
latencia, y las tres se pueden medir y discutir. Palacio da la razón práctica,
que es la fatiga de aprobación: un agente que pide permiso por cada cambio
produce decenas de interrupciones por sesión, y la respuesta de la gente es
aprobar sin leer. Concentrar la revisión en las puertas entre fases, donde la
información vale más y corregir cuesta menos, es lo que permite que la fase de
implementación se ejecute con poca intervención.

**Todo bucle necesita una salida con nombre que no sea el éxito.** Escalar, y
decir a quién, con qué. Un flujo sin ella encuentra sus propias salidas, y las
que encuentra son agotar el presupuesto, agotar el contexto y declarar el éxito.
La tercera es la cara. Alenezi lo formula como propiedad del bucle y la
formulación es la correcta: agotar el presupuesto escala a una persona en vez
de bajar el listón en silencio.

Junto todo, eso es lo que es la tabla de fases de la sección 15: una máquina de
estados cuyo estado vive en ficheros, cuyas transiciones están guardadas por
oráculos, y cuyos permisos de escritura difieren por fase. Escrita como
especificación del arnés, tiene este aspecto.

| Fase | Lo que el agente puede escribir | La transición exige |
|---|---|---|
| Propuesta | Borradores de propuesta | Esquema válido, los identificadores citados resuelven |
| Clarificación | La lista de preguntas | Ninguna pregunta bloqueante sin responder |
| Ratificación | Nada | Una aprobación humana registrada |
| Evidencia | Borradores de expectativas | Aprobación humana del resultado esperado |
| Confirmar el rojo | Nada | La evidencia nueva falla |
| Implementación | Solo rutas de código | La build pasa |
| Verificación | Solo rutas de código | Todas las filas requeridas verificadas, CI en verde |
| Integración | Nada | La fórmula de cierre evalúa a verdadero |

La columna del medio lleva el argumento. Dos fases en las que el agente no
escribe nada en absoluto son lo que impide que el bucle sea un circuito cerrado,
y son las dos primeras que se ensanchan discretamente cuando un equipo va con
retraso.

Palacio expresa la misma tabla desde el lado del agente, con tres niveles que
cualquier fichero de proyecto puede adoptar tal cual: *siempre*, lo que se hace
sin preguntar, como ejecutar los tests antes de un commit; *pregunta primero*,
lo que puede ser correcto pero tiene impacto, como tocar el esquema, añadir una
dependencia o modificar la API pública; y *nunca*, las líneas rojas, como
confirmar secretos, borrar un test que falla o salirse del alcance de la tarea.
Lo útil del esquema no son los ejemplos, es que separa autonomía de permiso: el
nivel *siempre* existe para que el agente no interrumpa por cada microdecisión,
y el nivel *nunca* elimina categorías enteras de error en vez de detectarlas. Y
es un marco que se mueve: algo pasa de *pregunta primero* a *siempre* cuando el
equipo ha visto al agente decidir bien en ese ámbito. Los permisos de la tabla
anterior son lo mismo con una diferencia: el fichero de proyecto lo pide y el
arnés lo impone.

### Qué le da cada uno al otro

Esto no es la relación entre una metodología y sus herramientas, y se lee mejor
en las dos direcciones.

**El trabajo de especificación le da al arnés lo que no puede calcular por sí
mismo:** una condición de salida que significa algo, que son obligaciones
ratificadas y no la sensación de completitud del propio modelo; un modelo de
estado ya diseñado, porque la matriz de cobertura es el estado del bucle; una
razón para los límites de permisos que no es paranoia; y un disparador de
escalado definido, el marcador de clarificación.

**El arnés le da al trabajo de especificación lo único que lo hace real:** una
puerta necesita algo que de verdad se ejecute, de verdad bloquee y no se pueda
sortear, y las tres son propiedades del arnés. La sección 8 define qué es una
puerta. El arnés es donde "obligatoria" deja de ser un adjetivo.

Y el argumento de Alenezi para poner el juicio humano arriba y no abajo es el
más contundente que conozco, porque no apela a la virtud sino a la aritmética.
Una persona revisando código generado a la velocidad a la que se genera es a
la vez el cuello de botella y el eslabón más débil, y lo segundo está medido:
quien revisa con un asistente al lado escribe código menos seguro y está más
convencido de lo contrario. El recurso escaso va donde más palanca tiene,
redactar el contrato y atender las escaladas. El volumen de la comprobación lo
hace el validador.

Que es la frase que hay que llevarse de esta sección:

> **Una especificación sin arnés es un deseo. Un arnés sin especificación es una
> manera eficiente de converger hacia la intención de nadie.**

---

## 17. De dónde sale la especificación

El bucle de la sección 15 empieza en la captura, con "la petición literal".
Todo lo que viene después da por hecho que alguien escribió esa frase. Seyff y
Glinz, en un artículo de posición de 2026, señalan lo que esa suposición
esconde: la práctica "guarda silencio en gran medida sobre de dónde salen las
especificaciones". La herramienta asume que las escribe un desarrollador, a
solas con un asistente. El censo de SpecMine confirma la forma: la
especificación la escribe un desarrollador o, "más a menudo", la redacta una
herramienta de IA y el desarrollador la retoca.

Léelo despacio, porque es la parte más débil de todo el montaje. El artefacto
más importante del proceso lo redacta la persona con menos acceso a lo que el
negocio quiere, y lo redacta con ayuda de un modelo que tiene sus propias
inclinaciones. Las secciones anteriores gobiernan lo que pasa con la
especificación una vez existe. Esta trata de los dos fallos que pasan antes.

### Desambiguar demasiado pronto

Seyff y Glinz lo dicen con una frase que merece guardarse: *la desambiguación
prematura puede ser un defecto y no una virtud.* Si el modelo resuelve cada
elemento poco definido adivinando, fija interpretaciones que las personas
interesadas no han tenido ocasión de validar. Su regla para la asistencia en la
fase temprana es que señale la falta de definición en vez de resolverla en
silencio: "este elemento aparece en tres sitios con relaciones distintas, ¿es
intencionado?".

Es el principio dos visto desde el otro lado. No basta con que el artefacto
pueda decir "no lo sé"; el paso que lo redacta tiene que tener permiso para
dejar cosas abiertas, y una plantilla que exige un valor en cada campo se lo
quita. Conecta con el coste que la sección 3 llamaba compromiso prematuro y con
la distinción de Hill que retoma la sección 19: una especificación escrita
antes de validar nada es una conjetura con estructura. Para lo que ya entiendes,
el orden "primero la especificación, después el código" es el correcto. Para lo
que todavía no entiendes, la especificación honesta se escribe después del
prototipo y antes de la segunda versión.

### La deriva hacia el sistema medio

El segundo fallo es más sutil y no tiene nombre en la literatura sobre
especificaciones, aunque sí en la de modelado. Los modelos de lenguaje traen
inclinaciones fuertes hacia las notaciones estándar, UML, BPMN, diagramas
entidad-relación, y, más en general, hacia la forma más frecuente de un
problema. Seyff y Glinz lo llaman homogeneización: sin contramedidas, los
proyectos asistidos por un modelo derivan hacia el mismo puñado de patrones.
Traducido a especificaciones, un borrador redactado por un modelo deriva hacia
el sistema medio, que no es el tuyo. Sus contramedidas son concretas: limitar la
recuperación al contexto de la sesión, penalizar el vocabulario importado, y un
modo explícito de "quédate dentro de nuestro lenguaje".

La versión de esta guía es una prueba de lectura. El vocabulario de la
especificación tiene que ser el del negocio. Un borrador que llega con palabras
que nadie en la sala usa es un borrador que ha importado otro sistema, y las
seis preguntas de la sección 5 se contestan solas, con las respuestas de otro,
sin que se note.

### Tres reglas de diseño que ya estaban aquí con otro nombre

Los autores proponen principios para la asistencia de IA en esa fase, y tres de
ellos son cosas que esta guía sostiene desde otro ángulo, lo que sugiere que son
propiedades del problema y no de la herramienta.

*Proponer, nunca imponer.* Toda asignación, todo cambio estructural, es una
sugerencia que la persona acepta, modifica o rechaza. Es "el agente propone,
una persona ratifica" aplicado antes de que exista un requisito.

*Inferencias visibles y reversibles.* Cada inferencia del modelo es un evento
de primera clase en la historia del modelo, y se puede deshacer. Es el
principio uno aplicado a las decisiones que toma el redactor, no solo a las que
toma el negocio.

*Trazabilidad de cada inferencia a su origen.* Cada tipo propuesto, cada regla
inferida, tiene que apuntar al elemento del que sale, y en la práctica eso se
impone exigiendo que cada propuesta cite al menos un elemento de origen por
identificador. Esta es la que la guía no tenía como comprobación y debería. En
el repositorio de la sección 13, cada requisito deriva de una intención. Un
requisito cuyo `derives_from` está vacío es un requisito que inventó el
redactor, y un validador puede negarse a ratificar mientras haya uno. Es una
comprobación barata de la única clase de invención que la sección 5 no puede
ver: la que llega ya vestida de regla.

### La entrevista

Hay una técnica más mundana que la mayoría de los equipos puede aplicar mañana,
y Fontoura la toma de la documentación de Anthropic: antes de escribir nada,
pídele al modelo que te entreviste. Que no pregunte lo obvio, que vaya a las
partes difíciles que no has considerado, casos límite, compromisos, y que solo
después escriba la especificación. Después, implementa en una sesión limpia,
para que la implementación se ajuste al documento y no a la conversación que lo
produjo.

Es la fase de clarificación de la sección 15 ejecutada antes de la propuesta
en vez de después, y funciona por la misma razón que el marcador: convierte en
preguntas lo que de otro modo serían suposiciones. Con un límite que la sección
1 ya señaló: una entrevista produce respuestas a la velocidad a la que una
persona puede darlas, en caliente. El marcador conserva la opción de no
responder todavía. Una buena entrevista termina con algunas preguntas sin
contestar, escritas, y con el token de estado sin cambiar.

---

## 18. Cuando hay más de un lector

Todo lo anterior vale para una persona y un agente. En un equipo, la
especificación conserva ese trabajo y coge dos más, y no verlo es como se acaba
con una carpeta de especificaciones que nadie lee y un ritual en el que nadie
cree.

| La especificación está entre | Lo que lleva |
|---|---|
| Una persona y el agente | La única memoria que tiene el agente, y lo que acota su deriva |
| Una persona y otra | Lo que un compañero lee en vez de leerte la mente |
| Un equipo y otro | El contrato en la frontera donde dos equipos se integran |

La trampa es tratar una especificación de equipo como una especificación
individual con más autores. Sigues escribiendo notas privadas, les pones una
carpeta compartida y lo llamas práctica. Las notas siguen dando por supuesto
todo lo que hay en tu cabeza. Un compañero abre el fichero, tropieza con la
primera regla implícita y adivina, que es exactamente el problema que las
especificaciones existen para matar. La prueba de la sección 3 se aplica igual:
tu compañero y el agente tienen la misma desventaja, ninguno estaba en tu
cabeza.

### La discusión se muda a la capa más barata

La regla que convierte una carpeta en una práctica de equipo es la que menos se
escribe, y Fontoura la escribe: **la especificación entra en revisión antes de
que exista el código.** Los requisitos llegan como una pull request, alguien
los lee, y solo cuando los aprueba cambia el estado y empieza el diseño. Lo
mismo con el diseño. Lo mismo con las tareas.

Una revisión de código después de implementar atrapa erratas en una decisión
que ya estaba mal. Una revisión de la especificación atrapa la decisión
equivocada antes de que una línea la codifique. La revisión más cara que hace
un equipo es la de después, cuando el desacuerdo es sobre una cosa terminada.

| Dónde aparece el desacuerdo | Lo que cuesta resolverlo |
|---|---|
| En la pull request de los requisitos | Un hilo de comentarios, antes de que exista código |
| En la revisión de código | Reescribir una funcionalidad que ya funciona |
| En la integración, entre equipos | Dos implementaciones que no encajan |
| En producción | Un incidente, y después todo lo anterior |

El valor de la especificación en un equipo no es la documentación. Es mover la
discusión a la capa donde tenerla cuesta menos. Un equipo con especificaciones
no discrepa menos. Discrepa antes.

### Revisar un documento no es revisar código

Palacio hace una observación que parece menor y no lo es: las puertas
anteriores a la implementación revisan texto, no código, y eso cambia quién
puede participar y qué se está preguntando. Más gente puede leer una
especificación que un diff: quien conoce el negocio puede decir si los
requisitos son los correctos sin saber programar. Y las dos preguntas que
compiten en una revisión de código, "¿es esto lo que queremos?" y "¿está bien
construido?", se separan: las puertas de antes responden a la primera, la
verificación de después responde a la segunda. Dos revisiones enfocadas cansan
menos que una que intenta hacer las dos cosas.

Sobre quién aprueba, la respuesta de Palacio es la buena: depende del equipo, y
lo esencial no es el rol sino que la aprobación sea un acto deliberado y
explícito. Alguien lee el artefacto, lo evalúa contra criterios conocidos y
decide si basta para avanzar. Quien conoce el dominio aprueba los requisitos.
Quien conoce el código aprueba la descomposición en tareas, que es la puerta
más técnica y donde más vale la pena que estén los desarrolladores. Y alguien
vigila las puertas mismas, para que ni se salten por presión de calendario ni
se conviertan en cuello de botella porque la persona que aprueba no está.

### El canon vive en la herramienta

A solas, tus convenciones viven en ti. En un equipo, si viven solo en cabezas,
cada desarrollador deriva en su propia dirección y acabas con cinco dialectos
de especificación que no se parecen en nada. El arreglo es el principio siete
en su forma organizativa: el canon va donde lo lee la herramienta. El contexto
duradero de la sección 13 con todo el equipo como autor y lector, las plantillas
y las skills que llevan el formato y el listón a la máquina de cada uno, y las
convenciones escritas: cuándo un cambio necesita especificación, cuál es el
formato, quién aprueba cada puerta.

Esto cambia también la incorporación. Una persona nueva lee las
especificaciones y el contexto duradero, no una página de wiki y un compañero
al que preguntar. Una convención que vive en la memoria de la persona más
veterana escala exactamente al número de personas que esa persona puede
corregir en persona. Una codificada en un fichero escala a todo el que ejecute
el agente, incluido el agente.

### La puerta tiene que ser física

A solas, el token de estado lo lees tú. En un equipo, una puerta que solo vive
en un fichero que nadie abre es una puerta que se salta, porque la mayoría no
la ve. Fontoura la pone en un tablero: una columna por fase, una tarjeta por
cambio, y la tarjeta se mueve cuando se aprueba la puerta. Aprobar *es* mover.
Con una regla que evita que el tablero se convierta en una segunda fuente de
verdad: Git guarda el artefacto y el tablero refleja el estado; la tarjeta
apunta a la especificación, no la copia.

Y la puerta gana músculo con lo que la sección 8 llama política obligatoria,
aplicada ahora a las personas: la protección de rama se niega a fusionar sin
revisión. La puerta tiene que ser física, no una norma que la gente recuerda en
sus días buenos.

### El cuello de botella se mueve

La razón de que todo esto compense en un equipo no tiene nada que ver con la
velocidad de teclear. A solas, tu cuello de botella era tu propio bucle. En un
equipo la generación se abarata deprisa, porque todo el mundo tiene un agente,
y el equipo puede producir varias veces más código que antes. Lo que sale a
producción no crece al mismo ritmo, porque la pared se ha movido: ahora está en
la revisión, en el despliegue y en la coordinación entre personas y equipos.
Fontoura lo resume en una frase que merece el subrayado: **generar es barato;
integrar es el trabajo.**

El único caso de empresa que Alenezi cita apunta en la misma dirección desde el
otro lado, y con la reserva de que es un solo caso: un ingeniero con cuatro
agentes especializados entregó una iniciativa dimensionada para un equipo de
cuatro personas, y la ganancia más consistente no vino de generar más rápido
sino de colapsar el bucle exterior de coordinación entre disciplinas, porque
una especificación compartida era el único referente al que todos miraban. Un
tablero con límite de trabajo en curso en la columna de revisión hace visible
esa pared: las tarjetas se amontonan ahí, y ningún agente más rápido las
despeja.

### Cómo falla en un equipo

Palacio cataloga las formas en que esto sale mal mientras parece salir bien, y
tres merecen vigilarse desde el primer mes.

**Teatro de especificación.** Se escriben especificaciones y se ejecutan las
puertas, pero la revisión es superficial y la firma es un trámite. La causa
suele ser una de dos: presión de tiempo, o especificaciones tan genéricas que
revisarlas no aporta nada. La respuesta no es más disciplina, es o mejores
especificaciones o menos proceso en los cambios que no lo necesitan.

**Documentación zombi.** El proyecto acumula especificaciones que nadie
consulta, nadie actualiza y nadie borra. Es el modo anclado adoptado sin un
proceso de mantenimiento: rigor en el primer ciclo, abandono en los siguientes.
La decisión consciente de qué especificaciones se mantienen y cuáles se tiran
tras implementar es parte del trabajo, y una especificación que se mantiene
tiene responsable.

**La especificación como herramienta de control.** Cada decisión tiene que
pasar por una puerta y la autonomía de quien construye desaparece. Es confundir
la estructura del proceso con el control del equipo. El nivel *siempre* de la
sección 16 existe precisamente para que las decisiones rutinarias no necesiten
aprobación; si el equipo siente que las puertas le limitan en vez de apoyarle,
la calibración está mal.

---

## 19. Lo que dice la evidencia

La revisión anterior de esta guía terminaba con una advertencia: nada de esto
está demostrado. Desde entonces alguien lo ha medido, y el resultado no es
halagador. Esta sección existe porque una guía que argumenta a favor de una
práctica debe a sus lectores el mejor argumento en contra, y ahora hay uno con
datos.

### El estudio

Hill, en un documento de trabajo de abril de 2026, analiza 100.247 pull
requests fusionadas en 119 repositorios de código abierto. Deriva cinco
hipótesis de las afirmaciones literales de los fabricantes, Spec Kit y Kiro
sobre todo: que las especificaciones reducen los defectos, que reducen el
retrabajo, que mejores especificaciones producen menos defectos y menos
retrabajo, y que acotan el alcance del código generado por IA. Traza los
defectos hasta el commit que los introdujo y compara a cada autor consigo
mismo, sus cambios con especificación contra sus cambios sin ella, que es el
diseño más conservador disponible para datos observacionales.

No se sostiene ninguna de las cinco. Dentro de cada autor, los cambios con
especificación llevan asociados más defectos (1,4 puntos más, en el límite de
la significación) y más retrabajo (5 puntos más, con p por debajo de 0,001).
La calidad de la especificación, puntuada en siete dimensiones que copian las
plantillas de las propias herramientas, tiene un efecto sobre el retrabajo de
exactamente cero. Y el efecto de acotar el alcance de los cambios con IA no
aparece. Cuatro comprobaciones de robustez, con otras medidas de resultado, con
las variables clásicas de predicción de defectos, dimensión a dimensión y a
nivel de repositorio, dicen lo mismo. Añadir "tiene especificación" a un modelo
de predicción de defectos mejora su ajuste en 0,000014.

La lectura del autor es la de la medicina: confusión por indicación. Las
tareas más difíciles, grandes y arriesgadas son las que reciben
especificación, y son también las que producen más defectos, así que la
especificación señala la dificultad en vez de reducirla.

### Lo que sí dice, y lo que no

Los límites los enumera el propio estudio, y son los que un lector honesto
apuntaría. Todo es código abierto, con una muestra de conveniencia. La medida
de "tiene especificación" es deliberadamente laxa: un enlace a una incidencia
cuenta. La calidad la puntuó un modelo de lenguaje. Y la mayor parte de los
datos son anteriores a los flujos agénticos: solo 2.650 pull requests llevan
etiqueta de IA, y en ellas la especificación no muestra ningún efecto en
ninguna dirección; el subconjunto más parecido al flujo que venden las
herramientas, especificaciones de alta calidad en cambios con IA, da 4,8 puntos
menos de defectos sobre 42 autores, que el autor califica de sugerente y no
robusto. Así que el mejor dato disponible dice que el beneficio anunciado no se
ve, no dice que la práctica sea inútil, y todavía no observa el flujo al que
más apunta.

Lo que este estudio hace con las afirmaciones comerciales es definitivo, y lo
que hace con esta guía es distinto, y conviene separar las dos cosas. El
argumento de la sección 1 nunca fue "menos errores". Fue que alguien pueda
responder, seis semanas después, por qué el sistema hace lo que hace y quién lo
acordó. Hill llega al mismo sitio desde los datos: las especificaciones "crean
valor después de que el código salga, no durante la generación", como rastro
de auditoría y como documentación que sobrevive a quien la escribió. Y añade
la frase que resume mejor que ninguna de esta guía por qué la generación no
resuelve el problema: *la especificación le dice a la IA qué construir; no le
dice lo que olvidó especificar.* La parte difícil no se resuelve, se reubica.

Que esta guía sobreviva al estudio porque nunca prometió lo que el estudio
refuta es una defensa, y también una afirmación más débil, y hay que decirla
como tal: lo que se defiende aquí es quién responde de qué y qué se puede
reconstruir, no una tasa de defectos.

### La cadena del 50 %

Hay un detalle del estudio que esta guía tiene que recoger porque es su propia
advertencia sobre las citas heredadas cumpliéndose. Piskala afirma que
"estudios controlados muestran reducciones de errores de hasta el 50 %". Hill
siguió la cita: lleva a un artículo del blog de desarrolladores de Red Hat y a
un artículo de InfoQ, y ninguno de los dos contiene un estudio, un experimento
ni un dato. Es una opinión de practicante que adquirió aspecto de evidencia a
base de repetirse. El apartado de fuentes de esta guía ya avisaba de que
Piskala es un argumento bien organizado y no evidencia; ahora se sabe además
que la única cifra que da no es suya ni de nadie.

### Los números del otro lado

Los números favorables existen y conviene leerlos con la misma lupa. El modelo
de referencia de Alenezi lleva en el resumen una reducción del 73 % en defectos
de seguridad bajo restricciones constitucionales y una reducción del 50 % en el
tiempo de salida al mercado. En el cuerpo del artículo, el propio autor
clasifica ambos como "evidencia de caso sin replicar", sobre la que "el
argumento no apoya su peso": un proyecto bancario con el mismo desarrollador
en las dos condiciones, y un ingeniero con cuatro agentes en un banco
brasileño. Léase el resumen y luego ese párrafo, y mídase la distancia. Lo que
sí tiene el artículo, y es más útil que las cifras, es un contraejemplo
honesto: un experimento preinscrito de Borg y otros no encontró desventaja de
mantenibilidad en código desarrollado con asistentes cuando había disciplina de
revisión convencional. La lectura de Alenezi es que la variable moderadora es
la gobernanza, no la IA, y él mismo la marca como hipótesis coherente con los
datos y no como hallazgo.

Fontoura aporta un caso de practicante que vale más por cómo lo delimita que
por sus cifras: trece aplicaciones, tres APIs, unas 138.000 líneas y unos 1.650
tests, en setenta días, a solas, sobre 28 especificaciones. Los límites los
escribe él: no generaliza, porque el método externaliza la pericia y no la
fabrica; se midió la velocidad y no se auditó la calidad; había una fecha de
entrega haciendo trabajo; y es un dato sin grupo de control. Su conclusión es
la correcta: el método funcionó a esa escala, una vez, para ese operador.

### Los críticos de oficio

Dos críticas de practicantes circulan lo bastante como para citarlas. Scott
Logic puso Spec Kit a prueba y lo encontró unas diez veces más lento que el
desarrollo iterativo, produciendo miles de líneas de markdown que aun así
dieron código con errores; lo llamó "waterfall reinventado". Zaninotto, desde
la experiencia de Marmelab en producción, escribe que la práctica brilla al
empezar de cero y que, a medida que la aplicación crece, las especificaciones
"pierden el punto más a menudo y frenan el desarrollo". Las dos son críticas a
la forma de una herramienta, un flujo único para todos los tamaños, que las
secciones 3 y 11 ya hacen, y la respuesta de Palacio es la proporcionalidad:
un arreglo de una línea no pasa por cuatro fases. Pero no conviene despacharlas
tan rápido. Lo que las dos describen, la relación entre volumen de documentos y
cambio real, es lo que Hill mide como retrabajo, y le sale en la misma
dirección.

### Lo que se sabe del problema, no del remedio

Hay un segundo cuerpo de datos que las fuentes citan mucho y que conviene
situar, porque no habla de especificaciones sino de asistencia con IA en
general. METR, en 2025, midió a dieciséis desarrolladores experimentados sobre
sus propios repositorios: con herramientas de IA tardaron un 19 % más y
creyeron haber ido un 24 % más rápido. El informe DORA de 2025, según lo
recoge Fontoura, encontró un 98 % más de pull requests y un 243 % más de
incidentes por pull request en los equipos con IA. Pearce y otros encontraron
vulnerabilidades en cerca del 40 % del código generado en contextos sensibles.
Esta guía cita esos tres a través de otras fuentes y así lo dice en el
apartado de fuentes. Establecen el problema con solidez: la velocidad es real,
la percepción de la velocidad no es fiable, y la tasa de fallo sube más rápido
que el caudal. No establecen que la especificación sea el remedio. Eso es lo
que Hill fue a buscar y no encontró.

### Lo que se sabe de la práctica misma

SpecMine, el censo de la Carnegie Mellon de julio de 2026, es el primer
retrato de la práctica a escala, y dice tres cosas que un lector debería tener
en la cabeza al leer cualquier afirmación sobre ella. La práctica tiene un año:
el 99,7 % de las 470.795 especificaciones se creó en 2025 o después. La mayor
parte es andamiaje: de 73.030 repositorios, 923 tienen cien estrellas o más, y
el censo marca los ficheros diminutos, los marcadores sin rellenar y el texto
de relleno como señales de plantillas que nadie completó. Y cómo una
especificación se convierte en código sigue siendo, en palabras de los autores,
una pregunta abierta: el 81,2 % de las pull requests que tocan una
especificación tocan también código, pero eso es una heurística, no una
observación de la relación. El estudio que hay que esperar es el que cruce ese
censo con los resultados: cuántos marcadores se resuelven, cuántas
especificaciones se abandonan a medias, y si alguna de las dos cosas predice
algo.

### Qué medir en tu propio equipo

Como ningún estudio observa todavía tu flujo, la medida que importa es la tuya.
Palacio propone un cuadro razonable, y esta guía lo adopta con un cambio de
énfasis. De flujo: la proporción entre tiempo de especificación y tiempo de
implementación, la tasa de aprobación en primera revisión en cada puerta, y la
tasa de desviación, cuántas veces el agente se salió de los parámetros de la
especificación y hubo que intervenir. De resultado: la calidad al primer
intento, el tiempo de retrabajo y el tiempo de revisión, que con un contrato
claro debería bajar porque se revisa contra la especificación y no contra el
criterio del revisor. Y lo que no medir: líneas generadas y número de
especificaciones; más especificaciones no es mejor.

El cambio de énfasis es este. Las tres medidas de resultado son exactamente las
que Hill encontró en la dirección equivocada en su muestra. Si en la tuya
también salen así, la sección 3 ya dijo lo que toca: la estructura no se ha
ganado su sitio, y no hay lealtad que valga a una práctica que empeora las
cifras que prometía mejorar. Lo que esta guía pide que se mida además, y ningún
estudio mide todavía, es lo que defiende: cuánto tarda alguien en responder,
sobre un cambio de hace tres meses, qué se decidió, quién lo aprobó y qué
evidencia lo sostiene. Si esa cifra no baja, tampoco hay excusa.

### Resumen honesto

Los beneficios que se venden no son los beneficios que se han mostrado. Menos
defectos y menos retrabajo se han buscado a escala y no han aparecido. Memoria,
decisiones atribuibles y evidencia que cae del proceso no se han medido, y son
el argumento de esta guía. Y ningún estudio observa todavía el flujo en el que
la especificación es la entrada principal de un agente, que es donde las
herramientas apuntan y donde esta guía vive. Esta sección es la que antes
envejecerá, y es la que hay que releer en cada revisión.

---

## 20. Qué llevarse

Si te vas a quedar con siete cosas.

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

6. **El arnés es donde "obligatorio" se vuelve verdad.** La mayor parte de la
   distancia entre una demostración y un sistema está en el programa que rodea
   al modelo, y casi nada de ese programa lo revisa nadie.

7. **Los beneficios que se venden no son los que se han mostrado.** Menos
   defectos y menos retrabajo se han buscado en cien mil pull requests y no han
   aparecido. Memoria, decisiones atribuibles y evidencia que cae del proceso
   no se han medido, y son el argumento de esta guía.

Y una cosa de la que desconfiar, también en esta guía: la estructura es barata
de añadir y sus beneficios son sobre todo costes evitados, que son invisibles a
menos que los midas. Si un equipo añade trazabilidad y le empeoran a la vez la
tasa de defectos y el tiempo de ciclo, la trazabilidad no se ha ganado su
sitio. La sección 19 dice qué se ha medido ya y con qué resultado. Lo que falta
por medir es lo tuyo.

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
  heredadas ocurriendo delante de nosotros. Y su única cifra, "estudios
  controlados" con reducciones de errores "de hasta el 50 %", remite a dos
  artículos de blog sin ningún estudio detrás, como documenta Hill.
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
- Brenn Hill, *Does Spec-Driven Development Reduce Defects? An Empirical Test of
  Industry Claims Across 119 Open-Source Repositories*, documento de trabajo,
  SSRN, abril de 2026. Leído completo. La única medición a escala que existe, y
  la fuente de casi toda la sección 19. Sus límites los enumera él mismo y esta
  guía los repite: código abierto, muestra de conveniencia, medida laxa de
  "tiene especificación", calidad puntuada por un modelo, y datos en su mayoría
  anteriores a los flujos agénticos. Los datos y el código están publicados,
  que es más de lo que puede decir ninguna otra fuente de esta lista.
- Mamdouh Alenezi, *Specification-Driven Development as the Foundation of
  AI-Native Enterprise Software Engineering*, arXiv 2607.16680, julio de 2026.
  Leído completo. Un modelo de referencia formal, la especificación como tupla
  de obligaciones funcionales, umbrales de calidad, restricciones
  constitucionales y estructura arquitectónica, con un generador estocástico
  dentro de un validador determinista. La fuente de "aceptación por observación
  frente a aceptación por verificación", de la monotonía del validador y del
  argumento sobre dónde poner el juicio humano. Sin datos propios; su corpus de
  44 fuentes está verificado una a una, y su apartado 6.4 pesa la evidencia con
  una honestidad que el resumen del artículo no refleja.
- Shyam Agarwal, Anmol Singhal, Travis Breaux y Bogdan Vasilescu, *SpecMine: A
  Large-Scale Corpus of Spec-Driven Development Artifacts*, arXiv 2608.25202,
  Carnegie Mellon, septiembre de 2026. Leído completo. Un conjunto de datos, no
  un resultado: el censo de la práctica en GitHub, con la cuenta de marcadores
  de clarificación y de huecos sin rellenar por documento. La fuente de las
  cifras de la sección 19 sobre la edad y la composición de la práctica.
- Norbert Seyff y Martin Glinz, *From Sketches to Specs: AI-Assisted Lightweight
  Metamodeling for Spec-Driven Development*, artículo de posición, MoDRE 2026.
  Leído completo. La fuente de la sección 17: la observación de que la práctica
  calla sobre el origen de las especificaciones, la desambiguación prematura
  como defecto, la homogeneización hacia notaciones estándar y los principios de
  diseño para la asistencia. Sin evaluación empírica, y lo dicen.
- Kevin Ryan, *Spec Driven Development: AI Native Software Engineering*,
  primera edición, 2026, versión beta temprana. Solo existe el primer capítulo
  y es el que se ha leído. La fuente de los cinco niveles de Shapiro, del caso
  StrongDM con sus escenarios externos y sus réplicas de servicios, y de la
  lectura del cuello de botella que se mueve. Las cifras de METR y de DORA que
  cita esta guía se citan a través de él y de Fontoura, no de los originales.
- Juan Palacio, *SDD, Spec Driven Development: cuando el código es la
  consecuencia*, guía didáctica de Scrum Manager, versión 1.0, abril de 2026.
  Leída completa. Escrita con asistencia de un modelo y lo declara. La fuente de
  la "documentación operativa", de la maldición de las instrucciones, de los
  tres niveles de límites, de la fatiga de aprobación, del cuadro de métricas y
  de los antipatrones de la sección 18. Es también la fuente que mejor lee la
  objeción del waterfall. Usa "constitución del proyecto" para el fichero de
  contexto, no en el sentido de Spec Kit, y la sección 11 lo señala.
- Felipe Fontoura, *Spec-Driven Development: The Definitive Guide to Building
  Software with AI Agents*, 2026. Leído completo. La fuente del fichero de
  estado de una línea y de "que el fichero exista no implica aprobación", de
  las tres capas de contexto, de "confirma antes de construir", del formato de
  informe de verificación, del capítulo sobre equipos y del caso de las trece
  aplicaciones, cuyos límites él mismo escribe. Un libro de practicante con un
  kit que vender, y aun así el más cuidadoso de las fuentes de practicante en
  distinguir lo que demostró de lo que cree.
- François Zaninotto (Marmelab), *Spec-Driven Development: The Waterfall Strikes
  Back*, noviembre de 2025, y Scott Logic, *Putting Spec Kit Through Its Paces*,
  noviembre de 2025. Citados a través de Hill y de Palacio, no leídos en el
  original. Son las dos críticas de practicante que la sección 19 recoge.

Tres capítulos son más ligeros en fuentes que el resto y sería deshonesto no
decir cuáles. La sección 9 destila las fuentes de arriba en vez de añadirles: los
mecanismos son suyos, la reducción a siete principios es mía, y quien trazara la
línea en otro sitio no estaría obviamente equivocado. La sección 16 es sobre todo
práctica. "Arnés" es uso corriente en la comunidad de herramientas para agentes y
el material de Ralph aporta el argumento del estado en disco, pero el orden de
construcción, el orden de las palancas de reducción de errores y la tabla de
permisos por fase son lo que ha funcionado y no lo que se ha publicado, y deben
leerse con ese peso. Y la sección 19 es la que más depende de un único estudio,
que además todavía no ha pasado por revisión de pares.

---

## Preguntas abiertas para la siguiente revisión

- Verificar todas las citas de arriba. Las citas heredadas son la vía por la que
  se propagan los errores, y la entrada de Piskala contiene ahora dos ejemplos
  resueltos de ello. En particular, leer METR, DORA y Pearce en el original
  antes de que la sección 19 los cite como si lo hubiéramos hecho.
- La comparativa de herramientas ya no está, desde la revisión 0.4. Era la
  sección que iba a envejecer más rápido, los hallazgos prácticos de Böckeler ya
  habían empezado a contradecir partes de ella, y una guía que envejece mal en
  una sección hace que se desconfíe de todas. Lo que valía la pena de ahí, la
  constitución como ejemplo de una herramienta que llega con opiniones, se movió
  a la sección 11.
- El capítulo legal necesita que lo contradiga alguien que se dedique a esto. Está
  escrito desde el lado de la ingeniería de una conversación que tiene dos lados.
- Añadir un ejemplo resuelto de principio a fin, completo, en vez de en fragmentos.
  Fontoura enseña cómo se hace: cinco especificaciones completas para un mismo
  producto, cada requisito trazado a una decisión de diseño y a una tarea con
  comando de verificación. La promoción de puntos de esta guía podría recibir el
  mismo trato en un apéndice.
- La sección 19 responde a la pregunta de la revisión anterior sobre el mejor
  argumento en contra, y la sección 3 sigue tratando el coste solo en cualitativo.
  La propia comparación de Spec Kit, unas doce horas de trabajo de documentación
  contra quince minutos de comandos, y el "diez veces más lento" de Scott Logic
  son las cifras con las que tendría que enfrentarse un apartado de coste.
- La pregunta sobre la constitución está medio respondida en la sección 11: se
  distingue de una guía de estilo cuando un validador la ejecuta. Queda la otra
  mitad, quién ratifica un cambio en ella y con qué procedimiento.
- La sección 17 propone una comprobación nueva, negarse a ratificar un requisito
  sin origen, y nadie la ha ejecutado. Es barata de probar sobre un repositorio
  real y conviene hacerlo antes de recomendarla con más convicción.
- La sección 16 ordena las palancas de reducción de errores por retorno sobre
  esfuerzo. Ese orden es un juicio de la práctica y nada de aquí lo mide. La
  afirmación de que la calidad de los mensajes de error supera a la ingeniería
  de prompts es la más comprobable de esta guía y la más embarazosa si resulta
  falsa.
- El testing por mutación se recomienda en la sección 16 como oráculo de los
  oráculos, sobre un subconjunto de ficheros. Nadie aquí lo ha ejecutado a esa
  escala sobre un repositorio cuyos tests escribió un agente, que es
  exactamente el caso para el que se recomienda.
- La guía tiene ahora veinte secciones y el subtítulo promete brevedad. Las
  secciones 9, 16, 17, 18 y 19 la han empujado muy por encima de lo que
  promete. La siguiente revisión debería o quitar "breve" o quitar capítulos, y
  lo segundo es la decisión más difícil de tomar honestamente sobre lo que uno
  mismo escribe.
- La sección 19 envejecerá antes que ninguna. Hill es un documento de trabajo,
  SpecMine es un conjunto de datos que alguien explotará pronto, y las
  replicaciones de los casos favorables llegarán o no. Releerla en cada
  revisión.
