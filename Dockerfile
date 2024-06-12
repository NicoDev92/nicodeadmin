# Utilizar la imagen base de Python 3.8
FROM python:3.8

# Establecer la variable de entorno para evitar problemas de buffer con la consola
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instalar dependencias desde el archivo requirements.txt con barra de progreso desactivada
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

# Copiar el código fuente al contenedor
COPY . /app/

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
