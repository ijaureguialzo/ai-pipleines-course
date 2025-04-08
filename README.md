# Verificación de Instalación de Hugging Face

Este repositorio contiene herramientas para verificar que la instalación del SDK de Hugging Face está correctamente configurada en tu sistema.

## Instrucciones de Instalación

### 1. Crear un entorno virtual

Primero, es recomendable crear un entorno virtual para aislar las dependencias de este proyecto:

### 0. Clonar el repositorio

Primero, clona este repositorio en tu máquina local:
```bash
git clone https://github.com/Tknika/ai-pipleines-course
```


```bash
sudo apt update
```
```bash
 sudo apt install python3.12-venv
```

```bash
# Crear un nuevo entorno virtual con el módulo venv incorporado en Python
python -m venv .venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

Una vez activado el entorno virtual, verás el nombre del entorno entre paréntesis al inicio de la línea de comandos, por ejemplo: `(venv)`.

### 2. Instalar dependencias

Para instalar todas las dependencias necesarias, ejecuta el siguiente comando en tu terminal:

```bash
pip install -r requirements.txt
```

Este comando instalará todos los paquetes requeridos, incluyendo:
- transformers
- datasets
- huggingface-hub
- torch
- accelerate

### 3. Verificar la instalación

Una vez instaladas las dependencias, puedes verificar que todo funciona correctamente ejecutando el script de prueba:

```bash
python test/check_huggingface_installation.py
```

El script realizará las siguientes comprobaciones:
- Verificará que PyTorch está instalado correctamente
- Comprobará que los paquetes de Hugging Face están disponibles
- Probará la conexión con la API de Hugging Face Hub
- Cargará un modelo pequeño y ejecutará una inferencia de prueba

### Solución de problemas

Si encuentras algún error durante la verificación:

1. Asegúrate de que el entorno virtual está activado.

2. Asegúrate de haber instalado todas las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Si tienes problemas con PyTorch, visita la [página oficial de PyTorch](https://pytorch.org/get-started/locally/) para obtener instrucciones específicas para tu sistema.

4. Para problemas con la conexión a Hugging Face Hub, verifica tu conexión a internet y que tengas los permisos necesarios.

5. Si el error persiste, revisa los mensajes específicos mostrados por el script para identificar el problema exacto.

## Requisitos del sistema

- Python 3.7 o superior
- Conexión a internet para descargar modelos
- Suficiente espacio en disco para los modelos (al menos 500 MB para las pruebas básicas) 