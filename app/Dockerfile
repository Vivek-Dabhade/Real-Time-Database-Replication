FROM python:3.12.4-alpine3.20

WORKDIR  /app

RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers 
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]

# pip freeze >> req.txt
# create venv
# enter in venv 
# install reuirements
# add venv to .gitignore and .dockerignore files.
