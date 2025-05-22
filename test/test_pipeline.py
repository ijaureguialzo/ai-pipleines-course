import os
import sys
from datetime import datetime

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from transformers import pipeline

# Configuración básica
CONFIG = {
    "credentials_file": "credentials.json",
    "spreadsheet_id": "18t1zpc9pBBxGn8ZmqP0uZoJjdz0-jdUHqdKxwG3MfyM",
    "model_name": "nlptown/bert-base-multilingual-uncased-sentiment",
    "report_folder": "reportes",
    "min_text_length": 10
}


def obtener_respuestas():
    """Conecta con Google Sheets y obtiene respuestas de texto"""
    print(f"Conectando a Google Sheets...")

    try:
        # Establecer conexión
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CONFIG["credentials_file"],
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(CONFIG["spreadsheet_id"]).sheet1

        # Obtener datos
        datos = sheet.get_all_records()
        if not datos:
            print("No se encontraron registros.")
            return {}

        # Extraer respuestas de texto
        respuestas = {}
        for pregunta in datos[0].keys():
            textos = [fila[pregunta] for fila in datos
                      if pregunta in fila and isinstance(fila[pregunta], str)
                      and len(fila[pregunta].strip()) >= CONFIG["min_text_length"]]

            if textos:
                respuestas[pregunta] = textos

        print(f"Se encontraron {len(respuestas)} preguntas con respuestas.")
        return respuestas
    except Exception as e:
        print(f"ERROR al obtener respuestas: {str(e)}")
        return {}


def analizar_sentimiento(textos):
    """Analiza el sentimiento de una lista de textos"""
    print(f"Analizando sentimiento con {CONFIG['model_name']}...")

    try:
        # Cargar modelo
        analizador = pipeline("sentiment-analysis", model=CONFIG["model_name"])

        # Analizar textos
        resultados = []
        for texto in textos:
            try:
                resultado = analizador(texto)[0]
                resultados.append({
                    "texto": texto,
                    "sentimiento": resultado["label"],
                    "confianza": round(resultado["score"], 2)
                })
                print(f"  - Analizado: '{texto[:30]}...' -> {resultado['label']}")
            except Exception as e:
                print(f"  - Error analizando texto: {str(e)}")

        return resultados
    except Exception as e:
        print(f"ERROR cargando modelo: {str(e)}")
        return []


def generar_reporte(resultados_por_pregunta):
    """Genera un reporte sencillo en formato markdown"""
    if not resultados_por_pregunta:
        return "# No hay resultados para analizar"

    # Iniciar reporte
    reporte = f"# Reporte de Análisis de Sentimiento\n"
    reporte += f"Fecha: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
    reporte += f"## Resumen por Pregunta\n\n"

    # Estadísticas globales
    todas_respuestas = []

    # Analizar cada pregunta
    for pregunta, resultados in resultados_por_pregunta.items():
        # Contar tipos de sentimiento
        sentimientos = {}
        for r in resultados:
            if r["sentimiento"] not in sentimientos:
                sentimientos[r["sentimiento"]] = 0
            sentimientos[r["sentimiento"]] += 1

        # Añadir resumen
        reporte += f"### {pregunta}\n"
        reporte += f"Total respuestas: {len(resultados)}\n\n"

        # Mostrar distribución de sentimientos
        reporte += "**Distribución de sentimientos:**\n"
        for sentimiento, cantidad in sentimientos.items():
            porcentaje = (cantidad / len(resultados)) * 100
            reporte += f"- {sentimiento}: {cantidad} ({porcentaje:.1f}%)\n"

        # Mostrar ejemplos
        reporte += "\n**Ejemplos:**\n"
        for r in resultados[:2]:  # Solo mostrar 2 ejemplos
            texto_corto = r["texto"][:100] + "..." if len(r["texto"]) > 100 else r["texto"]
            reporte += f"- \"{texto_corto}\" → {r['sentimiento']} ({r['confianza']})\n"

        reporte += "\n---\n\n"

        # Agregar a las estadísticas globales
        todas_respuestas.extend(resultados)

    return reporte


def guardar_resultados(resultados_por_pregunta):
    """Guarda resultados en archivos CSV y markdown"""
    # Crear carpeta si no existe
    if not os.path.exists(CONFIG["report_folder"]):
        os.makedirs(CONFIG["report_folder"])

    # Generar nombre de archivo con fecha
    fecha = datetime.now().strftime("%Y%m%d_%H%M")

    # Guardar reporte markdown
    reporte = generar_reporte(resultados_por_pregunta)
    ruta_md = f"{CONFIG['report_folder']}/reporte_{fecha}.md"
    with open(ruta_md, "w", encoding="utf-8") as f:
        f.write(reporte)
    print(f"Reporte guardado: {ruta_md}")

    # Guardar datos en CSV
    datos_planos = []
    for pregunta, resultados in resultados_por_pregunta.items():
        for r in resultados:
            datos_planos.append({
                "pregunta": pregunta,
                "texto": r["texto"],
                "sentimiento": r["sentimiento"],
                "confianza": r["confianza"]
            })

    # Guardar CSV
    if datos_planos:
        df = pd.DataFrame(datos_planos)
        ruta_csv = f"{CONFIG['report_folder']}/datos_{fecha}.csv"
        df.to_csv(ruta_csv, index=False)
        print(f"Datos guardados: {ruta_csv}")


def main():
    """Función principal del pipeline"""
    print(f"=== Iniciando análisis de sentimiento ===")

    # 1. Obtener respuestas de texto
    respuestas = obtener_respuestas()
    if not respuestas:
        print("No hay respuestas para analizar. Finalizando.")
        return

    # 2. Analizar sentimiento de cada pregunta
    resultados = {}
    for pregunta, textos in respuestas.items():
        print(f"Analizando: '{pregunta}'")
        resultados[pregunta] = analizar_sentimiento(textos)

    # 3. Guardar resultados
    guardar_resultados(resultados)
    print("=== Análisis completado ===")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR CRÍTICO: {str(e)}")
        sys.exit(1)
