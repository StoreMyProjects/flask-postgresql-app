FROM surnet/alpine-wkhtmltopdf:3.18.0-0.12.6-full

RUN apk add --no-cache python3 py3-pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]