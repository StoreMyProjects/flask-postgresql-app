FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel msgpack
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "msgpack>=1.2.1" \
	&& python -c "from importlib.metadata import version; assert tuple(map(int, version('setuptools').split('.')[:2])) >= (78, 1); assert tuple(map(int, version('msgpack').split('.')[:2])) >= (1, 2)"

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]