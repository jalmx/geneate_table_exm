# HTML Exam Table Generator (`gtable`)

Este script en Python permite convertir un archivo de texto plano con preguntas y respuestas (y opcionalmente un archivo JSON con respuestas incorrectas) en una **tabla limpia en formato HTML**. Es una herramienta ideal para generar material de exámenes estructurado y listo para impresión o visualización web.

El programa mezcla las opciones de respuesta de forma aleatoria y soporta tanto preguntas de **Opción Múltiple** como de **Verdadero o Falso**.

---

## 🚀 Características

* **Detección Automática de Formato:** Si la pregunta cuenta con un set de respuestas incorrectas en el archivo JSON, se procesa como opción múltiple; de lo contrario, se genera automáticamente como una pregunta de Verdadero/Falso.
* **Aleatorización (Shuffle):** Mezcla las respuestas en cada ejecución para garantizar que la opción correcta no quede siempre en laJ misma posición.
* **Limpieza de Texto:** Elimina automáticamente la numeración previa o guiones de las preguntas originales (`1.-`, `-`, etc.) para evitar redundancias en el HTML final.
* **Manejo de Errores Silencioso:** Si ocurre un fallo durante la ejecución, el script genera un archivo de registro `.log` con los detalles del error sin interrumpir abruptamente el flujo.

---

## 📋 Requisitos

* **Python 3.x** (No requiere la instalación de librerías de terceros, utiliza módulos nativos de la suite estándar).

---

## 🛠️ Estructura de los Archivos de Entrada

### 1. Archivo de Preguntas (`.txt`)
El archivo de texto debe intercalar estrictamente **una línea para la pregunta** y **una línea para la respuesta correcta**:

```text
1.- ¿Cuál es la capital de Francia?
París
2.- El agua hierve a 100 grados Celsius.
Verdadero

```

### 2. Archivo de Respuestas Incorrectas (`.json`) - *Opcional*

Para habilitar la opción múltiple, se debe proveer un archivo JSON donde la **clave** sea el número de la pregunta (basado en el índice de aparición en el archivo `.txt`) y el **valor** sea una lista con las respuestas incorrectas (distractores):

```json
{
  "1": ["Londres", "Madrid", "Berlín"]
}

```

---

## 💻 Modo de Uso

Ejecuta el script desde tu terminal utilizando alguna de las siguientes variantes:

### Opción A: Examen de Verdadero o Falso únicamente

Si solo se proporciona el archivo de texto, todas las preguntas tendrán las opciones estandarizadas "Verdadero" y "Falso".

```bash
python gtable.py mi_examen.txt

```

### Opción B: Examen Mixto o de Opción Múltiple

Al pasar el archivo JSON como segundo argumento, las preguntas que coincidan con los índices especificados se transformarán en opción múltiple.

```bash
python gtable.py mi_examen.txt respuestas_falsas.json

```

### Desplegar Ayuda

Para ver las instrucciones de uso directamente en la línea de comandos:

```bash
python gtable.py --help

```

---

## 📄 Salida (Output)

El script creará un archivo en el mismo directorio del archivo origen con el sufijo `_table.html` (por ejemplo, `mi_examen_table.html`).

La estructura del HTML generado conserva el siguiente formato de rejilla:

```html
<table width="100%">
  <tbody>
    <tr>
      <td colspan="3">1.- ¿Cuál es la capital de Francia?</td>
    </tr>
    <tr>
      <td width="33%" style="text-align: center;">Madrid</td>
      <td width="33%" style="text-align: center;">París</td>
      <td width="33%" style="text-align: center;">Londres</td>
    </tr>
  </tbody>
</table>

```
