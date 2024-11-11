import pandas as pd
import os
import subprocess

# Función para copiar el contenido del archivo Excel original a uno nuevo
def copiar_excel(original, nuevo):
    # Leer el archivo original con pandas
    excel_data = pd.read_excel(original, sheet_name=None)  # Cargar todas las hojas
    
    # Crear un nuevo archivo Excel con pandas y openpyxl
    with pd.ExcelWriter(nuevo, engine='openpyxl') as writer:
        for sheet_name, df in excel_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)  # Copiar cada hoja al nuevo archivo

    print(f"Archivo {nuevo} creado con éxito.")

# Función para convertir el nuevo archivo Excel a PDF usando LibreOffice
def convertir_excel_a_pdf(archivo_excel):
    if not os.path.exists(archivo_excel):
        raise FileNotFoundError(f"El archivo {archivo_excel} no existe.")
    
    # Ejecutar el comando de LibreOffice para convertir a PDF
    result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', archivo_excel])
    
    if result.returncode == 0:
        print(f"{archivo_excel} ha sido convertido a PDF exitosamente.")
    else:
        print(f"Error al convertir {archivo_excel} a PDF.")

# Ruta del archivo original
archivo_original = 'archivo_original.xlsx'

# Ruta del nuevo archivo que se creará
archivo_nuevo = 'archivo_nuevo.xlsx'

# Copiar el contenido del archivo Excel original al nuevo
copiar_excel(archivo_original, archivo_nuevo)

# Convertir el nuevo archivo Excel a PDF
convertir_excel_a_pdf(archivo_nuevo)
