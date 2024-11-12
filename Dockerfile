#Imagen base de Python
FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    flake8 \
    black \
    mypy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /generacion-documentos
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /generacion-documentos/tmp
#Usuario no root por seguridad
RUN useradd -m esuarez
USER esuarez
EXPOSE 4449
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4449"]
