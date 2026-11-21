# Imagen de desarrollo de la aplicación Flask.
FROM python:3.13-slim

# No generar ficheros .pyc y mostrar los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Primero las dependencias: esta capa se reutiliza si requirements.txt no cambia
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Después el código de la aplicación
COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
