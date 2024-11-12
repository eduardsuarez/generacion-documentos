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

#Usuario no root por seguridad
RUN useradd -ms /bin/bash esuarez

# Cambiar la propiedad de todos los archivos a 'esuarez'
RUN chown -R esuarez:esuarez /generacion-documentos


RUN mkdir -p /generacion-documentos/tmp && \
    chmod -R 777 /generacion-documentos/tmp && \
    chown -R esuarez:esuarez /generacion-documentos/tmp


USER esuarez

EXPOSE 4449
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4449"]
