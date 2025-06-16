# Base image
FROM python:3.11-slim

# Working directory
WORKDIR /app

# System dependencies for your application, including LaTeX and ffmpeg
RUN apt-get update && apt-get install -y \
    texlive-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    dvipng \
    cm-super \
    libcairo2-dev \
    libpango1.0-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    g++ \
    ffmpeg \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy project files
COPY . /app

# Expose port 8000 for Django
EXPOSE 8000

# Run Django application (the command will be handled by docker-compose)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
