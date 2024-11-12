from uuid import uuid4
import uuid
import openpyxl
import docx
import os
from datetime import datetime
from fastapi import FastAPI
from starlette.responses import JSONResponse
from src import convertir2pdf

app = FastAPI()

@app.get("/")
async def home():
    return {"Message": "Bienvenido a mi API"}

#Remmplazar valores en plantilla .docx
@app.post("/replaceDocx/")
async def reemplazar_docx():
    try:
        # Reemplazar valores en la plantilla
        print("Entró en /replaceDocx")
        ruta_actual = os.getcwd()
        ruta_plantilla = os.path.join(ruta_actual,"plantillas","formato-documento.docx")
        datos = {
            "FECHA_ACTUAL" : datetime.now().strftime("%H:%M:%S"),
            "INDUSTRIA_ESPECIFICA": "Redes de telecomunicaciones",
            "METRICA_RENDIMIENTO": "ROI",
            "NOMBRE_PLATAFORMA": "TELCO-BIT",
            "generatedPdf":"true"
        }
        documento = docx.Document(ruta_plantilla)

        for paragraph in documento.paragraphs:
            for run in paragraph.runs:
                for key, value in datos.items():
                    if f"${{{key}}}" in run.text:
                        run.text = run.text.replace(f"${{{key}}}", value)
        ruta_salida = f"temp_{uuid.uuid4()}.docx"
        ruta_salida_tmp = os.path.join(ruta_actual,"tmp",ruta_salida)
        documento.save(ruta_salida_tmp)
        print(f"se guardó documento correctamente -> {ruta_salida_tmp}")

        if "generatedPdf" in datos.keys() and datos["generatedPdf"] == "true":
            convertir2pdf.convertir_a_pdf(ruta_salida_tmp)
        return {"Mensaje": "Documento generado con éxito", "Ruta": ruta_salida_tmp}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "Mensaje": "Ocurrio un error al generar el documento"}
        )


# Reemplazar valores en la plantilla excel
@app.post("/replaceXlsx/")
async def reemplazar_xlsx():
    # Reemplazar valores en la plantilla
    print("Entró en /replaceXlsx")
    try:

        ruta_actual = os.getcwd()

        ruta_plantilla = os.path.join(ruta_actual,"plantillas","plantilla-excel.xlsx")

        valores = {
            "NOMBRE" : "Eduard Antonio",
            "APELLIDO": "Suárez Buitrago",
            "EMPRESA": "OSP International",
            "CORREO": "suareze205@gmail.com",
            "TELEFONO": "3227412700",
            "DIRECCION": "Calle 10 # 4-48",
            "generatedPdf":"true"
        }
        wb = openpyxl.load_workbook(ruta_plantilla)
        ws = wb.worksheets[0]
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and "${" in cell.value:
                    # Reemplazar el marcador con el valor correspondiente
                    for clave, valor in valores.items():
                        if f"${{{clave}}}" in cell.value:
                            cell.value = cell.value.replace(f"${{{clave}}}", str(valor))
        ruta_salida = f"{uuid.uuid4()}.xlsx"
        ruta_salida_tmp = os.path.join(ruta_actual,"tmp",ruta_salida)
        wb.save(ruta_salida_tmp)
        print(f"Archivo generado correctamente -> {ruta_salida_tmp}")

        if "generatedPdf" in valores.keys() and valores["generatedPdf"] == "true":
            convertir2pdf.convertir_a_pdf(ruta_salida_tmp)
        return {"Mensaje": "Documento generado con éxito", "Ruta": ruta_salida_tmp}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "Mensaje": "Ocurrio un error al generar el documento"}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4449)
