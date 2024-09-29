FROM python:3.11-slim

WORKDIR /pet-project
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY pet-project ./
EXPOSE 8000
CMD ["gunicorn", "main:main_app"]