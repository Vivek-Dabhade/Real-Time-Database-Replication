FROM python:3.15-rc-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
# pip freeze >> req.txt
# create venv
# enter in venv 
# install reuirements
# add venv to .gitignore and .dockerignore files.
