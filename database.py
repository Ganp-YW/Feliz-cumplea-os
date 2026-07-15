import urllib.request
import csv
import io
import os

# REEMPLAZA ESTO CON EL ENLACE DE TU GOOGLE SHEET PUBLICADO COMO CSV
# (Asegúrate de que termine en pub?output=csv)
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSSNuisnHm8XxofulPkycI2j0mksjka9tc0IUj3-PJHxrGA2uWE2I6csRuraCRC_S2L3weTjkfmIJDh/pub?output=csv" 

def obtener_todos_los_mensajes():
    """Descarga los mensajes online, o usa el archivo local si falla o no hay enlace configurado"""
    mensajes = []
    
    # 1. Intentar descargar de internet
    if GOOGLE_SHEET_CSV_URL.startswith("http"):
        try:
            import sys
            if "pyodide" in sys.modules:
                from pyodide.http import open_url
                csv_data = open_url(GOOGLE_SHEET_CSV_URL).read()
            else:
                req = urllib.request.Request(GOOGLE_SHEET_CSV_URL)
                with urllib.request.urlopen(req) as response:
                    csv_data = response.read().decode('utf-8')
                
            reader = csv.reader(io.StringIO(csv_data))
            next(reader, None) # Saltar la primera fila (encabezados)
            for row in reader:
                if len(row) >= 3:
                    mensajes.append({
                        "texto": row[0], 
                        "categoria": row[1], 
                        "color": row[2].strip()
                    })
            if mensajes:
                return mensajes
        except Exception as e:
            print(f"Error descargando mensajes online: {e}")
            
    # 2. Si falla o no hay URL, usar el archivo local (100_mensajes.csv)
    try:
        if os.path.exists("100_mensajes.csv"):
            with open("100_mensajes.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if len(row) >= 3:
                        mensajes.append({
                            "texto": row[0], 
                            "categoria": row[1], 
                            "color": row[2].strip()
                        })
    except Exception as e:
        print(f"Error leyendo archivo local: {e}")
        
    if not mensajes:
        mensajes.append({"texto": "No se encontraron mensajes. Verifica tu conexión o el archivo.", "categoria": "Error", "color": "red"})
        
    return mensajes
