FROM python:3.13-slim-bullseye

WORKDIR /api

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

# CMD ["fastapi", "run", "main.py", "--port", "80"]
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]