FROM python:3.11-slim

WORKDIR /app

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

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000
RUN python manage.py collectstatic --noinput

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120"]
