FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["fastapi", "dev", "--host", "0.0.0.0"]
