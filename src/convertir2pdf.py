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

# Función para convertir el nuevo archivo a PDF usando LibreOffice
def convertir_a_pdf(archivo_a_convertir):
    if not os.path.exists(archivo_a_convertir):
        raise FileNotFoundError(f"El archivo {archivo_a_convertir} no existe.")
    #Obtener ruta de la carpeta en la que se desea guardaar el archivo a partir dearchivo de entrada
    ruta_carpeta_tmp = os.path.abspath('tmp')
    os.makedirs(ruta_carpeta_tmp, exist_ok=True)

    # Ejecutar el comando de LibreOffice para convertir a PDF
    result = subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', archivo_a_convertir, '--outdir', ruta_carpeta_tmp])
    
    if result.returncode == 0:
        print(f" ha sido convertido a PDF exitosamente. Guardado en -> {ruta_carpeta_tmp}")
    else:
        print(f"Error al convertir {archivo_a_convertir} a PDF.")
if __name__ == "__main__":
    # Ruta del archivo original
    archivo_original = 'archivo_original.xlsx'

    # Ruta del nuevo archivo que se creará
    archivo_nuevo = 'archivo_nuevo.xlsx'

    # Copiar el contenido del archivo Excel original al nuevo
    copiar_excel(archivo_original, archivo_nuevo)

    # Convertir el nuevo archivo Excel a PDF
    convertir_a_pdf(archivo_nuevo)
