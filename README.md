# Verificación de Instalación de Hugging Face

Este repositorio contiene herramientas para verificar que la instalación del SDK de Hugging Face está correctamente configurada en tu sistema.

## Instalación y configuración de WSL en Windows

### 1. Instalar WSL en Windows

Para instalar WSL en Windows 10/11:

1. Abre PowerShell como administrador
2. Ejecuta el siguiente comando:
   ```bash
   wsl --install
   ```

3. Reinicia tu computadora cuando se te solicite

Este comando instalará Ubuntu por defecto. Si prefieres otra distribución, puedes instalarla después con:
```bash
wsl --install -d <Distribución>
```

Por ejemplo:
```bash
wsl --install -d Ubuntu
```

### 2. Configurar WSL

Después de reiniciar, WSL se iniciará automáticamente y te pedirá que configures un nombre de usuario y contraseña para tu distribución Linux.

### 3. Actualizar WSL (opcional)

Para actualizar a WSL 2 (recomendado para mejor rendimiento):
```bash
wsl --set-default-version 2
```

### 4. Usar WSL desde Visual Studio Code

1. Instala la extensión "Remote - WSL" en VS Code:
   - Abre VS Code
   - Ve a Extensions (Ctrl+Shift+X)
   - Busca "Remote Development" e instala todas las extensiones

2. Conectar a WSL desde VS Code:
   - Haz clic en el icono verde "><" en la esquina inferior izquierda de VS Code
   - Selecciona "New WSL Window" o "Connect to WSL"
   - VS Code se reabrirá conectado a tu distribución WSL

3. Navegar a tu proyecto:
   - Una vez conectado a WSL, puedes abrir una carpeta desde la terminal integrada:
   ```bash
   cd /path/to/your/project
   code .
   ```
   - O usar "File > Open Folder" para navegar a tu proyecto dentro del sistema de archivos de WSL

Ahora puedes ejecutar todos los comandos de instalación y verificación mencionados anteriormente dentro de tu entorno WSL.

## Instrucciones de Instalación

### 0. Clonar el repositorio

Primero, clona este repositorio en tu máquina local:
```bash
git clone https://github.com/Tknika/ai-pipleines-course
```

### 1. Crear un entorno virtual

Primero, es recomendable crear un entorno virtual para aislar las dependencias de este proyecto:

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

Ahora puedes ejecutar todos los comandos de instalación y verificación mencionados anteriormente dentro de tu entorno WSL. 