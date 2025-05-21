# Guía de Configuración para Análisis de Sentimiento con Google Forms

## Paso 1: Crear un Proyecto en Google Cloud
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las APIs:
   - [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
   - [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com)

## Paso 2: Configurar una Cuenta de Servicio
1. En la consola de Google Cloud, ve a "IAM & Admin" > "Service Accounts"
2. Haz clic en "Create Service Account"
3. Asigna un nombre y descripción para la cuenta
4. Otorga el rol "Editor" a la cuenta de servicio
5. Desde los 3 botones de acciones selecciona 'Administrar Claves'
5. Haz clic en "Agregar Clave", 'Crear nueva clave' y selecciona JSON
6. Guarda el archivo JSON en el mismo directorio que tu script (renómbralo a `credentials.json`)

## Paso 3: Compartir tu Google Sheet
1. Crea un [formulario de Google](https://docs.google.com/forms) con preguntas de texto libre
2. Configura las respuestas para que se guarden en una hoja de cálculo (en la pestaña respuestas de edicion del form)
3. Obtén el ID de la hoja de cálculo (parte larga en la URL):
   - Ejemplo: `https://docs.google.com/spreadsheets/d/`**`1AbCdEfGhIjKlMnOpQrStUvWxYz`**`/edit`
4. Haz clic en "Compartir" en la esquina superior derecha
5. Añade el email de la cuenta de servicio (lo encontrarás en el archivo de credenciales)
6. Otorga permisos de "Editor"

## Paso 4: Configurar el Script
1. Abre el archivo Python en tu editor
2. Modifica las siguientes variables globales al inicio del script:
   - `CREDENTIALS_FILE`: Ruta al archivo JSON de credenciales
   - `SPREADSHEET_ID`: El ID de tu hoja de cálculo
   - `REPORT_FOLDER`: Carpeta donde se guardarán los reportes (opcional)
   
## Paso 5: Instalar Dependencias (si no lo estan ya)
```bash
pip install pandas torch transformers gspread oauth2client
```

## Paso 6: Ejecutar el Script
```bash
python test_pipeline.py
```

## Funcionamiento
El script:
1. Se conecta a tu hoja de cálculo de Google
2. Identifica automáticamente todas las preguntas que tienen respuestas de texto
3. Analiza el sentimiento de cada respuesta utilizando Hugging Face
4. Genera un reporte que incluye:
   - Estadísticas generales y por pregunta
   - Ejemplos destacados de respuestas positivas y negativas
   - Una tabla con los resultados completos

## Notas Importantes
- El script detecta automáticamente qué campos contienen texto analizable
- Se ignorarán respuestas numéricas, de un solo carácter o demasiado cortas
- La primera ejecución puede tardar más tiempo ya que descarga el modelo
- Si quieres modificar qué se considera texto válido, ajusta el parámetro `min_text_length` en el script