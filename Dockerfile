#Imagen base de Python
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/tmp /app/output
#Usuario no root por seguridad
RUN useradd -m esuarez
USER esuarez
CMD [ "python", "src/generar_documentos.py"]