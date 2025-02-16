FROM python:3.11-alpine
RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    linux-headers
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["src/app.py"]
