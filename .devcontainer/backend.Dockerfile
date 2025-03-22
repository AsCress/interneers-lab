FROM python:3.13

WORKDIR /workspace/backend

COPY . ../

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001