FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN rm -rf /usr/lib/python3.12/site-packages/setuptools \
	/usr/lib/python3.12/site-packages/setuptools-*.dist-info \
	/usr/lib/python3.12/site-packages/msgpack \
	/usr/lib/python3.12/site-packages/msgpack-*.dist-info \
	/usr/lib/python3.12/site-packages/wheel-*.dist-info \
	/usr/local/lib/python3.12/site-packages/setuptools \
	/usr/local/lib/python3.12/site-packages/setuptools-*.dist-info \
	/usr/local/lib/python3.12/site-packages/msgpack \
	/usr/local/lib/python3.12/site-packages/msgpack-*.dist-info \
	/usr/local/lib/python3.12/site-packages/wheel-*.dist-info
RUN pip install --no-cache-dir --upgrade pip setuptools wheel msgpack
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade "setuptools>=78.1.1" "msgpack>=1.2.1" \
	&& python -c "from importlib.metadata import version; assert tuple(map(int, version('setuptools').split('.')[:2])) >= (78, 1); assert tuple(map(int, version('msgpack').split('.')[:2])) >= (1, 2)"

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]